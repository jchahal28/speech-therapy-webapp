from openai import OpenAI
import assemblyai as aai
from sklearn.metrics.pairwise import cosine_similarity
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
os.environ["ASSEMBLYAI_API_KEY"] = st.secrets["ASSEMBLYAI_API_KEY"]

client = OpenAI()

def get_openai_embeddings(text: str) -> list[float]:
    response = client.embeddings.create(input=text, model=TEXT_MODEL)
    return response.data[0].embedding

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

def get_transcript(filepath):
    aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(filepath)
    if transcript.status == aai.TranscriptStatus.error:
        return None
    else:
        return transcript.text
    
def cal_cosine(sentence1, sentence2):
    sentence1_embedded = get_openai_embeddings(sentence1)
    sentence2_embedded = get_openai_embeddings(sentence2)
    
    arrayOne = np.array(sentence1_embedded).reshape(1,-1)
    arrayTwo = np.array(sentence2_embedded).reshape(1,-1)
    cos_sim = cosine_similarity(arrayOne, arrayTwo)
    return cos_sim[0][0]

def sentence_comparer(user_transcript, actual_sentence):
    user_words = user_transcript.split(" ")
    final_view = ""
    for word in user_words:
        if word in actual_sentence:
            final_view += word + " "
        else:
            final_view +=  f":red[{word}] "
    return final_view
