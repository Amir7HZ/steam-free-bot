#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ربات بازی‌های ۱۰۰٪ تخفیف استیم - نسخه اصلاح شده با API واقعی
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

def get_real_100_off_games():
    """
    دریافت واقعی بازی‌های ۱۰۰٪ تخفیف از API استیم
    با استفاده از پارامترهای دقیق لینک شما
    """
    print("🔍 در حال دریافت لیست واقعی از API استیم...")

    try:
        # پارامترهای مهم از لینک شما:
        # maxprice=free (رایگان)
        # specials=1 (تخفیف‌های ویژه)
        # ndl=1 (احتمالاً برای جلوگیری از کش)
        url = "https://store.steampowered.com/search/results/"
        
        # پارامترهای پرس و جو (Query Parameters)
        params = {
            'query': '',  # رشته جستجوی خالی
            'start': 0,   # شروع از آیتم صفرم
            'count': 50,  # تعداد آیتم‌های درخواستی (می‌توانید افزایش دهید)
            'dynamic_data': '',
            'sort_by': '_ASC',
            'maxprice': 'free',  # فیلتر اصلی: قیمت حداکثر رایگان
            'specials': 1,       # فیلتر اصلی: فقط تخفیف‌های ویژه
            'supportedlang': 'english',
            'ndl': 1,
            'snr': '1_7_7_240_7',
            'infinite': 1
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://store.steampowered.com/search/?maxprice=free&specials=1'
        }

        response = requests.get(url, params=params, headers=headers, timeout=25)
        
        if response.status_code != 200:
            print(f"❌ خطا از سمت استیم! کد وضعیت: {response.status_code}")
            return []

        data = response.json()
        
        # بررسی وجود نتایج
        if not data.get('results_html') or data.get('total_count') == 0:
            print("⚠️ API استیم پاسخ داد، اما بازی‌ای یافت نشد.")
            return []

        total_games = data.get('total_count', 0)
        print(f"✅ API استیم پاسخ داد. در کل {total_games} آیتم رایگان/تخفیف‌خورده یافت شد.")

        # تجزیه HTML نتایج
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(data['results_html'], 'html.parser')
        
        games_found = []
        game_rows = soup.find_all('a', class_='search_result_row')

        for row in game_rows:
            # استخراج نام بازی
            title_elem = row.find('span', class_='title')
            if not title_elem:
                continue
            game_name = title_elem.text.strip()

            # استخراج آدرس و App ID
            game_url = row.get('href', '')
            data_ds_appid = row.get('data-ds-appid', '')
            app_id = data_ds_appid.split(',')[0] if data_ds_appid else ''

            # بررسی درصد تخفیف
            discount_block = row.find('div', class_='search_discount')
            discount_text = discount_block.text.strip() if discount_block else "0%"
            
            # استخراج عدد تخفیف (مثلاً از "-100%" عدد 100 را بگیر)
            import re
            discount_match = re.search(r'(\d+)%', discount_text)
            discount_percent = int(discount_match.group(1)) if discount_match else 0

            # فقط بازی‌های با ۱۰۰٪ تخفیف را نگه دار
            if discount_percent == 100:
                # استخراج قیمت‌ها (برای اطمینان)
                price_block = row.find('div', class_='search_price')
                price_text = price_block.text.strip() if price_block else ""
                
                games_found.append({
                    'name': game_name,
                    'app_id': app_id,
                    'discount': discount_percent,
                    'url': game_url,
                    'price_text': price_text,
                    'type': '💯 100% OFF'
                })

        print(f"🎮 از بین آنها، {len(games_found)} بازی با تخفیف ۱۰۰٪ شناسایی شد.")
        return games_found

    except requests.exceptions.Timeout:
        print("⏳ زمان درخواست به استیم به پایان رسید.")
        return []
    except Exception as e:
        print(f"⚠️ یک خطای غیرمنتظره رخ داد: {e}")
        return []

def create_message(games_list):
    """ساخت پیام فارسی"""
    now = datetime.now()
    persian_date = now.strftime('%Y/%m/%d')
    persian_time = now.strftime('%H:%M')
    
    message = f"""
<b>💯 فهرست بازی‌های ۱۰۰٪ تخفیف استیم</b>
🕐 بروزرسانی: {persian_date} - {persian_time}
🔗 <i>منبع: فیلتر مستقیم فروشگاه استیم</i>
────────────────────
"""
    
    if games_list:
        # ممکن است بازی‌های Free-to-Play نیز در نتایج باشند، آنها را جدا کنید
        true_100_off = [g for g in games_list if "Free" not in g.get('price_text', '')]
        free_to_play = [g for g in games_list if "Free" in g.get('price_text', '')]

        if true_100_off:
            message += f"\n<b>🎁 بازی‌های با تخفیف ۱۰۰٪ (قیمت اصلی داشتند):</b>\n\n"
            for i, game in enumerate(true_100_off[:10], 1):  # حداکثر ۱۰ مورد
                steam_link = f"https://store.steampowered.com/app/{game['app_id']}/" if game['app_id'] else game['url']
                message += f"{i}. <b>{game['name']}</b>\n"
                message += f"   🔗 <a href='{steam_link}'>مشاهده در استیم</a>\n"
                message += f"   ⚡ قیمت نهایی: <b>رایگان</b>\n"
                message += "   ────────────────────\n"

        # اگر فقط بازی Free-to-Play یافت شد
        if not true_100_off and free_to_play:
            message += f"\n<b>⚠️ امروز بازی با تخفیف ۱۰۰٪ یافت نشد، اما این بازی‌های رایگان دائم موجودند:</b>\n\n"
            for i, game in enumerate(free_to_play[:5], 1):
                steam_link = f"https://store.steampowered.com/app/{game['app_id']}/" if game['app_id'] else game['url']
                message += f"{i}. <b>{game['name']}</b>\n"
                message += f"   🔗 <a href='{steam_link}'>صفحه استیم</a>\n"
                message += "   ────────────────────\n"
            message += "\n<i>نکته: اینها بازی‌های Free-to-Play هستند که همیشه رایگان‌اند، نه تخفیف موقت.</i>\n"
    else:
        message += """
<b>🔍 امروز بازی با تخفیف ۱۰۰٪ یافت نشد.</b>

💡 توضیح:
• این ربات اکنون مستقیماً از فیلترهای فروشگاه استیم استفاده می‌کند.
• ممکن است واقعاً در لحظهٔ بررسی، بازی فعال با تخفیف ۱۰۰٪ موجود نباشد.
• بازی‌های Free-to-Play (همیشه رایگان) در این شمارش نمی‌آیند.
"""

    # پاورقی
    message += f"""
    
📌 <b>نکات فنی:</b>
• داده‌ها مستقیماً از API داخلی استیم دریافت شده.
• فیلترها: maxprice=free & specials=1
• زمان بررسی بعدی: ۳ ساعت دیگر

<code>با هر اجرا، آخرین وضعیت فروشگاه بررسی می‌شود.</code>
"""
    return message

def main():
    """تابع اصلی"""
    print("=" * 70)
    print("🔄 ربات در حال بررسی مستقیم فروشگاه استیم...")
    print("=" * 70)
    
    games = get_real_100_off_games()
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
