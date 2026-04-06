#!/usr/bin/env python3
"""
🚀 Automated Telegram Bot Deployment to Vercel + GitHub
Run this to automatically deploy your bot!
"""

import subprocess
import sys
import json
import os

def run_command(cmd, description=""):
    """Run shell command and return output"""
    if description:
        print(f"\n📝 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return False
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_tool(tool_name):
    """Check if a tool is installed"""
    result = subprocess.run(f"which {tool_name}", shell=True, capture_output=True)
    return result.returncode == 0

def main():
    print("\n" + "="*50)
    print("🚀 TELEGRAM BOT AUTO-DEPLOY")
    print("="*50)
    
    BOT_TOKEN = "8736183103:AAELHZD1wr-qohEQQ0rSRXJY2-qtZzOag6g"
    
    print("\n✅ Checking prerequisites...")
    
    if not check_tool("git"):
        print("❌ Git not found!")
        return
    
    print("   ✅ Git found")
    
    # GitHub Setup
    print("\n1️⃣ GitHub Setup")
    print("-" * 50)
    
    github_user = input("   Enter your GitHub username: ").strip()
    repo_name = input("   Enter repository name (e.g., telegram-bot): ").strip()
    
    if not github_user or not repo_name:
        print("❌ GitHub credentials required!")
        return
    
    print(f"   📝 Repository: {github_user}/{repo_name}")
    print("   ⚠️  Make sure to manually create the repo on GitHub first")
    print(f"   Then run: git remote add origin https://github.com/{github_user}/{repo_name}.git")
    print("            git push -u origin main")
    
    # Vercel Setup
    print("\n2️⃣ Vercel Setup")
    print("-" * 50)
    
    vercel_domain = input("   Enter your Vercel domain (e.g., my-bot.vercel.app): ").strip()
    
    if not vercel_domain:
        print("❌ Vercel domain required!")
        return
    
    # Set Webhook
    print("\n3️⃣ Setting Telegram Webhook")
    print("-" * 50)
    
    webhook_url = f"https://{vercel_domain}/api/webhook"
    print(f"   📡 Webhook URL: {webhook_url}")
    print(f"   🔗 Visit this URL to set webhook:")
    print(f"   https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}")
    
    # Success
    print("\n" + "="*50)
    print("✅ SETUP COMPLETE!")
    print("="*50)
    print(f"\n📚 Next Steps:")
    print(f"   1. Create repo on GitHub (https://github.com/new)")
    print(f"   2. Clone it and copy these files there")
    print(f"   3. Deploy to Vercel (https://vercel.com/new)")
    print(f"   4. Visit webhook URL above to activate bot")
    print(f"\n✅ Your bot is ready for deployment!")
    print("")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
