#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ربات بازی‌های با تخفیف ۱۰۰٪ استیم (Free to Keep NOW)
"""

import requests
import json
from datetime import datetime

# 🔴 اطلاعات شما
TELEGRAM_TOKEN = "8415450040:AAEk23aNy-o6tNGPSDq-T6Ka7IxH1w7yW4A"
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
        return {"ok": False, "error": str(e)}

def get_100_percent_discount_games():
    """دریافت بازی‌های با ۱۰۰٪ تخفیف از API استیم"""
    print("🔍 جستجوی بازی‌های با ۱۰۰٪ تخفیف در استیم...")
    
    try:
        # API استیم برای بازی‌های با تخفیف
        url = "https://store.steampowered.com/api/featuredcategories"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://store.steampowered.com/'
        }
        
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code != 200:
            print(f"❌ خطای API استیم: {response.status_code}")
            return []
        
        data = response.json()
        games = []
        
        # بررسی بخش "specials" (تخفیف‌ها)
        if 'specials' in data:
            specials = data['specials']['items']
            
            for game in specials:
                discount = game.get('discount_percent', 0)
                final_price = game.get('final_price', 999)
                original_price = game.get('original_price', 1000)
                
                # فقط بازی‌هایی با ۱۰۰٪ تخفیف و قیمت نهایی ۰
                if discount == 100 and final_price == 0:
                    games.append({
                        'name': game.get('name', 'Unknown'),
                        'app_id': game.get('id'),
                        'discount': discount,
                        'original_price': original_price / 100,  # تبدیل به تومان/دلار
                        'final_price': final_price,
                        'header_image': game.get('header_image', ''),
                        'type': '100% OFF'
                    })
        
        print(f"✅ {len(games)} بازی با ۱۰۰٪ تخفیف پیدا شد")
        return games[:10]  # حداکثر ۱۰ بازی
        
    except Exception as e:
        print(f"⚠️ خطا در دریافت از استیم: {e}")
        return []

def get_free_to_keep_from_search():
    """جستجوی مستقیم بازی‌های Free to Keep"""
    print("🔍 جستجوی Free to Keep...")
    
    try:
        # جستجوی بازی‌های با قیمت ۰
        search_url = "https://store.steampowered.com/search/results/?query&start=0&count=20&dynamic_data=&sort_by=_ASC&maxprice=free&specials=1&infinite=1"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://store.steampowered.com/search/?maxprice=free&specials=1'
        }
        
        response = requests.get(search_url, headers=headers, timeout=20)
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        games = []
        
        if data.get('total_count', 0) > 0:
            # HTML بازی‌ها را پارس کن
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(data['results_html'], 'html.parser')
            items = soup.find_all('a', {'class': 'search_result_row'})
            
            for item in items[:15]:  # 15 بازی اول
                title = item.get('data-search-title', '')
                app_id = item.get('data-ds-appid', '')
                discount = item.find('div', {'class': 'search_discount'})
                
                if discount and '100%' in discount.text:
                    price = item.find('div', {'class': 'search_price'})
                    
                    games.append({
                        'name': title,
                        'app_id': app_id,
                        'discount': 100,
                        'type': 'FREE TO KEEP'
                    })
        
        return games
        
    except Exception as e:
        print(f"⚠️ خطا در جستجو: {e}")
        return []

def create_message(api_games, search_games):
    """ساخت پیام فارسی فقط برای بازی‌های ۱۰۰٪ تخفیف"""
    now = datetime.now()
    persian_date = now.strftime('%Y/%m/%d')
    persian_time = now.strftime('%H:%M')
    
    # ترکیب بازی‌ها
    all_games = api_games + search_games
    
    # حذف تکراری‌ها
    unique_games = []
    seen_names = set()
    
    for game in all_games:
        if game['name'] not in seen_names:
            seen_names.add(game['name'])
            unique_games.append(game)
    
    # مرتب‌سازی
    unique_games = unique_games[:8]  # 8 بازی اول
    
    message = f"""
