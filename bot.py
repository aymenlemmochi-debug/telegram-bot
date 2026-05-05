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

# ====== جلب سعر مباشر ======
def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    res = requests.get(url).json()
    return float(res["price"])

# ====== جلب بيانات ======
def get_price_data(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=50"
    data = requests.get(url).json()
    closes = [float(candle[4]) for candle in data]
    return closes

# ====== RSI ======
def calculate_rsi(prices, period=14):
    gains, losses = [], []

    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        if diff > 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(diff))

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

# ====== تحليل ======
def get_signal(symbol):
    prices = get_price_data(symbol)

    rsi = calculate_rsi(prices)
    ema = calculate_ema(prices)
    last_price = prices[-1]

    if rsi < 30 and last_price > ema:
        return "BUY 🔥 قوي"

    elif rsi > 70 and last_price < ema:
        return "SELL 🔥 قوي"

    return "WAIT ⏳"

# ====== الوقت ======
def get_time():
    return datetime.now().strftime("%H:%M:%S")

# ====== تشغيل ======
last_signals = {}

def run_bot():
    global last_signals

    symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "LTCUSDT"]

    while True:
        for symbol in symbols:
            signal = get_signal(symbol)
            price = get_price(symbol)
            time_now = get_time()

            # منع التكرار
            if last_signals.get(symbol) != signal:
                message = f"""
📊 {symbol}
💰 السعر: {price}
⏰ الوقت: {time_now}

📢 الإشارة: {signal}
"""
                send_message(message)
                print(message)

                last_signals[symbol] = signal

        time.sleep(60)

# ====== السيرفر ======
@app.route('/')
def home():
    return "Bot is running"

if __name__ == "__main__":
    Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
