from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
import json
import re
from textblob import TextBlob
import nltk
from openai import OpenAI
from dotenv import load_dotenv
import speech_recognition as sr
from wtforms import Form, StringField, TextAreaField, validators
import uuid
import base64
from io import BytesIO

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///journal.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize OpenAI client (optional - app works without it)
client = None
try:
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key != 'your-openai-api-key-here':
        client = OpenAI(api_key=api_key)
    else:
        print("⚠️  OpenAI API key not found. AI features will be disabled.")
        print("   Set OPENAI_API_KEY environment variable to enable AI features.")
except Exception as e:
    print(f"⚠️  Could not initialize OpenAI client: {e}")
    print("   AI features will be disabled.")

db = SQLAlchemy(app)

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

# Optional speech recognition import
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("⚠️  Speech recognition not available. Voice features will be disabled.")

# Import VADER sentiment analyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Database Models
class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    sentiment_score = db.Column(db.Float, default=0.0)
    sentiment_label = db.Column(db.String(50), default='neutral')
    summary = db.Column(db.Text)
    tags = db.Column(db.Text)  # JSON string of tags
    word_count = db.Column(db.Integer, default=0)
    reading_time = db.Column(db.Integer, default=0)  # in minutes

# Forms
class JournalEntryForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    content = TextAreaField('Content', [validators.Length(min=1)])

# Enhanced AI Functions
def analyze_sentiment(text):
    """Enhanced sentiment analysis using both TextBlob and VADER"""
    # TextBlob analysis
    blob = TextBlob(text)
    textblob_score = blob.sentiment.polarity
    
    # VADER analysis
    vader_scores = sia.polarity_scores(text)
    vader_score = vader_scores['compound']
    
    # Combine both scores for better accuracy
    combined_score = (textblob_score + vader_score) / 2
    
    # Enhanced sentiment labeling
    if combined_score > 0.2:
        sentiment_label = 'positive'
    elif combined_score < -0.2:
        sentiment_label = 'negative'
    elif combined_score > 0.05:
        sentiment_label = 'slightly_positive'
    elif combined_score < -0.05:
        sentiment_label = 'slightly_negative'
    else:
        sentiment_label = 'neutral'
    
    return combined_score, sentiment_label

def generate_summary(text):
    """Generate AI summary using OpenAI GPT"""
    if not client:
        return "Summary generation requires OpenAI API key"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates concise, insightful summaries of journal entries. Focus on the main themes, emotions, and key events. Keep summaries under 100 words and maintain the personal tone."},
                {"role": "user", "content": f"Please summarize this journal entry: {text}"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def extract_tags(text):
    """Enhanced tag extraction using AI and NLP"""
    if not client:
        # Fallback to basic NLP tagging
        words = text.lower().split()
        # Remove common words and short words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'}
        tags = [word for word in words if len(word) > 3 and word not in common_words][:8]
        return tags
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Extract 5-8 relevant tags from this journal entry. Focus on emotions, activities, people, places, and themes. Return only the tags separated by commas, no explanations."},
                {"role": "user", "content": text}
            ],
            max_tokens=100,
            temperature=0.3
        )
        tags = response.choices[0].message.content.strip().split(',')
        return [tag.strip() for tag in tags if tag.strip()]
    except Exception as e:
        return []