<b>💯 بازی‌های با ۱۰۰٪ تخفیف استیم</b>
💰 <i>فقط Free to Keep - قابل اضافه کردن به کتابخانه</i>
📅 {persian_date} - ⏰ {persian_time}
────────────────────
"""
    
    if unique_games:
        message += f"\n<b>🎮 {len(unique_games)} بازی با تخفیف ۱۰۰٪:</b>\n\n"
        
        for i, game in enumerate(unique_games, 1):
            message += f"{i}. <b>{game['name']}</b>\n"
            
            # لینک مستقیم به استیم
            if game.get('app_id'):
                steam_url = f"https://store.steampowered.com/app/{game['app_id']}/"
                message += f"   🔗 <a href='{steam_url}'>دریافت از استیم</a>\n"
            
            # قیمت‌ها
            if game.get('original_price'):
                message += f"   📉 قبل: ${game['original_price']} → الان: <b>رایگان</b>\n"
            else:
                message += f"   🎁 وضعیت: <b>Free to Keep</b>\n"
            
            message += f"   ⚡ تخفیف: <b>۱۰۰٪</b>\n"
            message += "   ────────────────────\n"
        
        message += f"""
<b>📊 جمع‌بندی:</b>
• 💰 قیمت همه: <b>رایگان</b>
• ⏰ زمان فعلی: {persian_time}
• 🎮 قابل اضافه‌کردن به کتابخانه: <b>بله</b>
"""
    else:
        message += """
<b>⚠️ امروز هیچ بازی با ۱۰۰٪ تخفیف پیدا نکردم!</b>

💡 <i>معمولاً بازی‌های ۱۰۰٪ تخفیف در این مواقع ظاهر می‌شوند:</i>
• جشنواره‌های بزرگ استیم (Summer/Winter Sale)
• آخر هفته‌های خاص
• مناسبت‌های ویژه شرکت‌ها

🔍 <i>خودتان بررسی کنید:</i>
• <a href="https://store.steampowered.com/search/?maxprice=free&specials=1">لیست بازی‌های رایگان استیم</a>
• <a href="https://steamdb.info/sales/?min_discount=100">SteamDB: 100% Discount</a>
"""
    
    # اضافه کردن منابع
    message += f"""
    
<b>🎯 منابع بررسی:</b>
• Steam Store API
• Steam Specials Page
• Real-time Search

<b>⏰ بررسی بعدی:</b> ۳ ساعت دیگر
<code>فقط بازی‌های ۱۰۰٪ تخفیف (Free to Keep)</code>

<i>🤖 ربات اختصاصی ۱۰۰٪ تخفیف</i>
"""
    
    return message, len(unique_games)

def main():
    """تابع اصلی"""
    print("=" * 70)
    print("💯 ربات بازی‌های ۱۰۰٪ تخفیف استیم (Free to Keep)")
    print("=" * 70)
    
    # دریافت از API استیم
    print("🔍 دریافت از Steam API...")
    api_games = get_100_percent_discount_games()
    
    # دریافت از جستجو
    print("🔍 جستجوی مستقیم...")
    search_games = get_free_to_keep_from_search()
    
    # ساخت پیام
    message, game_count = create_message(api_games, search_games)
    
    # ارسال
    print(f"📤 ارسال {game_count} بازی ۱۰۰٪ تخفیف...")
    result = send_telegram(message)
    
    if result.get('ok'):
        print(f"✅ {game_count} بازی ۱۰۰٪ تخفیف گزارش شد!")
        print("\n" + "=" * 70)
        print("🎉 ربات با موفقیت اجرا شد!")
        print("=" * 70)
        return 0
    else:
        print(f"❌ خطا: {result.get('description', result.get('error', 'Unknown'))}")
        return 1

if __name__ == "__main__":
    exit(main())
