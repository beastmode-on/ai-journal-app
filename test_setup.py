#!/usr/bin/env python3
"""
Test script to verify AI Journal setup
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_wtf',
        'textblob',
        'nltk',
        'openai',
        'speech_recognition',
        'wtforms',
        'python_dotenv'
    ]
    
    print("Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package}")
        except ImportError as e:
            print(f"✗ {package}: {e}")
            failed_imports.append(package)
    
    return failed_imports

def test_nltk_data():
    """Test if NLTK data is available"""
    print("\nTesting NLTK data...")
    try:
        import nltk
        nltk.data.find('tokenizers/punkt')
        print("✓ NLTK punkt tokenizer")
        return True
    except LookupError:
        print("✗ NLTK punkt tokenizer not found")
        print("  Run: python -c \"import nltk; nltk.download('punkt')\"")
        return False

def test_flask_app():
    """Test if Flask app can be created"""
    print("\nTesting Flask app creation...")
    try:
        from app import app, db
        print("✓ Flask app created successfully")
        return True
    except Exception as e:
        print(f"✗ Flask app creation failed: {e}")
        return False

def test_ai_functions():
    """Test AI functions"""
    print("\nTesting AI functions...")
    try:
        from app import analyze_sentiment, generate_summary, extract_tags
        
        # Test sentiment analysis
        text = "I am feeling great today!"
        score, label = analyze_sentiment(text)
        print(f"✓ Sentiment analysis: {label} ({score:.2f})")
        
        # Test summary generation (without API key)
        summary = generate_summary(text)
        print(f"✓ Summary generation: {summary[:50]}...")
        
        # Test tag extraction (without API key)
        tags = extract_tags(text)
        print(f"✓ Tag extraction: {tags}")
        
        return True
    except Exception as e:
        print(f"✗ AI functions test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("AI Journal Setup Test")
    print("=" * 50)
    
    # Test imports
    failed_imports = test_imports()
    
    # Test NLTK data
    nltk_ok = test_nltk_data()
    
    # Test Flask app
    flask_ok = test_flask_app()
    
    # Test AI functions
    ai_ok = test_ai_functions()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    if not failed_imports and nltk_ok and flask_ok and ai_ok:
        print("🎉 All tests passed! Your AI Journal is ready to run.")
        print("\nTo start the application:")
        print("  python app.py")
        print("\nThen open: http://localhost:5000")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        
        if failed_imports:
            print(f"\nMissing packages: {', '.join(failed_imports)}")
            print("Install with: pip install -r requirements.txt")
        
        if not nltk_ok:
            print("\nNLTK data missing. Run:")
            print("  python -c \"import nltk; nltk.download('punkt')\"")
        
        if not flask_ok:
            print("\nFlask app creation failed. Check your app.py file.")
        
        if not ai_ok:
            print("\nAI functions failed. This might be due to missing API keys.")
            print("Check your .env file configuration.")

if __name__ == "__main__":
    main() 