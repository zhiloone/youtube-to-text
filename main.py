import os
from pytubefix import YouTube
from pydub import AudioSegment
import assemblyai as aai

from settings import settings

def download_youtube_audio(url, output_folder="downloads"):
    """Downloads a YouTube video and extracts audio as MP3."""
    yt = YouTube(url)
    video_title = yt.title.replace(" ", "_").replace("/", "_")  # Ensure safe filename
    audio_stream = yt.streams.filter(only_audio=True).first()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    mp4_filename = f"{video_title}.mp4"
    audio_path = os.path.join(output_folder, mp4_filename)
    mp3_path = os.path.join(output_folder, f"{video_title}.mp3")

    print(f"Downloading: {yt.title}...")

    # Explicitly set the output path and filename
    audio_stream.download(output_path=output_folder, filename=mp4_filename)

    # Convert to MP3
    print("Converting to MP3...")
    audio = AudioSegment.from_file(audio_path)
    audio.export(mp3_path, format="mp3")
    os.remove(audio_path)  # Clean up original file

    return mp3_path

def transcribe_audio(file_path):
    """Uploads an MP3 file to AssemblyAI and returns the transcription."""
    aai.settings.api_key = settings.ASSEMBLYAI_API_KEY
    
    config = aai.TranscriptionConfig(language_code="pt")
    transcriber = aai.Transcriber(config=config)
    
    print("Uploading file for transcription...")
    transcript = transcriber.transcribe(file_path)
    
    print("Transcription completed.")
    return transcript.text

if __name__ == "__main__":
    youtube_url = input("Enter the YouTube URL: ")
    audio_file = download_youtube_audio(youtube_url)
    
    transcription = transcribe_audio(audio_file)
    
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(transcription)

    print("Transcription saved to 'transcription.txt'.")
