#!/usr/bin/env python3
"""
ربات بازی‌های ۱۰۰٪ تخفیف استیم - نسخه نهایی و تمیز
"""

import requests
from bs4 import BeautifulSoup

# 🔴 تنظیمات شما
BOT_TOKEN = "8415450040:AAEk23aNy-o6tNGPSDq-T6Ka7IxH1w7yW4A"
CHAT_ID = "823135316"

def get_steam_game_names():
    """دریافت فقط اسم بازی‌ها (بدون DLC) از لینک شما"""
    url = "https://store.steampowered.com/search/results/"
    
    # پارامترهای دقیق از لینک شما
    params = {
        'query': '',
        'start': 0,
        'count': 30,
        'dynamic_data': '',
        'sort_by': '_ASC',
        'maxprice': 'free',
        'category1': '998',          # فقط بازی‌ها (نه DLC)
        'supportedlang': 'english',
        'specials': 1,
        'ndl': 1,
        'snr': '1_7_7_240_7',
        'infinite': 1
    }
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        data = response.json()
        
        soup = BeautifulSoup(data['results_html'], 'html.parser')
        game_names = []
        
        for item in soup.find_all('a', class_='search_result_row'):
            # فقط بازی‌های اصلی (حذف DLC)
            title_elem = item.find('span', class_='title')
            if title_elem:
                name = title_elem.text.strip()
                
                # فیلتر DLC (اگر اسم شامل این کلمات بود حذف کن)
                dlc_keywords = ['dlc', 'soundtrack', 'ost', 'expansion', 'pack']
                if not any(keyword in name.lower() for keyword in dlc_keywords):
                    game_names.append(name)
        
        return game_names
        
    except Exception as e:
        print(f"خطا: {e}")
        return []

def send_to_telegram(names):
    """ارسال با فرمت زیبا به تلگرام"""
    if not names:
        message = "⚠️ امروز بازی با تخفیف ۱۰۰٪ پیدا نکردم"
    else:
        message = "🎮 **بازی‌های ۱۰۰٪ تخفیف امروز**\n\n"
        message += "━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for i, name in enumerate(names[:12], 1):  # فقط ۱۲ بازی اول
            message += f"**{i}. {name}**\n"
            message += "➖➖➖➖➖➖➖➖➖\n"
        
        if len(names) > 12:
            message += f"\nو {len(names) - 12} بازی دیگر..."
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        requests.post(url, json=data, timeout=10)
        print(f"✅ {len(names)} بازی به تلگرام ارسال شد")
    except Exception as e:
        print(f"❌ خطا در ارسال: {e}")

def main():
    """تابع اصلی"""
    print("🔍 در حال جستجو در استیم...")
    games = get_steam_game_names()
    
    if games:
        print(f"✅ {len(games)} بازی پیدا شد:")
        for name in games[:5]:
            print(f"   • {name}")
        if len(games) > 5:
            print(f"   ... و {len(games) - 5} بازی دیگر")
    else:
        print("⚠️ بازی‌ای پیدا نشد")
    
    print("📤 ارسال به تلگرام...")
    send_to_telegram(games)
    print("🎉 کار تمام شد!")

if __name__ == "__main__":
    main()
