from openai import OpenAI
import os 
import streamlit as st
import numpy as np
from gtts import gTTS
import io
import soundfile as sf
import tempfile
MODEL_VERSION = "gpt-4o-mini"
TEXT_MODEL = "text-embedding-ada-002"

# set up your OpenAI API key and Assembly AI key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

client = OpenAI()
def generate_random_sentence():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Please generate a random sentence"}],
        temperature = 0.8
    )
    sentence = response.choices[0].message.content
    return sentence

def createAudio(sentence):
    tts = gTTS(sentence, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        with io.BytesIO() as f:
            # Save the audio to an in-memory file in MP3 format
            tts.write_to_fp(f)
            f.seek(0)

            # Read the audio data from the buffer
            audio_data, sample_rate = sf.read(f)

            # Save the data to the temporary WAV file
            sf.write(tmp_file.name, audio_data, sample_rate)
    return tmp_file

def saveAudio(audio_bytes, file_name):
    with open(file_name, 'wb') as new_wav_file:
        new_wav_file.write(audio_bytes)