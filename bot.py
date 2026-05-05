# ====== الإعدادات ======
TOKEN = "8712330118:AAF3Wkg7Rri-_zMDp6TTuqxmb-I0lsxLMJg"
CHAT_ID = "7113805375"

# ====== المكتبات ======
import requests
import time
import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

# ====== إرسال رسالة ======
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)

# ====== جلب بيانات من Binance ======
def get_price_data(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=50"
    data = requests.get(url).json()
    closes = [float(candle[4]) for candle in data]
    return closes

# ====== حساب RSI ======
def calculate_rsi(prices, period=14):
    gains = []
    losses = []

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

# ====== حساب EMA ======
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

    # BUY
    if rsi < 30 and last_price > ema:
        return f"{symbol} BUY 🔥 RSI={round(rsi,2)}"

    # SELL
    elif rsi > 70 and last_price < ema:
        return f"{symbol} SELL 🔥 RSI={round(rsi,2)}"

    return f"{symbol} WAIT ⏳ RSI={round(rsi,2)}"

# ====== تشغيل ======
last_signal = ""

def run_bot():
    global last_signal

    symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "LTCUSDT"]

    while True:
        for symbol in symbols:
            signal = get_signal(symbol)

            if signal != last_signal:
                send_message(signal)
                print(signal)
                last_signal = signal

        time.sleep(60)

# ====== السيرفر ======
@app.route('/')
def home():
    return "Bot is running"

if __name__ == "__main__":
    Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
last_signal = ""

def run_bot():
    global last_signal
    while True:
        signal = get_signal()

        if signal != last_signal:
            send_message(signal)
            last_signal = signal

        time.sleep(60)
def get_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    res = requests.get(url).json()
    return res["price"]
from datetime import datetime

def get_time():
    return datetime.now().strftime("%H:%M:%S")
