import os
import numpy as np
from moviepy.editor import AudioFileClip, VideoClip
from moviepy.video.io.bindings import PIL_to_npimage
from PIL import Image, ImageDraw, ImageFont

def generate_video(wav_path, srt_path, song_name):
    """
    Creates a vertical video with bass-reactive background and timed lyrics overlay.
    """
    # Load audio and clip duration (first 20s for chorus)
    duration = 20
    audio = AudioFileClip(wav_path).subclip(0, duration)
    # Prepare audio samples for RMS
    samples = audio.to_soundarray(fps=44100).mean(axis=1)
    fps = 24
    frame_size = int(44100 / fps)
    rms = [np.sqrt((samples[i:i+frame_size]**2).mean()) for i in range(0, len(samples), frame_size)]
    import numpy as np
    rms = np.array(rms)
    rms = rms / rms.max()

    # Load SRT cues
    cues = []
    with open(srt_path, encoding="utf-8") as f:
        blocks = f.read().strip().split("\n\n")
        for block in blocks:
            parts = block.split("\n")
            if len(parts) >= 3:
                _, times, text = parts[0], parts[1], " ".join(parts[2:])
                start, _ = times.split(" --> ")
                cues.append((parse_timestamp(start), text))

    # Video settings
    size = (1080, 1920)
    font = ImageFont.truetype("arial.ttf", 80)

    def make_frame(t):
        idx = min(int(t * fps), len(rms)-1)
        intensity = rms[idx]
        r = int(75 * (1 - intensity))
        g = 0
        b = int(130 * (1 - intensity))
        img = Image.new("RGB", size, (r, g, b))
        draw = ImageDraw.Draw(img)
        # Draw lyrics if cue matches
        for start, text in cues:
            if abs(t - start) < 2:
                w, h = draw.textsize(text, font=font)
                draw.text(((size[0]-w)/2, size[1]*0.8), text, font=font, fill=(255,255,255))
        return PIL_to_npimage(img)

    video = VideoClip(make_frame, duration=duration).set_audio(audio)
    output_path = os.path.join("outputs", f"{song_name}.mp4")
    video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=fps)
    return output_path

def parse_timestamp(ts):
    time, ms = ts.split(",")
    h, m, s = map(int, time.split(":"))
    return h*3600 + m*60 + s + int(ms)/1000
