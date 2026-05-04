import os
import time
from flask import Flask
from threading import Thread

app = Flask(__name__)

# الصفحة الرئيسية (باش Render ما يطفيش)
@app.route('/')
def home():
    return "Bot is running!"

# دالة الإشارة
def get_signal(rsi, ema20, ema50, macd, price):

    if 45 < rsi < 55:
        return "WAIT ⏳ سوق ضعيف"

    buy_score = 0
    sell_score = 0

    # شروط BUY
    if rsi > 55:
        buy_score += 1
    if ema20 > ema50:
        buy_score += 1
    if macd > 0:
        buy_score += 1
    if price > ema20:
        buy_score += 1

    # شروط SELL
    if rsi < 45:
        sell_score += 1
    if ema20 < ema50:
        sell_score += 1
    if macd < 0:
        sell_score += 1
    if price < ema20:
        sell_score += 1

    # القرار
    if buy_score >= 4:
        return "BUY 🔥 قوي"
    elif buy_score == 3:
        return "BUY ⚡ متوسط"

    if sell_score >= 4:
        return "SELL 🔥 قوي"
    elif sell_score == 3:
        return "SELL ⚡ متوسط"

    return "WAIT ⏳ لا تدخل"

# تشغيل البوت في Loop
def run_bot():
    while True:
        # مثال تجريبي (بدلهم لاحقاً ببيانات حقيقية)
        signal = get_signal(60, 100, 90, 1, 110)
        print(signal)

        time.sleep(10)  # كل 10 ثواني

# تشغيل الاثنين مع بعض
if __name__ == "__main__":
    Thread(target=run_bot).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
