from dotenv import load_dotenv
import os
import requests

STT_URL = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"

load_dotenv()
api_key = os.getenv("API_KEY")


def speech_to_text(file_url):
    response = requests.get(file_url)

    if response.status_code != 200:
        return None

    audio_data = response.content
    headers = {
        'Authorization': f'Api-Key {api_key}'
    }

    response = requests.post(STT_URL, headers=headers, data=audio_data)

    if not response.ok:
        return None

    return response.json().get('result')
