from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json
import re
from textblob import TextBlob
import nltk
import openai
from dotenv import load_dotenv
import speech_recognition as sr
from wtforms import Form, StringField, TextAreaField, validators
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///journal.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

db = SQLAlchemy(app)

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

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

# Forms
class JournalEntryForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    content = TextAreaField('Content', [validators.Length(min=1)])

# AI Functions
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0.1:
        sentiment_label = 'positive'
    elif sentiment_score < -0.1:
        sentiment_label = 'negative'
    else:
        sentiment_label = 'neutral'
    return sentiment_score, sentiment_label

def generate_summary(text):
    if not openai.api_key:
        return "Summary generation requires OpenAI API key"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates concise summaries of journal entries. Keep summaries under 100 words and focus on the main themes and emotions."},
                {"role": "user", "content": f"Please summarize this journal entry: {text}"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def extract_tags(text):
    if not openai.api_key:
        words = text.lower().split()
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        tags = [word for word in words if len(word) > 3 and word not in common_words][:10]
        return tags
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Extract 5-10 relevant tags from this journal entry. Return only the tags separated by commas, no explanations."},
                {"role": "user", "content": text}
            ],
            max_tokens=100,
            temperature=0.3
        )
        tags = response.choices[0].message.content.strip().split(',')
        return [tag.strip() for tag in tags]
    except Exception as e:
        return []

# Routes
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    entries = JournalEntry.query.order_by(JournalEntry.date_created.desc()).limit(5).all()
    return render_template('dashboard.html', entries=entries, current_user={'username': 'Guest'})

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    form = JournalEntryForm(request.form)
    if request.method == 'POST' and form.validate():
        sentiment_score, sentiment_label = analyze_sentiment(form.content.data)
        summary = generate_summary(form.content.data)
        tags = extract_tags(form.content.data)
        tags_json = json.dumps(tags)
        entry = JournalEntry(
            title=form.title.data,
            content=form.content.data,
            sentiment_score=sentiment_score,
            sentiment_label=sentiment_label,
            summary=summary,
            tags=tags_json
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
    entries = entries_query.order_by(JournalEntry.date_created.desc()).all()
    return render_template('search.html', entries=entries, query=query, emotion=emotion, date_filter=date_filter)

@app.route('/voice_input')
def voice_input():
    return render_template('voice_input.html')

@app.route('/process_voice', methods=['POST'])
def process_voice():
    try:
        return jsonify({
            'success': True,
            'text': 'This is a demo voice input. In a real implementation, this would process the uploaded audio file using speech recognition.'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/analytics')
def analytics():
    entries = JournalEntry.query.all()
    sentiment_counts = {}
    for entry in entries:
        sentiment_counts[entry.sentiment_label] = sentiment_counts.get(entry.sentiment_label, 0) + 1
    monthly_activity = {}
    for entry in entries:
        month = entry.date_created.strftime('%Y-%m')
        monthly_activity[month] = monthly_activity.get(month, 0) + 1
    return render_template('analytics.html', 
                         sentiment_counts=sentiment_counts,
                         monthly_activity=monthly_activity,
                         total_entries=len(entries))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False) 