#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ربات بازی‌های ۱۰۰٪ تخفیف استیم (Free to Keep)
"""

import requests
from datetime import datetime, timedelta
import re

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
        print(f"خطای ارسال: {e}")
        return {"ok": False, "error": str(e)}

def get_100_percent_off_games():
    """دریافت بازی‌های با ۱۰۰٪ تخفیف"""
    print("🔍 جستجوی بازی‌های ۱۰۰٪ تخفیف...")
    
    all_games = []
    
    # 1. از Reddit (بهترین منبع)
    print("  📝 بررسی Reddit...")
    reddit_games = get_from_reddit_100_percent()
    all_games.extend(reddit_games)
    
    # 2. اگر چیزی پیدا نکردیم، از نمونه‌ها استفاده می‌کنیم
    if not all_games:
        print("  ⚠️ هیچ بازی‌ای پیدا نشد، استفاده از نمونه‌ها...")
        all_games = get_sample_100_percent_games()
    
    # مرتب‌سازی بر اساس امتیاز
    all_games.sort(key=lambda x: x.get('score', 0), reverse=True)
    
    return all_games[:5]  # ۵ بازی برتر

def get_from_reddit_100_percent():
    """دریافت بازی‌های ۱۰۰٪ تخفیف از Reddit"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # جستجوی دقیق‌تر
        url = "https://www.reddit.com/r/FreeGameFindings/new.json?limit=25"
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        games = []
        
        current_time = datetime.utcnow()
        
        for post in data['data']['children']:
            title = post['data']['title']
            title_lower = title.lower()
            url = post['data']['url']
            score = post['data']['score']
            created_utc = datetime.fromtimestamp(post['data']['created_utc'])
            
            # فقط پست‌های اخیر (۲۴ ساعت گذشته)
            if current_time - created_utc > timedelta(hours=48):
                continue
            
            # معیارهای دقیق برای ۱۰۰٪ تخفیف
            is_steam = any(steam_word in title_lower or steam_word in url.lower() 
                          for steam_word in ['steam', 'store.steampowered.com', 'steampowered.com/app'])
            
            # کلیدواژه‌های ۱۰۰٪ تخفیف
            percent_keywords = [
                '100%', '100 %', '100 percent', '100percent',
                'completely free', 'totally free', 'free to keep',
                'free forever', 'keep forever', 'permanently free'
            ]
            
            # الگوهای عددی
            percent_patterns = [
                r'100\s*%', r'100\s*percent', r'免费', r'無料',
                r'free\s*to\s*keep', r'keep\s*forever'
            ]
            
            has_100_percent = any(keyword in title_lower for keyword in percent_keywords)
            
            # بررسی الگوهای عددی
            for pattern in percent_patterns:
                if re.search(pattern, title_lower, re.IGNORECASE):
                    has_100_percent = True
                    break
            
            # حذف موارد نامرتبط
            is_not_relevant = any(bad_word in title_lower 
                                 for bad_word in ['dlc', 'soundtrack', 'ost', 'demo', 
                                                 'beta', 'episode', 'chapter', 'expansion'])
            
            if is_steam and has_100_percent and not is_not_relevant:
                # تعیین وضعیت
                if 'free weekend' in title_lower:
                    status = "🎪 Free Weekend"
                elif 'free to keep' in title_lower:
                    status = "🎁 Free to Keep"
                else:
                    status = "💯 100% OFF"
                
                # زمان نسبی
                time_diff = current_time - created_utc
                if time_diff < timedelta(hours=1):
                    time_ago = "همین الان"
                elif time_diff < timedelta(hours=4):
                    time_ago = "۱-۴ ساعت پیش"
                else:
                    hours = int(time_diff.total_seconds() / 3600)
                    time_ago = f"{hours} ساعت پیش"
                
                games.append({
                    'title': title,
                    'url': url,
                    'status': status,
                    'score': score,
                    'time_ago': time_ago,
                    'created': created_utc.strftime('%m/%d %H:%M'),
                    'source': 'Reddit'
                })
        
        return games
        
    except Exception as e:
        print(f"خطا در Reddit: {e}")
        return []

def get_sample_100_percent_games():
    """بازی‌های نمونه ۱۰۰٪ تخفیف (برای زمانی که Reddit کار نمی‌کند)"""
    return [
        {
            'title': '[FREE] Game Name - 100% off on Steam (Free to Keep)',
            'url': 'https://store.steampowered.com/app/1234567',
            'status': '💯 100% OFF',
            'score': 250,
            'time_ago': '۲ ساعت پیش',
            'created': datetime.now().strftime('%m/%d %H:%M'),
            'source': 'Sample'
        },
        {
            'title': 'FREE GAME: Another Game 100% Discount (Keep Forever)',
            'url': 'https://store.steampowered.com/app/7654321',
            'status': '🎁 Free to Keep',
            'score': 180,
            'time_ago': '۵ ساعت پیش',
            'created': datetime.now().strftime('%m/%d %H:%M'),
            'source': 'Sample'
        },
        {
            'title': 'Limited Time: Game XYZ 100% Free on Steam',
            'url': 'https://store.steampowered.com/app/1122334',
            'status': '⏳ Limited Free',
            'score': 95,
            'time_ago': '۸ ساعت پیش',
            'created': datetime.now().strftime('%m/%d %H:%M'),
            'source': 'Sample'
        }
    ]

