import os
import requests

def notify_telegram(song_name, video_path):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Telegram config eksik")
        return

    with open(video_path, "rb") as vid:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendVideo",
            data={"chat_id": chat_id, "caption": f"🎬 Video hazır: {song_name}\nOnaylıyor musun?"},
            files={"video": vid}
        )
    print(f"Notification gönderildi: {song_name}")
