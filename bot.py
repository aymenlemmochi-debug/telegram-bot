# ====== الإعدادات ======
TOKEN = "8712330118:AAF3Wkg7Rri-_zMDp6TTuqxmb-I0lsxLMJg"
CHAT_ID = "7113805375"

# ====== المكتبات ======
import requests
import time
import os
from flask import Flask
from threading import Thread
from datetime import datetime

app = Flask(__name__)

# ====== إرسال رسالة ======
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)

# ====== جلب سعر ======
def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    return float(requests.get(url).json()["price"])

# ====== بيانات ======
def get_price_data(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=50"
    data = requests.get(url).json()
    return [float(c[4]) for c in data]

# ====== RSI ======
def calculate_rsi(prices, period=14):
    gains, losses = [], []

    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        gains.append(max(diff, 0))
        losses.append(abs(min(diff, 0)))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# ====== EMA ======
def calculate_ema(prices, period=20):
    ema = prices[0]
    k = 2 / (period + 1)

    for price in prices:
        ema = price * k + ema * (1 - k)

    return ema

# ====== الوقت ======
def get_time():
    return datetime.now().strftime("%H:%M:%S")

# ====== تحليل ======
def analyze(symbol):
    prices = get_price_data(symbol)

    rsi = calculate_rsi(prices)
    ema = calculate_ema(prices)
    last = prices[-1]

    # شروط أسهل باش يعطي صفقات أكثر
    if rsi < 40 and last > ema:
        signal = "BUY 🔥"
    elif rsi > 60 and last < ema:
        signal = "SELL 🔥"
    else:
        return None  # ما نرجع حتى شيء

    price = get_price(symbol)
    time_now = get_time()

    return f"""
📊 {symbol}
💰 السعر: {price}
⏰ الوقت: {time_now}

📢 الإشارة: {signal}
📈 RSI: {round(rsi,2)}
"""

# ====== تشغيل ======
def run_bot():
    symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "LTCUSDT"]

    while True:
        messages = []

        for symbol in symbols:
            result = analyze(symbol)
            if result:
                messages.append(result)

        if messages:
            full = "\n\n".join(messages)
            send_message(full)
            print(full)
        else:
            send_message("🚫 لا توجد صفقات الآن")

        time.sleep(60)

# ====== السيرفر ======
@app.route('/')
def home():
    return "Bot is running"

if __name__ == "__main__":
    Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
