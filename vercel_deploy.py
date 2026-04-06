#!/usr/bin/env python3
"""
🚀 VERCEL DEPLOYMENT HELPER
Guides you through Vercel deployment and sets webhook
"""

import requests
import sys

def set_webhook(vercel_domain):
    """Set Telegram webhook"""
    bot_token = "8736183103:AAELHZD1wr-qohEQQ0rSRXJY2-qtZzOag6g"
    webhook_url = f"https://{vercel_domain}/api/webhook"

    print(f"\n📡 Setting webhook to: {webhook_url}")

    try:
        response = requests.get(
            f"https://api.telegram.org/bot{bot_token}/setWebhook",
            params={"url": webhook_url},
            timeout=10
        )
        result = response.json()

        if result.get("ok"):
            print("✅ Webhook set successfully!")
            print(f"   Response: {result.get('description', 'OK')}")
            return True
        else:
            print(f"⚠️  Webhook failed: {result.get('description', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Error setting webhook: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🚀 VERCEL DEPLOYMENT HELPER")
    print("="*60)

    print("\n📋 Complete these steps:")
    print("   1. Go to: https://vercel.com/new")
    print("   2. Sign in with GitHub")
    print("   3. Select repository: MukeshSahni1/sms-tele-bot")
    print("   4. Click 'Deploy'")
    print("   5. Wait for deployment (takes ~1-2 minutes)")
    print("   6. Copy your Vercel domain (e.g., sms-tele-bot.vercel.app)")

    vercel_domain = input("\n   Enter your Vercel domain: ").strip()

    if not vercel_domain:
        print("❌ Vercel domain required!")
        return

    print(f"\n📊 Vercel Domain: {vercel_domain}")

    # Set webhook
    if set_webhook(vercel_domain):
        print("\n" + "="*60)
        print("🎉 DEPLOYMENT COMPLETE!")
        print("="*60)
        print(f"\n📊 Your Bot Info:")
        print(f"   GitHub: https://github.com/MukeshSahni1/sms-tele-bot")
        print(f"   Vercel: https://{vercel_domain}")
        print(f"   Webhook: https://{vercel_domain}/api/webhook")
        print(f"\n🤖 Test your bot:")
        print(f"   Send /start to your bot on Telegram!")
        print(f"\n✅ Your bot is now live and FREE for all users!")
    else:
        print("\n⚠️  Webhook not set. Set manually:")
        print(f"   https://api.telegram.org/bot8736183103:AAELHZD1wr-qohEQQ0rSRXJY2-qtZzOag6g/setWebhook?url=https://{vercel_domain}/api/webhook")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)