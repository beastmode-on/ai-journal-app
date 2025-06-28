#!/bin/bash

echo "🚀 AI Journal Vercel Deployment Script"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Make sure you're in the project directory."
    exit 1
fi

echo "✅ Project files found!"

# Step 1: Check if Vercel CLI is installed
echo ""
echo "📋 Step 1: Checking Vercel CLI..."
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not installed. Installing..."
    npm install -g vercel
fi

echo "✅ Vercel CLI ready!"

# Step 2: Check if user is logged in to Vercel
echo ""
echo "📋 Step 2: Checking Vercel authentication..."
if ! vercel whoami &> /dev/null; then
    echo "❌ Not logged in to Vercel."
    echo "🔐 Please login by running:"
    echo "   vercel login"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "✅ Vercel authentication ready!"

# Step 3: Deploy to Vercel
echo ""
echo "📋 Step 3: Deploying to Vercel..."
echo "🚀 Starting deployment..."

# Deploy with Vercel
if vercel --prod --yes; then
    echo ""
    echo "🎉 SUCCESS! Your AI Journal is now live on Vercel!"
    echo ""
    echo "📱 You can now access your journal from anywhere in the world!"
    echo "🌍 The app will be available at the URL shown above."
    echo ""
    echo "✨ Features available:"
    echo "   - Sentiment Analysis"
    echo "   - AI Summary Generation"
    echo "   - Smart Tagging"
    echo "   - Voice Input (demo)"
    echo "   - Search & Analytics"
    echo ""
    echo "📝 Next time you want to update your app, just run:"
    echo "   vercel --prod"
else
    echo "❌ Deployment failed. Please check the error messages above."
    exit 1
fi 