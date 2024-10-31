import streamlit as st
from allosaurus.app import read_recognizer
import epitran
from st_audiorec import st_audiorec
from gtts import gTTS
import os
import allo_inference
import random
import wordlist_variables as wv
import pron_tips

epi = epitran.Epitran('deu-Latn')
sentence_suggestion = wv.top_sentences[random.randint(0, 45)]

st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
    }
    </style>
    <h1 class="centered-title">Pronunciation Assessment</h1>
    """,
    unsafe_allow_html=True
)


# Custom CSS for a custom warning box
custom_css = """
<style>
div.custom-warning-box {
    background-color: #ffcccc !important;  /* Lighter red background */
    color: black !important;  /* Black text color */
    padding: 10px 20px;  /* Adjust padding to match default Streamlit alert */
    border-radius: 5px;  /* Border radius to match default Streamlit alert */
    margin-bottom: 10px;  /* Margin bottom to match spacing between alerts */
    font-size: 1rem;  /* Adjust font size to match default Streamlit alert */
    display: flex;
    align-items: center;
}
</style>
"""

# Inject the custom CSS into the Streamlit app
st.markdown(custom_css, unsafe_allow_html=True)

# Function to display a custom warning box
def custom_warning(message):
    st.markdown(f'<div class="custom-warning-box">{message}</div>', unsafe_allow_html=True)

st.info(f"Dont't Have anything in mind? Try This:{sentence_suggestion}")
# Initialize session state for user input and IPA transcription
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''
if 'ipa_transcription' not in st.session_state:
    st.session_state['ipa_transcription'] = ''

# Function to reset the session state
def reset():
    st.session_state['user_input'] = ''
    st.session_state['ipa_transcription'] = ''

# Creating a form
with st.form("input_form"):
    user_input = st.text_area("Enter your text here", value=st.session_state['user_input'])
    submit_button = st.form_submit_button(label="Enter")
    reset_button = st.form_submit_button(label="Reset", on_click=reset)

# Displaying the user input
if submit_button:
    st.session_state['user_input'] = user_input
    st.session_state['ipa_transcription'] = epi.transliterate(user_input)
    st.rerun()

if st.session_state['ipa_transcription']:

    st.header("Listen to Pronunciation Below")
    # Convert text to speech
    tts = gTTS(text=user_input, lang='de')
    # Save the audio file
    audio_file = "german_text.mp3"
    tts.save(audio_file)
    # printing or showing audio on frontend
    st.audio("german_text.mp3",format="audio/mpeg")
    # prompting user
    st.write(f"The below are the phonemes, observe carefully and take note of the tips- {st.session_state['ipa_transcription']}")
    tip = pron_tips.pro_tip_user(st.session_state['user_input'] ,st.session_state['ipa_transcription'])
    st.info(tip,icon="ℹ️")
    st.header("Speak the sentence now!")
    wav_audio_data = st_audiorec()
    if wav_audio_data is not None:
        with open('myfile_asm.wav', mode='bx') as f:
            f.write(wav_audio_data)
            # Using allosaurus for inference
        with st.spinner('Evaluating...'):
            model = read_recognizer("finetuned")
            output = model.recognize("myfile_asm.wav", 'deu')
        st.header("Below is the evaluation")
        expected_phones_list = allo_inference.split_phonemes(st.session_state['ipa_transcription'])
        obtained_output_list = allo_inference.split_phonemes(output)
        similarity_obtained = allo_inference.compare_phoneme_lists(expected_phones_list,obtained_output_list)
        
        if similarity_obtained>=75:
            st.success("Well Done! Excellent.",icon = "✅")
        elif similarity_obtained>=50 and similarity_obtained<75:
            st.warning("Good!", icon="🔥")       
            highlighted_list1, highlighted_list2 = allo_inference.compare_and_highlight(expected_phones_list,obtained_output_list)
            # Display using Streamlit
            st.markdown(f"Expected Pronunciation:: <p>{highlighted_list1}</p>", unsafe_allow_html=True)
            st.markdown(f"Your Pronunciation: <p>{highlighted_list2}</p>", unsafe_allow_html=True)
        else:
            custom_warning("🚨 Needs More Practice! Try Again!")
            highlighted_list1, highlighted_list2 = allo_inference.compare_and_highlight(expected_phones_list,obtained_output_list)
            # Display using Streamlit
            st.markdown(f"Expected Pronunciation: <p>{highlighted_list1}</p>", unsafe_allow_html=True)
            st.markdown(f"Your Pronunciation: <p>{highlighted_list2}</p>", unsafe_allow_html=True)

        #st.write(f"Expected Pronunciation: {st.session_state['ipa_transcription']}")
        #st.write(f"Your Pronunciation : ", output)
        os.remove("myfile_asm.wav")
        os.remove("german_text.mp3")

# Reset button to clear the session state
if reset_button:
    reset()
    st.rerun()
