import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import requests

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からLINEとDiscordの情報を読み込む
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

app = Flask(__name__)

# LINEのメッセージをDiscordに送信する関数
def send_to_discord(message):
    """LINEのメッセージをDiscordに送信"""
    data = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=data)

@app.route("/webhook", methods=["POST"])
def webhook():
    """LINEのWebhookを受信し、Discordへメッセージを転送"""
    data = request.json

    # ユーザーが送信したメッセージを取得
    for event in data.get("events", []):
        if event["type"] == "message" and "text" in event["message"]:
            user_message = event["message"]["text"]
            send_to_discord(f"LINEからのメッセージ: {user_message}")

    return jsonify({"status": "ok"})

@app.route("/")
def home():
    """ホームページにアクセスされた場合"""
    return "Hello, Render!"

if __name__ == "__main__":
    # RenderがPORTを指定してくれるので、それを使う
    port = int(os.environ.get("PORT", 5000))  # PORT環境変数が設定されている場合、それを使用
    app.run(host="0.0.0.0", port=port)  # すべてのIPアドレスからアクセス可能
