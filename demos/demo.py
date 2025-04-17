import requests
import os

#  api_key = os.getenv("ELEVENLABS_API_KEY")
api_key = "sk_df82d1641ee26f5fea897725beccb4a0a40801f2859b9754"

CHUNK_SIZE = 1024

VOICE_ID = "K9WixKJNDiyDSBLFy0Ic"  #Claude PVC
#  VOICE_ID = "pqHfZKP75CvOlQylNhV4"  #Bill
url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": api_key,
}

data = {
    "text": "Greetings! I am ALTER. How can I help you today?",
    "model_id": "eleven_turbo_v2",
    #  "voice_settings": {
    #  "stability": 0.5,
    #  "similarity_boost": 0.5
    #  }
}

response = requests.post(url, json=data, headers=headers)
with open("output.mp3", "wb") as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)
