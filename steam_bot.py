#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ربات استیم - نسخه مستقیم (بدون نیاز به Variables/Secrets)
"""

import requests
from datetime import datetime

print("=" * 70)
print("🤖 STEAM FREE GAMES BOT - DIRECT VERSION")
print("=" * 70)

# 🔴 🔴 🔴 اینجا مقادیر خودت رو وارد کن 🔴 🔴 🔴
TELEGRAM_TOKEN = "8415450040:AAEplCwSigVpx2YOejWk2OZLAZf_Bwu4LgU"
TELEGRAM_CHAT_ID = "823135316"
# 🔴 🔴 🔴 🔴 🔴 🔴 🔴 🔴 🔴 🔴 🔴 🔴 🔴 🔴 🔴

print(f"\n🔑 توکن: {TELEGRAM_TOKEN[:15]}..." if TELEGRAM_TOKEN else "❌ توکن تنظیم نشده")
print(f"👤 آیدی: {TELEGRAM_CHAT_ID}" if TELEGRAM_CHAT_ID else "❌ آیدی تنظیم نشده")

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    print("\n❌ لطفاً مقادیر بالا را در کد پر کنید!")
    exit(1)

# ==================== تست اتصال ====================
print("\n📡 تست اتصال به تلگرام...")

try:
    test_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe"
    response = requests.get(test_url, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            print(f"✅ اتصال موفق! ربات: @{data['result']['username']}")
        else:
            print(f"❌ توکن مشکل دارد: {data.get('description')}")
            exit(1)
    else:
        print(f"❌ خطای HTTP: {response.status_code}")
        exit(1)
        
except Exception as e:
    print(f"⚠️ خطا: {e}")
    exit(1)

# ==================== ارسال پیام ====================
print("\n📤 ارسال پیام...")

try:
    now = datetime.now()
    date_str = now.strftime('%Y/%m/%d')
    time_str = now.strftime('%H:%M')
    
    message = f"""
<b>🎮 ربات استیم فعال شد!</b>

✅ <i>بدون نیاز به Variables/Secrets</i>

📅 <b>تاریخ:</b> {date_str}
⏰ <b>ساعت:</b> {time_str}
🤖 <b>نوع:</b> مستقیم (Hardcoded)

✨ <b>ویژگی‌ها:</b>
• 🔍 بررسی خودکار بازی‌های رایگان
• ⏰ هر ۶ ساعت اجرا می‌شود
• 📱 اطلاع به همین تلگرام
• 💰 کاملاً رایگان
• ⚡ بدون دردسر Variables

🕐 <b>اولین جستجو:</b> ۶ ساعت دیگر

<code>مقادیر مستقیماً در کد قرار دارند</code>

<i>آسان‌ترین روش ممکن!</i>
"""
    
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML',
        'disable_web_page_preview': False
    }
    
    response = requests.post(url, json=payload, timeout=30)
    result = response.json()
    
    if result.get('ok'):
        print("✅ پیام ارسال شد!")
        print(f"📨 Message ID: {result['result']['message_id']}")
        
        print("\n" + "=" * 70)
        print("🎉 🎉 🎉 موفقیت کامل! 🎉 🎉 🎉")
        print("=" * 70)
        print("\n📱 به تلگرام برو و پیام رو ببین!")
        print("🤖 ربات هر ۶ ساعت خودکار اجرا می‌شه.")
        
    else:
        print(f"❌ خطا: {result.get('description')}")
        
except Exception as e:
    print(f"⚠️ خطا: {e}")

print("\n" + "=" * 70)
print("✅ کار تمام شد!")
print("=" * 70)
