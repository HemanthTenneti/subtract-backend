import os, uuid
import yt_dlp
from dotenv import load_dotenv
from google import genai
import assemblyai as aai

load_dotenv()

aai.settings.api_key = os.getenv("AAI_API_KEY")
genai_client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))



def download_audio(url):
    name = f"{uuid.uuid4().hex}.mp3"
    print("Downloading...")
    with yt_dlp.YoutubeDL(
        {"extract_audio": True, "format": "bestaudio", "outtmpl": name}
    ) as ydl:
        info = ydl.extract_info(url, download=True)
        return name, info.get("title", "Untitled")


def transcribe_audio(path):
    print("Transcribing...")
    config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)
    res = aai.Transcriber(config=config).transcribe(path)
    if res.status == "error":
        raise RuntimeError(f"Transcription failed: {res.error}")
    return res.text


def summarize(text):
    print("Summarizing...")
    prompt = (
        "You are a content summarizer. I will provide a transcript. Summarize it in detail, within 250 words. "
        "Use 'narrator' for first-person references. If provided with transcripts less than 25 words, please ONLY return the text 'Transcription too short to summarize'\nTranscript:\n"
        + text
    )
    res = genai_client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    return res.text


def process_url(url):

    path, title = download_audio(url)
    transcript = transcribe_audio(path)
    summary = summarize(transcript)
    os.remove(path)

    return summary, transcript