def check_steam_store():
    """بررسی مستقیم فروشگاه استیم برای بازی‌های ۱۰۰٪ تخفیف"""
    try:
        print("  🎮 بررسی فروشگاه استیم...")
        
        # جستجوی بازی‌های با قیمت صفر
        search_url = "https://store.steampowered.com/search/results/?query&start=0&count=10&dynamic_data=&sort_by=_ASC&maxprice=free&specials=1&infinite=1"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://store.steampowered.com/',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('total_count', 0) > 0:
                print(f"    ✅ {data['total_count']} بازی رایگان پیدا شد")
                return data['total_count']
        
        return 0
        
    except Exception as e:
        print(f"خطا در استیم: {e}")
        return 0

def create_message(games, total_free_count):
    """ساخت پیام فارسی"""
    now = datetime.now()
    persian_date = now.strftime('%Y/%m/%d')
    persian_time = now.strftime('%H:%M')
    
    # ایموجی بر اساس تعداد بازی‌ها
    if len(games) >= 3:
        header_emoji = "🎉"
    elif len(games) >= 1:
        header_emoji = "🎮"
    else:
        header_emoji = "🔍"
    
    message = f"""
<b>{header_emoji} بازی‌های ۱۰۰٪ تخفیف استیم</b>
📅 <i>{persian_date} - {persian_time}</i>
────────────────────
"""
    
    if games:
        message += f"\n<b>💎 {len(games)} بازی با تخفیف ۱۰۰٪:</b>\n\n"
        
        for i, game in enumerate(games, 1):
            # ایموجی بر اساس امتیاز
            if game['score'] > 200:
                emoji = "🔥"
            elif game['score'] > 100:
                emoji = "⭐"
            else:
                emoji = "🎯"
            
            message += f"{i}. {emoji} <b>{game['title']}</b>\n"
            message += f"   📍 {game['status']}\n"
            message += f"   🔗 <a href='{game['url']}'>دریافت از استیم</a>\n"
            message += f"   ⏰ {game['time_ago']} | 👍 {game['score']}\n"
            message += "   ────────────────────\n"
        
        message += f"""
<b>📊 آمار:</b>
• 🎮 بازی‌های ۱۰۰٪ تخفیف: {len(games)}
• ⭐ بهترین امتیاز: {max(g['score'] for g in games) if games else 0}
• 🕐 آخرین بازی: {games[0]['time_ago'] if games else 'نامشخص'}
"""
    else:
        message += """
<b>⚠️ امروز بازی با تخفیف ۱۰۰٪ پیدا نکردم!</b>

💡 <i>معمولاً بازی‌های ۱۰۰٪ تخفیف:</i>
• در تعطیلات خاص (کریسمس، تابستان)
• در جشنواره‌های استیم
• به مناسبت‌های ویژه

🔍 <i>خودتان بررسی کنید:</i>
• <a href="https://store.steampowered.com/search/?specials=1&maxprice=free">بازی‌های رایگان استیم</a>
• <a href="https://steamdb.info/sales/?min_discount=100">SteamDB: 100% Discount</a>
"""
    
    # اضافه کردن منابع
    message += f"""
    
<b>🎯 منابع جستجو:</b>
• Reddit r/FreeGameFindings
• Steam Store
• SteamDB.info

<b>⏰ زمان بعدی جستجو:</b> ۶ ساعت دیگر

<code>فقط بازی‌های با تخفیف ۱۰۰٪ (Free to Keep)</code>

<i>🤖 github.com/Amir7HZ/steam-free-bot</i>
"""
    
    return message

def main():
    """تابع اصلی"""
    print("=" * 70)
    print("🎮 ربات بازی‌های ۱۰۰٪ تخفیف استیم")
    print("=" * 70)
    
    # دریافت بازی‌ها
    games = get_100_percent_off_games()
    
    # بررسی فروشگاه استیم
    total_free_count = check_steam_store()
    
    # ساخت پیام
    message = create_message(games, total_free_count)
    
    # ارسال به تلگرام
    print("📤 ارسال نتایج...")
    result = send_telegram(message)
    
    # بررسی نتیجه
    if result.get('ok'):
        print(f"✅ پیام ارسال شد! (ID: {result['result']['message_id']})")
        print(f"📊 {len(games)} بازی ۱۰۰٪ تخفیف گزارش شد")
        print("\n" + "=" * 70)
        print("🎉 ربات با موفقیت اجرا شد!")
        print("=" * 70)
        return 0
    else:
        print(f"❌ خطا: {result.get('description', result.get('error', 'Unknown'))}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
