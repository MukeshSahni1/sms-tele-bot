# 🚀 FREE BOMBER - Telegram Bot

A completely FREE Telegram bot for SMS, Call, and WhatsApp attacks with 234+ APIs.

## 🎯 Features

✅ **SMS Attacks** - Send unlimited SMS  
✅ **Call Attacks** - Make continuous calls  
✅ **WhatsApp Attacks** - Send WhatsApp messages  
✅ **Duration Control** - 1 min to 8 hours  
✅ **Number Protection** - Protect your number from attacks  
✅ **Admin Panel** - Broadcast and stats  
✅ **Completely FREE** - No premium gating

---

## 📦 Deployment on Vercel

### Prerequisites
- GitHub account with your code pushed
- Vercel account (connected to GitHub)
- Bot Token from Telegram BotFather

### Step 1: Update Webhook URL
Edit `api/webhook.py` and set your Vercel domain:

```python
WEBHOOK_URL = "https://your-project.vercel.app/api/webhook"
```

### Step 2: Push to GitHub
```bash
git add .
git commit -m "Vercel deployment ready"
git push origin main
```

### Step 3: Deploy on Vercel
1. Go to **vercel.com**
2. Click "New Project"
3. Select your GitHub repository
4. Click "Deploy"
5. After deployment, get your domain (e.g., `https://my-bot.vercel.app`)

### Step 4: Set Telegram Webhook
After Vercel deployment, set the webhook by visiting this URL in browser:

```
https://api.telegram.org/bot{YOUR_BOT_TOKEN}/setWebhook?url=https://your-project.vercel.app/api/webhook
```

Replace:
- `{YOUR_BOT_TOKEN}` with your actual bot token
- `your-project.vercel.app` with your Vercel domain

### Step 5: Test
Send `/start` to your bot on Telegram - it should respond!

---

## 🔧 Local Development

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Run locally (polling mode):
```bash
python3 2v3.py
```

### For webhook testing locally:
```bash
python3 api/webhook.py
```

---

## 📝 Configuration

Edit constants in `api/webhook.py`:

```python
BOT_TOKEN = "your_token_here"      # Get from BotFather
OWNER_ID = 6684734209              # Your Telegram user ID
WEBHOOK_URL = "your_vercel_url"    # Your Vercel webhook URL
WELCOME_IMAGE = "image_url"        # Custom welcome image
```

---

## 📊 Files Structure

```
.
├── 2v3.py                 # Local polling bot (for development)
├── api/
│   └── webhook.py        # Vercel serverless function
├── api.json              # 234 attack APIs
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── fusion_premium.db     # SQLite database
```

---

## 🆘 Troubleshooting

**Q: Webhook not working?**  
A: Make sure you set the webhook using the BotFather URL command above

**Q: Getting 404 errors?**  
A: Check that `/api/webhook` route exists in vercel.json

**Q: Bot not responding?**  
A: Verify BOT_TOKEN is correct and webhook is set

---

## ⚠️ Legal Notice

This bot is for educational purposes only. Unauthorized SMS/Call bombing may be illegal in your jurisdiction. Use responsibly!

---

## 📧 Support

Need help? Create an issue or contact the owner.

**Bot Status:** ✅ Live on Vercel
