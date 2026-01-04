#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ربات استیم - نسخه سازگار با Variables و Secrets
"""

import os
import sys
import requests
from datetime import datetime

print("=" * 70)
print("🤖 STEAM FREE GAMES BOT - VARIABLES MODE")
print("=" * 70)

# ==================== دریافت از Variables یا Secrets ====================
# اول از Variables بخون، اگر نبود از Secrets
TOKEN = os.getenv('TELEGRAM_TOKEN') or os.getenv('BOT_TOKEN') or os.getenv('TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID') or os.getenv('CHAT_ID') or os.getenv('USER_ID')

print("\n🔍 جستجوی متغیرها (Variables & Secrets):")

# لیست همه متغیرهای محیطی مرتبط
print("\n📋 همه متغیرهای محیطی مرتبط:")
for key, value in sorted(os.environ.items()):
    key_upper = key.upper()
    if any(word in key_upper for word in ['TELEGRAM', 'TOKEN', 'CHAT', 'BOT', 'USER']):
        # برای امنیت، توکن رو کامل نمایش نده
        if 'TOKEN' in key_upper:
            display_value = f"{value[:10]}...[مخفی]..." if value else "خالی"
        else:
            display_value = value or "خالی"
        print(f"  {key}: {display_value}")

print(f"\n📊 نتیجه نهایی:")
print(f"توکن انتخاب شده: {'✅ پیدا شد' if TOKEN else '❌ پیدا نشد'}")
print(f"آیدی انتخاب شده: {'✅ پیدا شد' if CHAT_ID else '❌ پیدا نشد'}")

if TOKEN:
    print(f"  طول توکن: {len(TOKEN)} کاراکتر")
if CHAT_ID:
    print(f"  آیدی: {CHAT_ID}")

# ==================== اگر پیدا نشد ====================
if not TOKEN or not CHAT_ID:
    print("\n" + "=" * 70)
    print("❌ خطا: متغیرها پیدا نشدند!")
    print("\n💡 راه‌حل‌های ممکن:")
    print("\n1. اگر از Variables استفاده می‌کنید:")
    print("   به این آدرس بروید:")
    print("   https://github.com/Amir7HZ/steam-free-bot/settings/variables/actions")
    print("   دو Variable اضافه کنید:")
    print("   - Name: TELEGRAM_TOKEN")
    print("   - Name: TELEGRAM_CHAT_ID")
    
    print("\n2. یا در فایل workflow.yml اینطور تنظیم کنید:")
    print("   env:")
    print("     TELEGRAM_TOKEN: \${{ vars.TELEGRAM_TOKEN }}")
    print("     TELEGRAM_CHAT_ID: \${{ vars.TELEGRAM_CHAT_ID }}")
    
    print("\n3. اگر از Secrets استفاده می‌کنید:")
    print("   https://github.com/Amir7HZ/steam-free-bot/settings/secrets/actions")
    print("   و Secrets رو اضافه کنید.")
    print("=" * 70)
    sys.exit(1)

# ==================== تست اتصال ====================
print("\n" + "=" * 70)
print("📡 تست اتصال به تلگرام...")

try:
    test_url = f"https://api.telegram.org/bot{TOKEN}/getMe"
    response = requests.get(test_url, timeout=10)
    
    if response.status_code == 401:
        print("❌ خطای 401: توکن نامعتبر یا منقضی شده!")
        print("   لطفاً توکن جدید از @BotFather بگیرید.")
        sys.exit(1)
    elif response.status_code == 404:
        print("❌ خطای 404: توکن اشتباه است!")
        sys.exit(1)
    elif response.status_code != 200:
        print(f"❌ خطای HTTP: {response.status_code}")
        sys.exit(1)
    
    data = response.json()
    if data.get('ok'):
        bot_name = data['result']['first_name']
        bot_username = data['result']['username']
        print(f"✅ اتصال موفق!")
        print(f"   🤖 نام ربات: {bot_name}")
        print(f"   📛 کاربری: @{bot_username}")
    else:
        print(f"❌ پاسخ نامعتبر: {data}")
        sys.exit(1)
        
except Exception as e:
    print(f"⚠️ خطا در اتصال: {e}")
    sys.exit(1)

# ==================== ارسال پیام ====================
print("\n" + "=" * 70)
print("📤 ارسال پیام...")

try:
    now = datetime.now()
    date_str = now.strftime('%Y/%m/%d')
    time_str = now.strftime('%H:%M')
    
    message = f"""
<b>🎮 ربات استیم - GitHub Actions</b>

✅ <i>راه‌اندازی موفقیت‌آمیز</i>

📅 <b>تاریخ:</b> {date_str}
⏰ <b>ساعت:</b> {time_str} (ایران)
🏗️ <b>نوع:</b> Variables Mode

✨ <b>ویژگی‌ها:</b>
• 🔍 جستجوی خودکار بازی‌های رایگان
• ⏰ اجرای هر ۶ ساعت
• 📱 اطلاع‌رسانی به تلگرام
• 💰 کاملاً رایگان
• ⚡ بدون سرور

🔗 <b>لینک‌های مفید:</b>
• <a href="https://store.steampowered.com/search/?maxprice=free">بازی‌های رایگان استیم</a>
• <a href="https://www.reddit.com/r/FreeGameFindings/">Reddit Free Games</a>

🕐 <b>اولین جستجو:</b> ۶ ساعت دیگر

<code>تایید شده با Variables/Secrets</code>

<i>github.com/Amir7HZ/steam-free-bot</i>
"""
    
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML',
        'disable_web_page_preview': False
    }
    
    print("در حال ارسال...")
    response = requests.post(url, json=payload, timeout=30)
    result = response.json()
    
    if result.get('ok'):
        print("✅ پیام ارسال شد!")
        print(f"   📨 Message ID: {result['result']['message_id']}")
        print(f"   👤 به: {result['result']['chat']['id']}")
        
        print("\n" + "=" * 70)
        print("🎉 🎉 🎉 موفقیت کامل! 🎉 🎉 🎉")
        print("=" * 70)
        print("\n📱 اکنون به تلگرام خود بروید.")
        print("🤖 ربات هر ۶ ساعت خودکار اجرا می‌شود.")
        print("⚙️ نوع: Variables Mode")
        
    else:
        print(f"❌ خطا: {result.get('description')}")
        sys.exit(1)
        
except Exception as e:
    print(f"⚠️ خطا: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ ربات با موفقیت اجرا شد!")
print("=" * 70)
sys.exit(0)
