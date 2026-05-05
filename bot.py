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

# ====== إشارات بسيطة ======
import random

def get_signal():
    buy_score = random.randint(0, 5)
    sell_score = random.randint(0, 5)

    if buy_score >= 3:
        return "BUY 🔥 قوي"
    elif buy_score == 2:
        return "BUY ⚡ متوسط"

    if sell_score >= 3:
        return "SELL 🔥 قوي"
    elif sell_score == 2:
        return "SELL ⚡ متوسط"

    return "WAIT ⏳ لا تدخل"

# ====== تشغيل البوت ======
def run_bot():
    while True:
        signal = get_signal()
        send_message(signal)
        print(signal)
        time.sleep(10)

# ====== السيرفر ======
@app.route('/')
def home():
    return "Bot is running"

if __name__ == "__main__":
    Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
