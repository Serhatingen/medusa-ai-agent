def generate_video(wav_path, srt_path, song_name):
    # Dummy path for now
    video_path = f"outputs/{song_name}.mp4"
    open(video_path, "wb").write(b"")  # Empty dummy file
    return video_path
