#!/bin/bash

echo "🤖 AI Journal Quick Deployment Script"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Make sure you're in the project directory."
    exit 1
fi

echo "✅ Project files found!"

# Step 1: Check Git status
echo ""
echo "📋 Step 1: Checking Git status..."
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized. Please run:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

echo "✅ Git repository ready!"

# Step 2: Check GitHub CLI
echo ""
echo "📋 Step 2: Checking GitHub CLI..."
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not installed. Installing..."
    brew install gh
fi

# Step 3: Check GitHub authentication
echo ""
echo "📋 Step 3: Checking GitHub authentication..."
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub."
    echo "🔐 Please authenticate by running:"
    echo "   gh auth login"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "✅ GitHub authentication ready!"

# Step 4: Create GitHub repository
echo ""
echo "📋 Step 4: Creating GitHub repository..."
REPO_NAME="ai-journal-app"

# Check if repository already exists
if gh repo view $REPO_NAME &> /dev/null; then
    echo "✅ Repository already exists: https://github.com/$(gh api user --jq .login)/$REPO_NAME"
else
    echo "🔧 Creating new repository..."
    if gh repo create $REPO_NAME --public --source=. --remote=origin --push; then
        echo "✅ Repository created successfully!"
    else
        echo "❌ Failed to create repository. Please check your GitHub permissions."
        exit 1
    fi
fi

# Step 5: Get repository URL
REPO_URL="https://github.com/$(gh api user --jq .login)/$REPO_NAME"
echo "📦 Repository URL: $REPO_URL"

# Step 6: Deploy to Render
echo ""
echo "📋 Step 5: Deploying to Render.com..."
echo ""
echo "🚀 Manual Deployment Steps:"
echo "1. Go to https://render.com"
echo "2. Sign up/Login with your GitHub account"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Connect your repository: $REPO_URL"
echo "5. Configure the service:"
echo "   - Name: ai-journal"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn app:app"
echo "   - Plan: Free"
echo "6. Click 'Create Web Service'"
echo ""
echo "⏳ Wait 2-3 minutes for deployment..."
echo ""
echo "🎉 Once deployed, your app will be available at:"
echo "   https://ai-journal.onrender.com"
echo ""
echo "📱 You can then access your AI Journal from anywhere in the world!"

# Optional: Try to open Render in browser
if command -v open &> /dev/null; then
    echo ""
    read -p "🌐 Open Render.com in your browser? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "https://render.com"
    fi
fi

echo ""
echo "✅ Deployment script completed!"
echo "📝 Next: Follow the manual steps above to deploy to Render." 