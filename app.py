import streamlit as st
from utils import generate_random_sentence

st.title("Random Sentence Generator")
if st.button("Random Sentence Generator"):
    random_sentence = generate_random_sentence()
    st.text(f"Generated sentence is: {random_sentence}")
else:
    st.text("Click the button to generate a sentence")