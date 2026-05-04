from flask import Flask, jsonify

app = Flask(__name__)

DATA = {
    "balance": 1144.32,
    "trades": 284750,
    "winrate": 94
}

@app.route("/")
def home():
    return open("index.html").read()

@app.route("/data")
def data():
    return jsonify(DATA)

@app.route("/start_trade")
def trade():
    print("Trade Started")
    return "ok"

app.run(host="0.0.0.0", port=10000)
