#!/usr/bin/env python3
"""
🚀 GitHub Code Pusher
Pushes your bot code to an existing GitHub repository
"""

import subprocess
import sys
import os

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

def main():
    print("\n" + "="*50)
    print("🚀 GITHUB CODE PUSHER")
    print("="*50)

    print("\n📋 First, create a repository on GitHub:")
    print("   1. Go to: https://github.com/new")
    print("   2. Name it: sms-tele-bot")
    print("   3. Make it Public")
    print("   4. Click 'Create repository'")
    print("   5. Copy the repository URL")

    input("\n   Press Enter when you've created the repository...")

    # Get repository URL
    repo_url = input("\n   Paste your GitHub repository URL: ").strip()

    if not repo_url:
        print("❌ Repository URL required!")
        return

    print(f"\n📊 Repository: {repo_url}")

    # Configure git
    print("\n1️⃣ Configuring Git...")
    run_cmd('git config user.name "Bot Deployer"')
    run_cmd('git config user.email "bot@example.com"')

    # Remove existing remote if any
    run_cmd("git remote remove origin 2>/dev/null || true")

    # Add remote
    print("\n2️⃣ Adding GitHub remote...")
    run_cmd(f'git remote add origin "{repo_url}"')

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
        print(f"\n🔗 Repository: {repo_url}")
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
        print("   - Check repository URL")
        print("   - Make sure you have push access")
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