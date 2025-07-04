import os

def transcribe_and_sync(wav_path, lyrics, song_name):
    # Dummy sync simulation - export dummy .srt
    srt_path = f"outputs/{song_name}.srt"
    with open(srt_path, "w") as f:
        f.write("1\n00:00:00,000 --> 00:00:05,000\n" + lyrics.splitlines()[0])
    return srt_path
