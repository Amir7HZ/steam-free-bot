#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ربات بازی‌های ۱۰۰٪ تخفیف استیم - نسخه نهایی و دقیق
منبع: API رسمی بخش Specials استیم
"""

import requests
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

def get_steam_specials_100_off():
    """
    دریافت بازی‌های ۱۰۰٪ تخفیف از API رسمی بخش Specials استیم
    این API دقیقاً همان اطلاعاتی را برمی‌گرداند که در بخش 'ویژه‌ها' می‌بینید.
    """
    print("🎮 در حال دریافت لیست ویژه‌های استیم...")

    try:
        # API اصلی بخش ویژه‌های استیم
        url = "https://store.steampowered.com/api/featuredcategories"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        response = requests.get(url, headers=headers, timeout=25)

        if response.status_code != 200:
            print(f"❌ خطا در ارتباط با استیم! کد وضعیت: {response.status_code}")
            return []

        data = response.json()

        # بازی‌ها در کلید 'specials' قرار دارند
        if 'specials' not in data or 'items' not in data['specials']:
            print("⚠️ بخش ویژه‌ها در پاسخ API یافت نشد.")
            return []

        all_specials = data['specials']['items']
        print(f"✅ {len(all_specials)} آیتم در بخش ویژه‌های استیم یافت شد.")

        games_found = []

        for game in all_specials:
            # شرط اصلی: تخفیف دقیقاً ۱۰۰٪ و قیمت نهایی صفر
            discount = game.get('discount_percent', 0)
            final_price = game.get('final_price', 999)  # قیمت به سنت (یا واحد پایه)
            original_price = game.get('original_price', 0)

            if discount == 100 and final_price == 0:
                # اطمینان از این که بازی Free-to-Play همیشگی نیست (قیمت اصلی داشت)
                if original_price > 0:
                    games_found.append({
                        'name': game.get('name', 'نامشخص'),
                        'app_id': game.get('id'),
                        'discount': discount,
                        'original_price_cents': original_price,
                        'original_price_formatted': f"${original_price / 100:.2f}",
                        'header_image': game.get('header_image', ''),
                        'type': '💯 100% OFF'
                    })

        print(f"🎯 از بین آنها، {len(games_found)} بازی با تخفیف واقعی ۱۰۰٪ شناسایی شد.")
        return games_found

    except requests.exceptions.Timeout:
        print("⏳ زمان درخواست به پایان رسید.")
        return []
    except Exception as e:
        print(f"⚠️ خطا در پردازش داده‌های استیم: {e}")
        return []

def create_message(games_list):
    """ساخت پیام فارسی"""
    now = datetime.now()
    persian_date = now.strftime('%Y/%m/%d')
    persian_time = now.strftime('%H:%M')

    message = f"""
<b>🔥 بازی‌های با تخفیف ۱۰۰٪ استیم</b>
📅 بروزرسانی: {persian_date} - {persian_time}
🏪 منبع: <i>بخش ویژه‌های استیم (Specials)</i>
────────────────────
"""

    if games_list:
        message += f"\n<b>💰 {len(games_list)} بازی رایگان برای همیشه:</b>\n\n"

        for i, game in enumerate(games_list, 1):
            steam_link = f"https://store.steampowered.com/app/{game['app_id']}/"
            message += f"{i}. <b>{game['name']}</b>\n"
            message += f"   🔗 <a href='{steam_link}'>دریافت از استیم</a>\n"
            message += f"   📉 قیمت اصلی: <s>{game['original_price_formatted']}</s> → <b>رایگان!</b>\n"
            message += "   ────────────────────\n"

        message += f"""
<b>📊 جمع‌بندی فوری:</b>
• تعداد بازی‌های رایگان: {len(games_list)}
• میانگین قیمت اصلی: ${sum(g['original_price_cents'] for g in games_list) / len(games_list) / 100:.2f}
"""
    else:
        message += """
<b>🔍 امروز بازی با تخفیف ۱۰۰٪ یافت نشد.</b>

💡 توضیح:
• این ربات مستقیماً به بخش «ویژه‌های استیم» متصل می‌شود.
• اگر بازی‌ای با قیمت اصلی بالاتر از صفر و قیمت نهایی صفر وجود داشته باشد، نمایش داده می‌شود.
• ممکن است در لحظهٔ بررسی، چنین تخفیفی فعال نباشد.
"""

    # پاورقی
    message += f"""
    
⚙️ <b>اطلاعات فنی:</b>
• API مورد استفاده: <code>store.steampowered.com/api/featuredcategories</code>
• فیلتر دقیق: <code>discount_percent == 100 && final_price == 0</code>
• بررسی بعدی: ۲ ساعت دیگر

<code>این گزارش تنها بازی‌های موقتاً رایگان (Free to Keep) را نشان می‌دهد.</code>
"""
    return message

def main():
    """تابع اصلی"""
    print("=" * 70)
    print("🔄 ربات در حال بررسی بخش ویژه‌های استیم...")
    print("=" * 70)

    games = get_steam_specials_100_off()
    message = create_message(games)

    print("📤 در حال ارسال گزارش به تلگرام...")
    result = send_telegram(message)

    if result.get('ok'):
        print("✅ گزارش با موفقیت ارسال شد!")
        print("=" * 70)
        return 0
    else:
        error_msg = result.get('description') or result.get('error', 'خطای نامشخص')
        print(f"❌ خطا در ارسال به تلگرام: {error_msg}")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    exit(main())
