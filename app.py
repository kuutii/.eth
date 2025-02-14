import os
from dotenv import load_dotenv

load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 設定（LINEとDiscordの情報をここに入れる）
LINE_CHANNEL_ACCESS_TOKEN = "MoiY4JNIiTHs1wKEyMm1Q76mZRrJqcG1rT+ObRfjuqc7cNSHV9rahzflU679Ydi7dslbnGa9WZGimvH0OaVx8Wn0uE8/LVDEIoDTDhLZoSWICzPz+5Luh62zsLUycY4TOSXGSF04Viq2mEBhic/yeAdB04t89/1O/w1cDnyilFU="  # LINE Botのアクセストークン
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1339946657646907423/hF1xtimi0sLfvypeq1DqlJRgXV4zXTghc6HMuRMsY12GrijyTO5Vqp5ctWEIl5BoH4EF"  # Discord Webhook URL

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
