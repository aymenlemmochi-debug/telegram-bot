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

# ====== دالة إرسال رسالة ======
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)

# ====== إشارات بسيطة (تجريب) ======
def get_signal():
    import random
    signals = [
        "BUY 🔥 قوي",
        "SELL 🔥 قوي",
        "WAIT ⏳ لا تدخل"
    ]
    return random.choice(signals)

# ====== تشغيل البوت ======
def run_bot():
    while True:
        signal = get_signal()
        send_message(signal)
        print("Sent:", signal)
        time.sleep(10)  # كل 10 ثواني

# ====== ويب سيرفر (باش يبقى شغال) ======
@app
