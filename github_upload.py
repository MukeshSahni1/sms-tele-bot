#!/usr/bin/env python3
"""
🚀 GitHub Repository Creator & Pusher
Creates a GitHub repo and pushes your bot code
"""

import subprocess
import sys
import os
import requests

def run_cmd(cmd, description=""):
    """Run shell command"""
    if description:
        print(f"📝 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"⚠️  {result.stderr}")
            return False
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_github_repo(username, token, repo_name):
    """Create GitHub repository using API"""
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "description": "Telegram SMS/Call/WhatsApp Bomber Bot - Free & Open Source",
        "private": False,
        "auto_init": False
    }

    print("📝 Creating GitHub repository...")
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code == 201:
            print("✅ Repository created successfully!")
            return True
        elif response.status_code == 422:
            print("⚠️  Repository already exists - continuing...")
            return True
        else:
            print(f"❌ Failed to create repo: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error creating repo: {e}")
        return False

def main():
    print("\n" + "="*50)
    print("🚀 GITHUB REPOSITORY CREATOR")
    print("="*50)

    # Get credentials
    print("\n📋 GitHub Credentials:")
    username = input("   Enter GitHub username: ").strip()
    token = input("   Enter GitHub Personal Token (create at https://github.com/settings/tokens): ").strip()
    repo_name = input("   Enter repository name (default: telegram-bot): ").strip() or "telegram-bot"

    if not username or not token:
        print("❌ Username and token required!")
        return

    print(f"\n📊 Repository: {username}/{repo_name}")

    # Create repository
    if not create_github_repo(username, token, repo_name):
        print("❌ Failed to create repository")
        return

    # Configure git
    print("\n1️⃣ Configuring Git...")
    run_cmd(f'git config user.name "{username}"')
    run_cmd(f'git config user.email "{username}@users.noreply.github.com"')

    # Create remote URL
    remote_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"

    # Remove existing remote if any
    run_cmd("git remote remove origin 2>/dev/null || true")

    # Add remote
    print("\n2️⃣ Adding GitHub remote...")
    run_cmd(f'git remote add origin "{remote_url}"')

    # Switch to main branch
    print("\n3️⃣ Switching to main branch...")
    run_cmd("git branch -M main")

    # Push code
    print("\n4️⃣ Pushing code to GitHub...")
    result = run_cmd("git push -u origin main 2>&1")

    if result is not False:
        print("\n" + "="*50)
        print("✅ SUCCESS! Code uploaded to GitHub")
        print("="*50)
        print(f"\n🔗 Repository: https://github.com/{username}/{repo_name}")
        print("\n📋 Next Steps:")
        print("   1. Go to: https://vercel.com/new")
        print("   2. Sign in with GitHub")
        print("   3. Select your repository")
        print("   4. Click Deploy")
        print("   5. Copy your Vercel domain")
        print("   6. Set webhook: https://api.telegram.org/bot8736183103:AAELHZD1wr-qohEQQ0rSRXJY2-qtZzOag6g/setWebhook?url=https://YOUR-VERCEL-DOMAIN/api/webhook")
        print("\n🎉 Ready for Vercel deployment!")
    else:
        print("\n❌ Push failed. Try:")
        print("   - Check your token permissions")
        print("   - Create repo manually at https://github.com/new")
        print("   - Run: git push -u origin main")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
