#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ربات بازی‌های رایگان استیم
فایل اصلی: steam_bot.py
"""

import os
import sys
import requests
import json
from datetime import datetime

print("=" * 60)
print("🎮 STEAM FREE GAMES BOT - GitHub Actions")
print("=" * 60)

# دریافت تنظیمات از Environment Variables
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

print(f"🔑 توکن: {'✅ موجود' if TOKEN else '❌ مفقود'}")
print(f"👤 آیدی: {CHAT_ID or '❌ مفقود'}")

if not TOKEN or not CHAT_ID:
    print("""
❌ خطا: تنظیمات کامل نیست!
لطفاً در GitHub:
1. به Settings → Secrets → Actions بروید
2. دو Secret اضافه کنید:
   - TELEGRAM_TOKEN: توکن ربات تلگرام
   - TELEGRAM_CHAT_ID: آیدی عددی شما
""")
    sys.exit(1)

def send_telegram_message(text, parse_mode='HTML'):
    """ارسال پیام به تلگرام"""
    try:
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        
        # اگر متن طولانی است، کوتاه کن
        if len(text) > 4000:
            text = text[:4000] + "\n\n📝 [متن کامل نمایش داده نشد]"
        
        data = {
            'chat_id': CHAT_ID,
            'text': text,
            'parse_mode': parse_mode,
            'disable_web_page_preview': False
        }
        
        print("📤 در حال ارسال پیام به تلگرام...")
        response = requests.post(url, json=data, timeout=30)
        result = response.json()
        
        if result.get('ok'):
            print(f"✅ پیام ارسال شد! (Message ID: {result['result']['message_id']})")
            return True
        else:
            print(f"❌ خطای تلگرام: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"⚠️ خطا در ارسال: {e}")
        return False

def get_current_time():
    """دریافت زمان فعلی به فارسی"""
    now = datetime.now()
    return {
        'date': now.strftime('%Y/%m/%d'),
        'time': now.strftime('%H:%M'),
        'full': now.strftime('%Y/%m/%d %H:%M:%S')
    }

def create_welcome_message():
    """ساخت پیام خوش‌آمدگویی"""
    time_info = get_current_time()
    
    message = f"""
<b>🎮 ربات بازی‌های رایگان استیم</b>

✅ <i>با موفقیت راه‌اندازی شد!</i>

📅 <b>تاریخ راه‌اندازی:</b> {time_info['date']}
⏰ <b>ساعت:</b> {time_info['time']} (ایران)
🤖 <b>پلتفرم:</b> GitHub Actions

✨ <b>ویژگی‌های ربات:</b>
• 🔍 بررسی خودکار بازی‌های رایگان
• ⏰ اجرای هر ۶ ساعت
• 📱 اطلاع‌رسانی به تلگرام
• 💰 کاملاً رایگان

🕐 <b>برنامه زمانی:</b>
• هر ۶ ساعت: جستجوی بازی‌های جدید
• اولین جستجو: ۶ ساعت دیگر
• حالت دستی: همیشه قابل اجرا

🔗 <b>لینک‌های مفید:</b>
• <a href="https://store.steampowered.com/search/?maxprice=free">بازی‌های رایگان استیم</a>
• <a href="https://www.reddit.com/r/FreeGameFindings/">Reddit Free Games</a>
• <a href="https://steamdb.info/free/">SteamDB Free Games</a>

<code>ربات به صورت خودکار مدیریت می‌شود. نیاز به هیچ اقدام دیگری نیست.</code>

<i>با ❤️ توسط شما روی GitHub Actions</i>
"""
    
    return message

def main():
    """تابع اصلی"""
    print("\n🔧 شروع فرآیند اجرا...")
    
    # دریافت بازی‌های رایگان (فعلاً پیام تست)
    print("🔍 در حال بررسی بازی‌های رایگان...")
    
    # ساخت پیام
    message = create_welcome_message()
    
    # ارسال به تلگرام
    print("📨 آماده‌سازی پیام برای ارسال...")
    success = send_telegram_message(message)
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 ربات با موفقیت اجرا شد!")
        print("📱 به تلگرام خود بروید و پیام را بررسی کنید.")
        print("=" * 60)
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ خطا در اجرای ربات!")
        print("⚠️ لطفاً تنظیمات را بررسی کنید.")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
