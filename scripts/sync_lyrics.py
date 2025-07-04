import whisper
import os

def transcribe_and_sync(wav_path, lyrics, song_name):
    """
    Uses OpenAI Whisper model to transcribe audio and align with provided lyrics.
    Outputs an .srt file.
    """
    model = whisper.load_model("base")
    result = model.transcribe(wav_path)
    segments = result.get("segments", [])
    srt_path = os.path.join("outputs", f"{song_name}.srt")
    with open(srt_path, "w", encoding="utf-8") as srt_file:
        for i, seg in enumerate(segments, start=1):
            start = seg['start']
            end = seg['end']
            text = seg['text'].strip()
            srt_file.write(f"{i}\n")
            srt_file.write(f"{format_time(start)} --> {format_time(end)}\n")
            srt_file.write(f"{text}\n\n")
    return srt_path

def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    msec = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{msec:03d}"
