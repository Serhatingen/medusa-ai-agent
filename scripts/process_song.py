import os
from scripts.sync_lyrics import transcribe_and_sync
from scripts.generate_video import generate_video
from scripts.notify_for_approval import notify_telegram

SONGS_DIR = "songs"
OUTPUT_DIR = "outputs"

def process_songs():
    for filename in os.listdir(SONGS_DIR):
        if filename.endswith(".wav"):
            song_name = filename[:-4]
            txt_path = os.path.join(SONGS_DIR, f"{song_name}.txt")
            wav_path = os.path.join(SONGS_DIR, filename)
            if not os.path.exists(txt_path):
                continue

            print(f"Processing {song_name}")
            lyrics = open(txt_path).read()
            srt_path = transcribe_and_sync(wav_path, lyrics, song_name)
            video_path = generate_video(wav_path, srt_path, song_name)
            notify_telegram(song_name, video_path)
