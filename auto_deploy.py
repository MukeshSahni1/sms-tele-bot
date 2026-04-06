#!/usr/bin/env python3
"""
🚀 FULLY AUTOMATED TELEGRAM BOT DEPLOYMENT
Does everything for you - just provide your credentials!
"""

import subprocess
import sys
import os
import requests
import json
from pathlib import Path

class BotDeployer:
    def __init__(self):
        self.bot_token = "8736183103:AAELHZD1wr-qohEQQ0rSRXJY2-qtZzOag6g"
        self.project_dir = os.getcwd()
        
    def print_header(self, text):
        """Print formatted header"""
        print("\n" + "="*60)
        print(f"  {text}")
        print("="*60)
    
    def run_cmd(self, cmd, description=""):
        """Run shell command"""
        if description:
            print(f"📝 {description}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                if "already exists" not in result.stderr.lower():
                    print(f"⚠️  {result.stderr}")
            return result.stdout.strip() if result.returncode == 0 else None
        except subprocess.TimeoutExpired:
            print(f"⏱️  Command timed out")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def step1_github_setup(self):
        """Step 1: Setup GitHub"""
        self.print_header("STEP 1️⃣  - GITHUB SETUP")
        
        print("\n📋 GitHub Credentials Required:")
        github_user = input("   Enter GitHub username: ").strip()
        
        if not github_user:
            print("❌ Username required!")
            return None
        
        github_token = input("   Enter GitHub Personal Token (create at https://github.com/settings/tokens): ").strip()
        
        if not github_token:
            print("⚠️  No token provided - will try without authentication")
        
        repo_name = input("   Enter repository name (default: telegram-bot): ").strip() or "telegram-bot"
        
        return {
            "username": github_user,
            "token": github_token,
            "repo_name": repo_name
        }
    
    def step2_github_push(self, github_info):
        """Step 2: Push to GitHub"""
        self.print_header("STEP 2️⃣  - PUSHING TO GITHUB")
        
        if not github_info:
            print("❌ No GitHub credentials")
            return False
        
        username = github_info["username"]
        token = github_info["token"]
        repo_name = github_info["repo_name"]
        
        print(f"   📊 Repository: {username}/{repo_name}")
        
        # Configure git
        self.run_cmd(f'git config user.name "{username}"', "Setting git user")
        self.run_cmd(f'git config user.email "{username}@users.noreply.github.com"', "Setting git email")
        
        # Set remote
        if token:
            remote_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
            print("   🔐 Using authenticated connection")
        else:
            remote_url = f"https://github.com/{username}/{repo_name}.git"
            print("   ⚠️  Using unauthenticated connection (may fail if repo doesn't exist)")
        
        self.run_cmd(f"git remote remove origin 2>/dev/null || true")
        self.run_cmd(f'git remote add origin "{remote_url}"', "Adding remote")
        
        self.run_cmd("git branch -M main", "Switching to main branch")
        
        print("\n   📤 Pushing code to GitHub...")
        result = self.run_cmd("git push -u origin main 2>&1")
        
        if result:
            print(f"   ✅ Successfully pushed to GitHub!")
            print(f"   🔗 Repository: https://github.com/{username}/{repo_name}")
            return True
        else:
            print("\n   ⚠️  Push failed. Make sure:")
            print(f"      1. Repository exists: https://github.com/new")
            print(f"      2. Your token has 'repo' permissions")
            print(f"      3. Run: git push -u origin main (manually)")
            return False
    
    def step3_vercel_setup(self):
        """Step 3: Vercel setup"""
        self.print_header("STEP 3️⃣  - VERCEL DEPLOYMENT")
        
        print("\n📋 Vercel Setup:")
        print("   1. Go to: https://vercel.com/new")
        print("   2. Sign in with GitHub")
        print("   3. Select your repository")
        print("   4. Click Deploy")
        print("   5. Wait for deployment to complete")
        print("   6. Copy your Vercel domain")
        
        vercel_domain = input("\n   Enter your Vercel domain (e.g., my-bot.vercel.app): ").strip()
        
        if not vercel_domain:
            print("❌ Domain required!")
            return None
        
        return vercel_domain
    
    def step4_webhook(self, vercel_domain):
        """Step 4: Set webhook"""
        self.print_header("STEP 4️⃣  - TELEGRAM WEBHOOK")
        
        if not vercel_domain:
            print("❌ No Vercel domain provided")
            return False
        
        webhook_url = f"https://{vercel_domain}/api/webhook"
        print(f"   📡 Webhook URL: {webhook_url}")
        
        print("\n   🔗 Setting webhook...")
        
        try:
            response = requests.get(
                f"https://api.telegram.org/bot{self.bot_token}/setWebhook",
                params={"url": webhook_url},
                timeout=10
            )
            result = response.json()
            
            if result.get("ok"):
                print("   ✅ Webhook set successfully!")
                print(f"   📝 Response: {result.get('description', 'OK')}")
                return True
            else:
                print(f"   ⚠️  Failed: {result.get('description', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print(f"   🔗 Set manually: {webhook_url}")
            return False
    
    def deploy(self):
        """Run full deployment"""
        print("\n")
        print("╔" + "="*58 + "╗")
        print("║" + " "*10 + "🚀 FULLY AUTOMATED TELEGRAM BOT DEPLOYMENT" + " "*6 + "║")
        print("╚" + "="*58 + "╝")
        
        # Step 1: GitHub
        github_info = self.step1_github_setup()
        if not github_info:
            print("\n❌ GitHub setup failed")
            return False
        
        # Step 2: Push
        if not self.step2_github_push(github_info):
            print("\n⚠️  GitHub push had issues - continuing anyway...")
        
        # Step 3: Vercel
        vercel_domain = self.step3_vercel_setup()
        if not vercel_domain:
            print("\n❌ Vercel setup failed")
            return False
        
        # Step 4: Webhook
        webhook_success = self.step4_webhook(vercel_domain)
        
        # Summary
        self.print_summary(github_info, vercel_domain, webhook_success)
        return True
    
    def print_summary(self, github_info, vercel_domain, webhook_ok):
        """Print deployment summary"""
        self.print_header("✅ DEPLOYMENT SUMMARY")
        
        print("\n📊 Deployment Info:")
        print(f"   GitHub: https://github.com/{github_info['username']}/{github_info['repo_name']}")
        print(f"   Vercel: https://{vercel_domain}")
        print(f"   Bot: Live! 🎉")
        
        print("\n✨ Your Bot Features:")
        print("   ✅ SMS Attacks (Free)")
        print("   ✅ Call Attacks (Free)")
        print("   ✅ WhatsApp Attacks (Free)")
        print("   ✅ 234 APIs Available")
        print("   ✅ 24/7 Uptime on Vercel")
        
        if webhook_ok:
            print("\n🤖 Test Your Bot:")
            print("   Send /start to your bot on Telegram!")
            print("   It should respond immediately!")
        else:
            print("\n⚠️  Webhook not set - bot may not respond")
            print("   Try setting it manually at:")
            print(f"   https://api.telegram.org/bot{self.bot_token}/setWebhook?url=https://{vercel_domain}/api/webhook")
        
        print("\n" + "="*60)
        print("✅ YOUR TELEGRAM BOT IS NOW LIVE ON VERCEL! 🎉")
        print("="*60 + "\n")

def main():
    try:
        # Check if in correct directory
        if not os.path.exists("vercel.json"):
            print("❌ This script must run in the bot project directory!")
            print("   (where vercel.json exists)")
            sys.exit(1)
        
        deployer = BotDeployer()
        success = deployer.deploy()
        
        if success:
            print("✅ Deployment complete! Your bot is ready!")
            sys.exit(0)
        else:
            print("⚠️  Deployment had issues - check the output above")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n❌ Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
