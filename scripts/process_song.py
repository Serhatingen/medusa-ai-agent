import os
from scripts.sync_lyrics import transcribe_and_sync
from scripts.generate_video import generate_video
from scripts.notify_for_approval import notify_telegram

SONGS_DIR = "songs"
OUTPUT_DIR = "outputs"

# Ensure the songs and outputs directories exist
os.makedirs(SONGS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Track which songs we've already processed
PROCESSED_FILE = os.path.join(OUTPUT_DIR, "processed.txt")
processed = set()
if os.path.exists(PROCESSED_FILE):
    with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
        processed = set(line.strip() for line in f)

def process_songs():
    for filename in os.listdir(SONGS_DIR):
        if not filename.lower().endswith(".wav"):
            continue

        song_name = filename[:-4]
        if song_name in processed:
            continue

        wav_path = os.path.join(SONGS_DIR, filename)
        txt_path = os.path.join(SONGS_DIR, f"{song_name}.txt")
        if not os.path.exists(txt_path):
            print(f"Lyrics for {song_name} not found, skipping.")
            continue

        print(f"Processing {song_name}...")

        # Read lyrics from text file
        with open(txt_path, "r", encoding="utf-8") as f:
            lyrics = f.read()

        # 1. Sync lyrics to create an SRT file
        srt_path = transcribe_and_sync(wav_path, lyrics, song_name)
        # 2. Generate the video with lyrics overlay
        video_path = generate_video(wav_path, srt_path, song_name)
        # 3. Notify user via Telegram for approval
        notify_telegram(song_name, video_path)

        # Mark this song as processed
        with open(PROCESSED_FILE, "a", encoding="utf-8") as f:
            f.write(song_name + "\n")
        processed.add(song_name)
