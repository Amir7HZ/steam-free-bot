#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ربات کامل بازی‌های رایگان استیم
"""

import requests
import json
from datetime import datetime
import time

# 🔴 مقادیر خودت رو اینجا بذار
TELEGRAM_TOKEN = "68415450040:AAEplCwSigVpx2YOejWk2OZLAZf_Bwu4LgU"
TELEGRAM_CHAT_ID = "823135316"

def send_telegram(message):
    """ارسال پیام به تلگرام"""
    try:
        url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': False
        }
        response = requests.post(url, json=data, timeout=30)
        return response.json()
    except Exception as e:
        print(f"خطا در ارسال: {e}")
        return None

def get_free_games_from_reddit():
    """دریافت بازی‌های رایگان از Reddit"""
    try:
        print("🔍 در حال جستجو در Reddit...")
        
        # آدرس Reddit برای بازی‌های رایگان
        url = "https://www.reddit.com/r/FreeGameFindings/new.json?limit=15"
        headers = {'User-Agent': 'SteamFreeBot/1.0'}
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        games = []
        
        for post in data['data']['children']:
            title = post['data']['title'].lower()
            url = post['data']['url']
            
            # فقط بازی‌های استیم که رایگان هستند
            if 'steam' in title and ('free' in title or '100%' in title):
                # حذف DLCها و موارد نامرتبط
                if any(bad in title for bad in ['dlc', 'soundtrack', 'ost', 'demo', 'beta']):
                    continue
                
                games.append({
                    'title': post['data']['title'],
                    'url': url,
                    'score': post['data']['score'],
                    'created': datetime.fromtimestamp(post['data']['created_utc']).strftime('%m/%d %H:%M')
                })
                
                if len(games) >= 5:  # حداکثر ۵ بازی
                    break
        
        return games
        
    except Exception as e:
        print(f"خطا در Reddit: {e}")
        return []

def get_steam_free_games():
    """دریافت بازی‌های رایگان از استیم"""
    try:
        print("🔍 در حال جستجو در استیم...")
        
        # لیست برخی بازی‌های رایگان معروف (می‌تونی گسترش بدی)
        popular_free_games = [
            {"name": "Destiny 2", "url": "https://store.steampowered.com/app/1085660"},
            {"name": "Warframe", "url": "https://store.steampowered.com/app/230410"},
            {"name": "Apex Legends", "url": "https://store.steampowered.com/app/1172470"},
            {"name": "Dota 2", "url": "https://store.steampowered.com/app/570"},
            {"name": "Team Fortress 2", "url": "https://store.steampowered.com/app/440"}
        ]
        
        return popular_free_games[:3]  # ۳ بازی اول
        
    except Exception as e:
        print(f"خطا در استیم: {e}")
        return []

def main():
    """تابع اصلی"""
    print("=" * 60)
    print("🎮 شروع جستجوی بازی‌های رایگان استیم")
    print("=" * 60)
    
    # دریافت بازی‌ها
    reddit_games = get_free_games_from_reddit()
    steam_games = get_steam_free_games()
    
    # زمان فعلی
    now = datetime.now()
    persian_date = now.strftime('%Y/%m/%d')
    persian_time = now.strftime('%H:%M')
    
    # ساخت پیام
    message = f"""
<b>🎮 بازی‌های رایگان استیم</b>
📅 <i>{persian_date} - {persian_time}</i>
────────────────────
"""
    
    if reddit_games:
        message += f"\n<b>🆓 بازی‌های رایگان جدید:</b>\n\n"
        for i, game in enumerate(reddit_games, 1):
            emoji = "🔥" if game['score'] > 100 else "🎮"
            message += f"{i}. {emoji} <b>{game['title']}</b>\n"
            message += f"   🔗 <a href='{game['url']}'>لینک بازی</a>\n"
            message += f"   ⏰ {game['created']} | 👍 {game['score']}\n"
            message += "   ────────────────────\n"
    
    elif steam_games:
        message += f"\n<b>⭐ بازی‌های رایگان محبوب:</b>\n\n"
        for i, game in enumerate(steam_games, 1):
            message += f"{i}. 🎮 <b>{game['name']}</b>\n"
            message += f"   🔗 <a href='{game['url']}'>صفحه استیم</a>\n"
            message += "   ────────────────────\n"
    
    else:
        message += """
<b>⚠️ امروز بازی رایگان جدیدی پیدا نکردم!</b>

💡 <i>پیشنهادات:</i>
• خودتان بررسی کنید: 
  <a href="https://store.steampowered.com/search/?maxprice=free">بازی‌های رایگان استیم</a>
• عضو Reddit شوید:
  <a href="https://www.reddit.com/r/FreeGameFindings/">r/FreeGameFindings</a>
"""
    
    # اضافه کردن فوتر
    message += f"""
    
<b>📊 اطلاعات ربات:</b>
• ⏰ اجرای بعدی: ۶ ساعت دیگر
• 🔄 وضعیت: فعال
• 📱 دریافت کننده: شما

<code>هر ۶ ساعت به صورت خودکار جستجو می‌کند.</code>
"""
    
    # ارسال پیام
    print("📤 ارسال نتایج به تلگرام...")
    result = send_telegram(message)
    
    if result and result.get('ok'):
        print(f"✅ پیام ارسال شد! (ID: {result['result']['message_id']})")
        print("\n" + "=" * 60)
        print("🎉 ربات با موفقیت اجرا شد!")
        print("=" * 60)
    else:
        print("❌ خطا در ارسال پیام!")
    
    return 0

if __name__ == "__main__":
    main()
