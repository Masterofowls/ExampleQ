#!/bin/bash

# Netlify Deployment Script for Flask Student Portal

echo "🚀 Starting Netlify deployment..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create dist directory for Netlify
echo "📁 Creating dist directory..."
mkdir -p dist
echo "Flask Student Portal - Deployed to Netlify!" > dist/index.html

echo "✅ Deployment preparation complete!"
echo "🌐 Your app will be available at the Netlify URL"
echo ""
echo "📋 Environment Variables to set in Netlify:"
echo "  SECRET_KEY=your-secret-key-here"
echo "  NETLIFY=true"
echo "  FLASK_ENV=production"
echo ""
echo "📖 Visit your Netlify dashboard to complete deployment"
