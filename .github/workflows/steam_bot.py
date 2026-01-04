#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ربات اطلاع‌رسانی بازی‌های رایگان استیم
GitHub Actions Version
"""

import os
import requests
import json
import sys
from datetime import datetime
from urllib.parse import quote

# تنظیمات از Environment Variables
TELEGRAM_TOKEN = os.getenv('8415450040:AAEplCwSigVpx2YOejWk2OZLAZf_Bwu4LgU')
CHAT_ID = os.getenv('823135316')

if not TELEGRAM_TOKEN or not CHAT_ID:
    print("❌ خطا: TELEGRAM_TOKEN یا CHAT_ID تنظیم نشده!")
    print("لطفاً در GitHub Secrets تنظیم کنید.")
    sys.exit(1)

def send_telegram_message(text, parse_mode='HTML'):
    """ارسال پیام به تلگرام"""
    try:
        url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
        
        # اگر متن خیلی طولانی است، کوتاهش کن
        if len(text) > 4000:
            text = text[:4000] + "\n\n📝 متن کامل در لینک بالا..."
        
        data = {
            'chat_id': CHAT_ID,
            'text': text,
            'parse_mode': parse_mode,
            'disable_web_page_preview': False
        }
        
        response = requests.post(url, json=data, timeout=30)
        result = response.json()
        
        if result.get('ok'):
            print(f"✅ پیام ارسال شد: {result['result']['message_id']}")
            return True
        else:
            print(f"❌ خطای تلگرام: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"⚠️ خطا در ارسال به تلگرام: {e}")
        return False

def get_free_games_from_reddit():
    """دریافت بازی‌های رایگان از Reddit"""
    print("🔍 در حال دریافت از Reddit...")
    
    try:
        url = "https://www.reddit.com/r/FreeGameFindings/new.json?limit=15"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Steam-Bot/1.0'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"⚠️ خطا از Reddit: {response.status_code}")
            return []
        
        data = response.json()
        games = []
        
        for post in data['data']['children']:
            title = post['data']['title'].lower()
            url = post['data']['url']
            
            # فیلتر کردن: فقط پست‌های مربوط به Steam
            is_steam = any(keyword in title for keyword in ['steam', 'استیم'])
            is_free = any(keyword in title for keyword in ['free', 'رایگان', '100%', 'giveaway'])
            not_dlc = all(keyword not in title for keyword in ['dlc', 'soundtrack', 'ost', 'demo'])
            
            if is_steam and is_free and not_dlc:
                games.append({
                    'title': post['data']['title'],
                    'url': url,
                    'created': datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y/%m/%d %H:%M'),
                    'score': post['data']['score']
                })
                
                if len(games) >= 5:  # حداکثر ۵ بازی
                    break
        
        print(f"✅ {len(games)} بازی از Reddit پیدا شد")
        return games
        
    except Exception as e:
        print(f"⚠️ خطا در دریافت از Reddit: {e}")
        return []

def get_steam_free_games():
    """دریافت بازی‌های رایگان از استیم"""
    print("🔍 در حال دریافت از استیم...")
    
    try:
        # جستجوی بازی‌های رایگان در استیم
        url = "https://store.steampowered.com/search/results/?query&start=0&count=10&dynamic_data=&sort_by=_ASC&maxprice=free&snr=1_7_7_7000_7&specials=1&infinite=1"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://store.steampowered.com/',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('total_count', 0) > 0:
                print(f"✅ {data['total_count']} بازی رایگان در استیم")
                # اینجا می‌توانی HTML را پارس کنی
                return data.get('total_count', 0)
        
        return 0
        
    except Exception as e:
        print(f"⚠️ خطا در دریافت از استیم: {e}")
        return 0

def main():
    """تابع اصلی"""
    print("=" * 60)
    print("🎮 STEAM FREE GAMES BOT - GITHUB ACTIONS")
    print("=" * 60)
    
    # دریافت زمان فعلی
    now_iran = datetime.now().strftime('%Y/%m/%d - %H:%M')
    now_utc = datetime.utcnow().strftime('%H:%M UTC')
    
    # دریافت بازی‌ها
    reddit_games = get_free_games_from_reddit()
    steam_count = get_steam_free_games()
    
    # ساخت پیام
    message = f"""
<b>🎮 بازی‌های رایگان استیم</b>
📅 <i>{now_iran} (ایران)</i>
⏰ <i>{now_utc} (UTC)</i>
────────────────────

"""
    
    if reddit_games:
        message += f"<b>🆓 {len(reddit_games)} بازی رایگان پیدا شد:</b>\n\n"
        
        for i, game in enumerate(reddit_games, 1):
            # ایموجی بر اساس امتیاز پست
            emoji = "🔥" if game['score'] > 100 else "⭐" if game['score'] > 50 else "🎮"
            message += f"{i}. {emoji} <b>{game['title']}</b>\n"
            message += f"   🔗 <a href='{game['url']}'>لینک بازی</a>\n"
            message += f"   ⏰ {game['created']} | 👍 {game['score']}\n"
            message += "   ────────────────────\n"
    
    else:
        message += """
<b>⚠️ امروز بازی رایگان جدیدی پیدا نکردم!</b>

💡 <i>ممکنه:</i>
• امروز بازی رایگانی نباشه
• Reddit در دسترس نباشه
• نیاز به صبر داشته باشیم

🔍 <i>می‌تونی خودت چک کنی:</i>
https://store.steampowered.com/search/?maxprice=free
"""
    
    # اضافه کردن آمار
    message += f"""
    
<b>📊 آمار:</b>
• بازی‌های Reddit: {len(reddit_games)}
• بازی‌های رایگان استیم: {steam_count}
• زمان بعدی بررسی: ۶ ساعت دیگر

<b>🔔 نکته:</b>
این ربات هر ۶ ساعت به صورت خودکار اجرا می‌شه و بازی‌های رایگان رو برات پیدا می‌کنه.

<i>با ❤️ توسط GitHub Actions</i>
    """
    
    # ارسال پیام
    print("📤 در حال ارسال پیام به تلگرام...")
    success = send_telegram_message(message)
    
    if success:
        print("✅ ربات با موفقیت اجرا شد!")
        return 0
    else:
        print("❌ خطا در اجرای ربات!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
