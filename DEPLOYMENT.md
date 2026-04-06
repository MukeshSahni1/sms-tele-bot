# 🚀 QUICK DEPLOYMENT GUIDE

## ⚡ 3-Step Deployment (Takes 5 minutes!)

### Step 1: Create GitHub Repository
Visit https://github.com/new and:
- Set **Repository name** (e.g., `telegram-bot`)
- Select **Public**
- Click **Create repository**

### Step 2: Push Your Code to GitHub
Copy-paste these commands in terminal (in your bot directory):

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

Replace:
- `YOUR_USERNAME` - Your GitHub username
- `YOUR_REPO_NAME` - Your repository name

### Step 3: Deploy to Vercel
1. Go to https://vercel.com/new
2. Sign in with GitHub
3. Select your repository
4. Click **Deploy**
5. Copy your Vercel domain (e.g., `my-bot.vercel.app`)

### Step 4: Activate Bot Webhook
Visit this URL in your browser (replace the domain):

```
https://api.telegram.org/bot8736183103:AAELHZD1wr-qohEQQ0rSRXJY2-qtZzOag6g/setWebhook?url=https://YOUR-VERCEL-DOMAIN/api/webhook
```

Example:
```
https://api.telegram.org/bot8736183103:AAELHZD1wr-qohEQQ0rSRXJY2-qtZzOag6g/setWebhook?url=https://my-bot.vercel.app/api/webhook
```

### Step 5: Test Your Bot! ✅
Send `/start` to your bot on Telegram - it should respond!

---

## 🎯 What Gets Deployed?

✅ **api/webhook.py** - Server-side bot handler  
✅ **api.json** - 234 Attack APIs  
✅ **requirements.txt** - Python dependencies  
✅ **vercel.json** - Vercel configuration  
✅ **fusion_premium.db** - Database (auto-created)  

---

## 🔧 Configuration

### Environment Variables (Optional on Vercel)
If you want to customize, set these in Vercel Dashboard → Settings → Environment Variables:

- `WEBHOOK_URL` = Your full webhook URL
- `DATABASE_URL` = Path to database file

---

## ❓ Troubleshooting

**Bot not responding?**
- ✅ Verify webhook is set (visit the URL above)
- ✅ Check Vercel deployment logs
- ✅ Make sure domain is correct

**Webhook errors?**
- Check Vercel logs: `vercel logs --follow`
- Make sure `/api/webhook` route exists in `vercel.json`

**Database errors?**
- Vercel's `/tmp` directory clears on redeploy
- Use Vercel's PostgreSQL or create a persistent storage solution

---

## 📊 Project Structure

```
.
├── 2v3.py                 ← Local polling bot (keep for testing)
├── api/
│   └── webhook.py        ← Vercel's serverless function
├── api.json              ← 234 APIs
├── fusion_premium.db     ← SQLite database
├── vercel.json           ← Vercel config
├── requirements.txt      ← Dependencies
├── deploy.sh            ← Bash deployment script
├── setup_deploy.py      ← Python setup helper
└── README.md            ← Documentation
```

---

## 🚀 Advanced: Use GitHub Actions for Auto-Deploy

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Vercel
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: vercel/action@master
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

Get your tokens from Vercel Dashboard and add them to GitHub Secrets.

---

## ✅ You're All Set!

Your bot is now:
- ✅ Version controlled (Git)
- ✅ Deployed globally (Vercel)  
- ✅ Live 24/7 (Serverless)
- ✅ Completely FREE (No premium)

**Happy botting! 🎉**
