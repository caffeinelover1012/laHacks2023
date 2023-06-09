from youtube_transcript_api import YouTubeTranscriptApi
from pytube import extract
import wikipediaapi
import re
from bs4 import BeautifulSoup
from pytesseract import pytesseract
from PIL import Image
import PyPDF2
import speech_recognition as sr

pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
def get_text_from_youtube(url):
    video_id=extract.video_id(url)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US', 'en-GB', 'a.en'])
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return ''

    # Combine all parts of the transcript and limit the text to 1500 words
    text = ' '.join([part['text'] for part in transcript])
    words = text.split()
    limited_text = ' '.join(words[:2000])

    return limited_text

# x=get_text_from_youtube('https://youtu.be/58N2N7zJGrQ')
# print(x)

def get_title_from_url(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?([a-z]{2}|simple)\.wikipedia\.org\/wiki\/(.+)$'
    match = re.search(pattern, url)
    if match:
        return match.group(2)
    else:
        return None
def get_wikipedia_text(page_title, language='en'):
    wiki = wikipediaapi.Wikipedia(language)
    page = wiki.page(page_title)

    if page.exists():
        return page.text
    else:
        return None
def get_text_from_wikipedia(url):
    page_title = get_title_from_url(url)
    if page_title:
        text = get_wikipedia_text(page_title)
        if text:
            pass
            return text[:2500]
        else:
            print("Page not found")
    else:
        print("Invalid URL")
    return None
# x=(get_text_from_wiki('https://en.wikipedia.org/wiki/Native_American_self-determination'))
# print(type(x))
# print(x)
def get_text_from_image(img):
    try:
        text = pytesseract.image_to_string(img)
        return text
    except:
        return None

# print(get_text_from_image('./static/testsc.jpg'))


def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file.stream, strict=False)
    pdf_text = []

    for page in reader.pages:
        content = page.extract_text()
        pdf_text.append(content)

    return " ".join(pdf_text)[:2000]


def get_text_from_audio(audio_file, duration=300):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source, duration=duration)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError:
            return "Error occurred during the request. Please try again."
