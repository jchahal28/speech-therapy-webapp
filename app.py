import streamlit as st
from utils import generate_random_sentence, createAudio, saveAudio
IMAGE_ADDRESS="https://img.freepik.com/free-vector/hand-drawn-speech-therapy-scenes-collection_52683-78405.jpg"
AUDIO_FILE="output.wav"
SCORE_BENCHMARK = 0.98
GUIDE=["The app will generate a random sentence and its audio. You can play the audio, view the sentence, or do both.",
       "The you can click on the **Start Recording** button and start speaking out the text you see.",
       "Then click on **Stop Recording** to start the evaluations.",
        "Based on the evaluation you can start again if you like."]

def markdown_creators(*args):
    for chunks in args:
        st.markdown(f"- {chunks}")
        
st.title("Speech Therapist")
st.image(IMAGE_ADDRESS,caption = "Speech Therapist")
st.subheader("User Guide: How to Use the App 📒")
markdown_creators(*GUIDE)

st.title("Random Sentence Generator")
if st.button("Random Sentence Generator"):
    random_sentence = generate_random_sentence()
    st.text(f"Generated sentence is: {random_sentence}")
else:
    st.text("Click the button to generate a sentence")
    