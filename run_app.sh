#!/bin/bash

echo "🚀 Starting AI Journal App..."
echo "=============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if requirements are installed
echo "📦 Checking dependencies..."
python3 -c "import flask" 2>/dev/null || {
    echo "📥 Installing dependencies..."
    python3 -m pip install -r requirements.txt
}

# Create database if it doesn't exist
echo "🗄️  Setting up database..."
python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
print('Database ready!')
"

# Start the app
echo "🌐 Starting server on http://localhost:8080"
echo "📱 You can also access it from your phone at http://YOUR_IP:8080"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python3 app.py 