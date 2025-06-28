# AI Journal - Personal Journal with AI Features

A modern, AI-powered personal journal application that combines traditional journaling with cutting-edge artificial intelligence features. Write your thoughts, and let AI analyze your emotions, generate summaries, and create intelligent tags.

## 🌟 Features

### 🤖 AI-Powered Analysis
- **Sentiment Analysis**: Automatically detects mood (positive, negative, neutral) using TextBlob
- **Smart Summaries**: AI-generated concise summaries of longer entries using OpenAI GPT
- **Intelligent Tagging**: Automatic tag generation based on entry content
- **Emotion Tracking**: Visual representation of emotional patterns over time

### 🎤 Voice Input
- **Speech-to-Text**: Convert your voice to text for hands-free journaling
- **Real-time Recording**: Record your thoughts directly in the browser
- **Audio Processing**: Automatic transcription using SpeechRecognition

### 🔍 Advanced Search & Organization
- **Multi-criteria Search**: Search by keywords, emotions, or dates
- **Smart Filtering**: Filter entries by sentiment or time period
- **Tag-based Organization**: Organize entries with AI-generated tags

### 📊 Analytics & Insights
- **Visual Analytics**: Charts showing sentiment distribution and activity patterns
- **Journaling Insights**: Discover your writing patterns and emotional trends
- **Progress Tracking**: Monitor your journaling consistency

### 🎨 Modern UI/UX
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Beautiful Interface**: Modern, clean design with smooth animations
- **User-friendly**: Intuitive navigation and easy-to-use features

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- OpenAI API key (for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-journal
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   # Edit .env file with your configuration
   ```

5. **Initialize the database**
   ```bash
   python app.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open your browser**
   Navigate to `http://localhost:5000`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True

# OpenAI API Configuration (for AI features)
OPENAI_API_KEY=your-openai-api-key-here
```

### Getting an OpenAI API Key

1. Visit [OpenAI's website](https://openai.com/)
2. Create an account or sign in
3. Navigate to the API section
4. Generate a new API key
5. Add the key to your `.env` file

## 📖 Usage Guide

### Creating Your First Entry

1. **Register/Login**: Create an account or log in to your existing account
2. **New Entry**: Click "New Entry" from the dashboard
3. **Write**: Enter a title and your journal content
4. **AI Analysis**: The system automatically analyzes sentiment, generates a summary, and creates tags
5. **Save**: Click "Save Entry" to store your entry

### Using Voice Input

1. **Voice Input**: Navigate to the "Voice Input" page
2. **Start Recording**: Click "Start Recording" and allow microphone access
3. **Speak**: Clearly speak your thoughts into the microphone
4. **Stop Recording**: Click "Stop Recording" when finished
5. **Review**: Edit the transcribed text if needed
6. **Create Entry**: Click "Create Entry" to save

### Searching Entries

1. **Search Page**: Go to the "Search" page
2. **Keywords**: Enter search terms to find specific content
3. **Emotion Filter**: Filter by positive, negative, or neutral entries
4. **Date Filter**: Search for entries from specific dates
5. **Results**: View and click on matching entries

### Viewing Analytics

1. **Analytics Page**: Navigate to "Analytics"
2. **Overview**: See total entries and sentiment distribution
3. **Charts**: View visual representations of your journaling patterns
4. **Insights**: Discover trends and patterns in your writing

## 🛠️ Technical Details

### Architecture
- **Backend**: Flask (Python web framework)
- **Database**: SQLite (with SQLAlchemy ORM)
- **Frontend**: Bootstrap 5 + Custom CSS/JavaScript
- **AI**: TextBlob (sentiment analysis) + OpenAI GPT (summaries/tags)
- **Voice**: SpeechRecognition + Web Audio API

### Key Components

#### AI Functions
- `analyze_sentiment()`: Uses TextBlob for sentiment analysis
- `generate_summary()`: Uses OpenAI GPT for entry summarization
- `extract_tags()`: Uses OpenAI GPT for intelligent tagging

#### Database Models
- `User`: User accounts and authentication
- `JournalEntry`: Journal entries with AI analysis results

#### Routes
- `/`: Landing page
- `/dashboard`: Main user dashboard
- `/new_entry`: Create new journal entries
- `/voice_input`: Voice-to-text functionality
- `/search`: Advanced search and filtering
- `/analytics`: Data visualization and insights

## 🔧 Customization

### Adding New AI Features

1. **Create new AI function** in `app.py`
2. **Add to entry creation** in the `new_entry` route
3. **Update database model** if needed
4. **Add to templates** for display

### Styling Customization

- **CSS Variables**: Modify colors in `static/css/style.css`
- **Bootstrap Override**: Customize Bootstrap components
- **Animations**: Add new CSS animations

### Database Modifications

- **New Fields**: Add columns to existing models
- **New Models**: Create new database tables
- **Migrations**: Use Flask-Migrate for database changes

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

1. **Set environment variables**
   ```env
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=your-secure-secret-key
   ```

2. **Use a production WSGI server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Set up a reverse proxy** (nginx recommended)

4. **Use a production database** (PostgreSQL recommended)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **TextBlob**: For sentiment analysis
- **OpenAI**: For GPT-powered AI features
- **Bootstrap**: For the responsive UI framework
- **Flask**: For the web framework
- **SpeechRecognition**: For voice input functionality

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## 🔮 Future Features

- **Export functionality** (PDF, Word, etc.)
- **Collaborative journaling**
- **Mood tracking over time**
- **Journaling prompts and suggestions**
- **Mobile app version**
- **Advanced analytics and insights**
- **Integration with calendar apps**
- **Backup and sync features**

---

**Happy Journaling! 📖✨** 