def calculate_reading_time(text):
    """Calculate estimated reading time in minutes"""
    words = len(text.split())
    # Average reading speed: 200-250 words per minute
    reading_time = max(1, words // 200)
    return reading_time

def process_voice_audio(audio_data):
    """Process voice input using speech recognition"""
    if not SPEECH_RECOGNITION_AVAILABLE:
        return "Speech recognition is not available in this environment. Please type your entry instead."
    
    try:
        # Decode base64 audio data
        audio_bytes = base64.b64decode(audio_data.split(',')[1])
        
        # Create recognizer
        recognizer = sr.Recognizer()
        
        # Convert audio bytes to AudioData
        audio = sr.AudioData(audio_bytes, sample_rate=16000, sample_width=2)
        
        # Recognize speech
        text = recognizer.recognize_google(audio)
        return text
    except Exception as e:
        return f"Error processing voice: {str(e)}"

# Routes
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/test')
def test():
    return "AI Journal App is working! 🎉"

@app.route('/dashboard')
def dashboard():
    try:
        entries = JournalEntry.query.order_by(JournalEntry.date_created.desc()).limit(5).all()
        
        # Calculate dashboard stats
        total_entries = JournalEntry.query.count()
        this_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_entries = JournalEntry.query.filter(JournalEntry.date_created >= this_month).count()
        
        # Get sentiment distribution
        sentiment_stats = db.session.query(
            JournalEntry.sentiment_label,
            db.func.count(JournalEntry.id)
        ).group_by(JournalEntry.sentiment_label).all()
        
        return render_template('dashboard.html', 
                             entries=entries, 
                             current_user={'username': 'Guest'},
                             total_entries=total_entries,
                             monthly_entries=monthly_entries,
                             sentiment_stats=sentiment_stats)
    except Exception as e:
        # Return a simple error page for debugging
        return f"Dashboard Error: {str(e)}", 500

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    form = JournalEntryForm(request.form)
    if request.method == 'POST' and form.validate():
        # Enhanced AI processing
        sentiment_score, sentiment_label = analyze_sentiment(form.content.data)
        summary = generate_summary(form.content.data)
        tags = extract_tags(form.content.data)
        tags_json = json.dumps(tags)
        word_count = len(form.content.data.split())
        reading_time = calculate_reading_time(form.content.data)
        
        entry = JournalEntry(
            title=form.title.data,
            content=form.content.data,
            sentiment_score=sentiment_score,
            sentiment_label=sentiment_label,
            summary=summary,
            tags=tags_json,
            word_count=word_count,
            reading_time=reading_time
        )
        db.session.add(entry)
        db.session.commit()
        flash('Journal entry created successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html', form=form)

@app.route('/entry/<int:entry_id>')
def view_entry(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)
    tags = json.loads(entry.tags) if entry.tags else []
    return render_template('view_entry.html', entry=entry, tags=tags)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    emotion = request.args.get('emotion', '')
    date_filter = request.args.get('date', '')
    tag_filter = request.args.get('tag', '')
    
    entries_query = JournalEntry.query
    
    if query:
        entries_query = entries_query.filter(
            JournalEntry.content.contains(query) | 
            JournalEntry.title.contains(query)
        )
    if emotion:
        entries_query = entries_query.filter(JournalEntry.sentiment_label == emotion)
    if date_filter:
        try:
            search_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            entries_query = entries_query.filter(
                db.func.date(JournalEntry.date_created) == search_date
            )
        except ValueError:
            pass
    if tag_filter:
        entries_query = entries_query.filter(JournalEntry.tags.contains(tag_filter))
    
    entries = entries_query.order_by(JournalEntry.date_created.desc()).all()
    
    # Get all unique tags for filter
    all_tags = set()
    for entry in JournalEntry.query.all():
        if entry.tags:
            tags = json.loads(entry.tags)
            all_tags.update(tags)
    
    return render_template('search.html', 
                         entries=entries, 
                         query=query, 
                         emotion=emotion, 
                         date_filter=date_filter,
                         tag_filter=tag_filter,
                         all_tags=sorted(all_tags))

@app.route('/voice_input')
def voice_input():
    return render_template('voice_input.html')

@app.route('/process_voice', methods=['POST'])
def process_voice():
    try:
        data = request.get_json()
        audio_data = data.get('audio')
        
        if not audio_data:
            return jsonify({'success': False, 'error': 'No audio data received'})
        
        # Process the voice input
        text = process_voice_audio(audio_data)
        
        if text.startswith('Error'):
            return jsonify({'success': False, 'error': text})
        
        return jsonify({
            'success': True,
            'text': text
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/analytics')
def analytics():
    entries = JournalEntry.query.all()
    
    # Sentiment analysis
    sentiment_counts = {}
    for entry in entries:
        sentiment_counts[entry.sentiment_label] = sentiment_counts.get(entry.sentiment_label, 0) + 1
    
    # Monthly activity
    monthly_activity = {}
    for entry in entries:
        month = entry.date_created.strftime('%Y-%m')
        monthly_activity[month] = monthly_activity.get(month, 0) + 1
    
    # Word count trends
    word_counts = [entry.word_count for entry in entries]
    avg_word_count = sum(word_counts) / len(word_counts) if word_counts else 0
    
    # Most common tags
    all_tags = []
    for entry in entries:
        if entry.tags:
            tags = json.loads(entry.tags)
            all_tags.extend(tags)
    
    tag_counts = {}
    for tag in all_tags:
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return render_template('analytics.html', 
                         sentiment_counts=sentiment_counts,
                         monthly_activity=monthly_activity,
                         total_entries=len(entries),
                         avg_word_count=round(avg_word_count, 1),
                         top_tags=top_tags)

# Custom Jinja filters
@app.template_filter('from_json')
def from_json(value):
    if value:
        try:
            return json.loads(value)
        except:
            return []
    return []

if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
            print("Database initialized successfully!")
    except Exception as e:
        print(f"Database initialization error: {e}")
    
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False) 