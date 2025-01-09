import streamlit as st
from streamlit_mic_recorder import mic_recorder
from utils import generate_random_sentence, createAudio, saveAudio, get_transcript, cal_cosine, sentence_comparer
#IMAGE_ADDRESS="https://img.freepik.com/free-vector/hand-drawn-speech-therapy-scenes-collection_52683-78405.jpg"
IMAGE_ADDRESS="https://img.freepik.com/free-vector/teddy-bear-concept-illustration_114360-1562.jpg?t=st=1736400332~exp=1736403932~hmac=214102eb6c79341b08028e84435cfdf2fe8f5410bfeebd714fe1987078074b2d&w=996"
AUDIO_FILE="output.wav"
SCORE_BENCHMARK = 0.98
GUIDE=["The app will generate a random sentence and its audio. You can play the audio, view the sentence, or do both.",
       "The you can click on the **Start Recording** button and start speaking out the text you see.",
       "Then click on **Stop Recording** to start the evaluations.",
        "Based on the evaluation you can start again if you like."]

def markdown_creators(*args):
    for chunks in args:
        st.markdown(f"- {chunks}")
        
st.title("BuddyBear: Your Speech Therapist 🧸")
st.image(IMAGE_ADDRESS,caption = "Speech Therapist")
st.subheader("User Guide: How to Use the App 📒")
markdown_creators(*GUIDE)

def disable_audio_recorder_session():
    st.session_state.recorder = False
def recreate_audio_recorder_session():
    st.session_state.recorder = True
def shuffle_sentence_and_disable_audio():
    st.session_state.recorder = False
    st.session_state.random_sentence = ""

if 'random_sentence' not in st.session_state:
    st.session_state.random_sentence = ""
if 'recorder' not in st.session_state:
    st.session_state.recorder = False

st.header("Generated Audio and Sentence")
if not st.session_state.random_sentence:
    text_output = generate_random_sentence()
    audio_output = createAudio(text_output)
    st.session_state.random_sentence = text_output
    st.audio(audio_output.name, format = "audio/wav")
    st.header("Transcript")
    st.subheader(text_output)
else:
    audio_rerun_output = createAudio(st.session_state.random_sentence)
    st.audio(audio_rerun_output.name, format = "audio/wav")
    st.header("Transcript")
    st.subheader(st.session_state.random_sentence)
# if st.button("Random Sentence Generator"):
#     random_sentence = generate_random_sentence()
#     st.text(f"Generated sentence is: {random_sentence}")
# else:
#     st.text("Click the button to generate a sentence")
st.header("Record ⏺️")
audio = mic_recorder(start_prompt="Start Recording 🎙️",
                     stop_prompt="Stop Recording 🛑",
                     just_once=False,
                     use_container_width=False,
                     callback=recreate_audio_recorder_session,
                     args=(),
                     kwargs={},
                     key=None)
if st.session_state.recorder:
    if audio:
        saveAudio(audio['bytes'], AUDIO_FILE)
        st.audio(audio['bytes'])
        with st.spinner("Evaulating Your Response..... ✅"):
            user_audio_transcript=get_transcript(AUDIO_FILE)
            if not user_audio_transcript:
                st.error("Ouch..Error has occured! Please contact the developer.", icon = "🛑")
                st.stop()
            cosine_score=cal_cosine(user_audio_transcript,st.session_state.random_sentence)
    
        st.header("Evaluations 🗒")
        if cosine_score > SCORE_BENCHMARK:
            st.subheader("Good Work Mate! 😍")
            st.subheader("Your score is {}".format(cosine_score))
            st.markdown("### Your Transcript!")
            st.write("Missing/Incorrect words are highlighted in red color for you!")
            st.markdown(f"#### {sentence_comparer(user_audio_transcript, st.session_state.random_sentence)}")
            st.subheader("You have Good Speaking Capabilities! Keep up ✅")
            # create a button re try
            st.button("Wanna Try Again 🤔", on_click=shuffle_sentence_and_disable_audio, key='success_btn')
        else:
            st.header("Having Little Bit of Trouble! 🤗")
            st.subheader("Your score is {}".format(cosine_score))
            st.markdown("### Your Transcript!")
            st.write("Missing/Incorrect words are highlighted in red color for you!")
            st.markdown(f"#### {sentence_comparer(user_audio_transcript, st.session_state.random_sentence)}")
            st.subheader("Let's Try Again 💪")
            # create a button re try
            st.button("Please Try Again 😊", on_click=shuffle_sentence_and_disable_audio, key='failure_btn')