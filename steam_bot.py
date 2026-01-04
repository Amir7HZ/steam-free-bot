#!/usr/bin/env python3
import requests

# 🔴 اطلاعات ربات خودت اینجا بذار
BOT_TOKEN = "8415450040:AAEk23aNy-o6tNGPSDq-T6Ka7IxH1w7yW4A"
CHAT_ID = "823135316"

def get_steam_game_names():
    """فقط اسم بازی‌ها رو از لینک استیم می‌گیره"""
    url = "https://store.steampowered.com/search/results/"
    
    params = {
        'query': '',
        'start': 0,
        'count': 50,
        'maxprice': 'free',
        'specials': 1,
        'snr': '1_7_7_240_7',
        'infinite': 1
    }
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        # استخراج HTML و پیدا کردن اسم بازی‌ها
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(data['results_html'], 'html.parser')
        
        game_names = []
        for item in soup.find_all('span', class_='title'):
            game_names.append(item.text.strip())
        
        return game_names
        
    except:
        return ["خطا در دریافت"]

def send_to_telegram(names):
    """اسم بازی‌ها رو به تلگرام می‌فرسته"""
    if not names:
        message = "⚠️ امروز بازی با تخفیف 100% نیست"
    else:
        message = "🎮 بازی‌های 100% تخفیف امروز:\n\n" + "\n".join(names[:15])  # فقط 15 بازی اول
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, json=data)

# اجرای اصلی
if __name__ == "__main__":
    print("🔍 در حال بررسی استیم...")
    games = get_steam_game_names()
    print(f"✅ {len(games)} بازی پیدا شد")
    
    if games:
        for name in games[:5]:  # نمایش 5 بازی اول در کنسول
            print(f"• {name}")
    
    print("📤 در حال ارسال به تلگرام...")
    send_to_telegram(games)
    print("✅ ارسال شد")
