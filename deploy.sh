#!/bin/bash

# 🚀 Automated Deployment Script for Telegram Bot on Vercel
# This script handles: GitHub upload + Vercel deployment

set -e

echo "================================"
echo "🚀 TELEGRAM BOT AUTO-DEPLOY"
echo "================================"
echo ""

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not found. Install it:"
    echo "   https://cli.github.com/"
    exit 1
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Step 1: GitHub Authentication
echo "1️⃣ Authenticating with GitHub..."
gh auth login --web

# Step 2: Create GitHub Repository
read -p "2️⃣ Enter your GitHub username: " GITHUB_USER
read -p "   Enter repository name (e.g., telegram-bot): " REPO_NAME

echo "   📝 Creating repository on GitHub..."
gh repo create $REPO_NAME --public --source=. --remote=origin --push || {
    echo "⚠️  Repository might already exist. Pushing to existing repo..."
    git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git" 2>/dev/null || true
    git branch -M main
    git push -u origin main
}

# Step 3: Vercel Deployment
echo ""
echo "3️⃣ Deploying to Vercel..."
echo "   Make sure you're logged in with: vercel login"

# Get Vercel domain
read -p "   After deployment, enter your Vercel domain (e.g., my-bot.vercel.app): " VERCEL_DOMAIN

# Step 4: Set Telegram Webhook
echo ""
echo "4️⃣ Setting Telegram Webhook..."
BOT_TOKEN="8736183103:AAELHZD1wr-qohEQQ0rSRXJY2-qtZzOag6g"
WEBHOOK_URL="https://$VERCEL_DOMAIN/api/webhook"

echo "   📡 Setting webhook to: $WEBHOOK_URL"

curl -s "https://api.telegram.org/bot$BOT_TOKEN/setWebhook?url=$WEBHOOK_URL" | python3 -m json.tool

echo ""
echo "================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "================================"
echo ""
echo "📊 Your Bot Info:"
echo "   GitHub: https://github.com/$GITHUB_USER/$REPO_NAME"
echo "   Vercel: https://$VERCEL_DOMAIN"
echo "   Webhook: $WEBHOOK_URL"
echo ""
echo "🧪 Test your bot:"
echo "   Send /start to your bot on Telegram!"
echo ""
