import streamlit as st
from st_audiorec import st_audiorec
import wordlist_variables as wv
import random
import audio_inference
import os
import allo_inference
import pron_tips


st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
    }
    </style>
    <h1 class="centered-title">Learn & Pronounce</h1>
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



# Function to shuffle the word list
def shuffle_words(words):
    random.shuffle(words)
    return words


# Function to insert word at specific position
def insert_word_at_position(words, word, position):
    if position >= len(words):
        words.append(word)
    else:
        words.insert(position, word)
    return words

# Initialize session state for the word list and current word
if 'words' not in st.session_state:
    st.session_state.words = shuffle_words(wv.word_list.copy())
if 'current_word' not in st.session_state:
    if st.session_state.words:
        st.session_state.current_word = st.session_state.words.pop(0)
    else:
        st.session_state.current_word = None
if 'performance' not in st.session_state:
    st.session_state.performance = None

def display_word_and_audio():
    if st.session_state.current_word:
        st.write("Current Word:", st.session_state.current_word)
        phonemes_cw = wv.word_list_phonemes[st.session_state.current_word]
        phones_cw = "".join(phonemes_cw)
        st.write(f"The phonemes for give word: {phones_cw}")
        tip = pron_tips.pro_tip_user(st.session_state.current_word ,phones_cw)
        st.info(tip,icon="ℹ️")
        st.write("Listen to the pronunciation below:")
        base_audio = f"base_files/{st.session_state.current_word}.wav"
        st.audio(base_audio)
        st.write("Record your pronunciation")
        return st_audiorec()
    else:
        st.write("All words completed!")
        return None

# Display the current word or completion message
wav_audio_data = display_word_and_audio()


if st.button("Submit"):
    if wav_audio_data is not None:
        with open('myfile.wav', mode='bx') as f:
            f.write(wav_audio_data)
        base_audio = f"base_files/{st.session_state.current_word}.wav"
        with st.spinner('Evaluating...'):
            siamese_output = audio_inference.get_siamese_inference("myfile.wav",base_audio,st.session_state.current_word)
            allo_output = audio_inference.get_allo_inference('myfile.wav')
            os.remove("myfile.wav")

            allo_word_phones = wv.word_list_phonemes[st.session_state.current_word]
            obtained_phones = allo_inference.split_phonemes(str(allo_output))
            comparision_val = allo_inference.compare_phoneme_lists(allo_word_phones,obtained_phones)
            #print(siamese_output)
            #print(comparision_val)
 
        if siamese_output >= 0.96 and comparision_val>=75:
            st.session_state.performance = "Excellent"         
            position = None
            st.success(st.session_state.performance, icon="✅")
        elif 0.80 <= siamese_output < 0.96 and 60<= comparision_val < 75:
            st.session_state.performance = "Good"
            highlighted_list1, highlighted_list2 = allo_inference.compare_and_highlight(allo_word_phones, obtained_phones)
            st.markdown(f"Expected Pronunciation: <p>{highlighted_list1}</p>", unsafe_allow_html=True)
            st.markdown(f"Your Pronunciation: <p>{highlighted_list2}</p>", unsafe_allow_html=True)
            position = 7
            st.warning(st.session_state.performance,icon="🔥")
        elif siamese_output< 0.80 and comparision_val<60:
            st.session_state.performance = "Needs More Practice"
            position = 3
            highlighted_list1, highlighted_list2 = allo_inference.compare_and_highlight(allo_word_phones, obtained_phones)
            st.markdown(f"Expected Pronunciation: <p>{highlighted_list1}</p>", unsafe_allow_html=True)
            st.markdown(f"Your Pronunciation: <p>{highlighted_list2}</p>", unsafe_allow_html=True)
            custom_warning("🚨"+st.session_state.performance)
        else:
            avg_op = ((siamese_output*100)+comparision_val)/2
            #avg_op = (siamese_output*100*0.80) + (comparision_val*0.20) 
            if avg_op>=75:
                st.session_state.performance = "Excellent"         
                position = None
                st.success(st.session_state.performance, icon="✅")
            elif 60<= avg_op < 75:
                st.session_state.performance = "Good"
                highlighted_list1, highlighted_list2 = allo_inference.compare_and_highlight(allo_word_phones, obtained_phones)
                st.markdown(f"Expected Pronunciation: <p>{highlighted_list1}</p>", unsafe_allow_html=True)
                st.markdown(f"Your Pronunciation: <p>{highlighted_list2}</p>", unsafe_allow_html=True)
                position = 7
                st.warning(st.session_state.performance,icon="🔥")
            elif avg_op<60:
                st.session_state.performance = "Needs More Practice"
                position = 3
                highlighted_list1, highlighted_list2 = allo_inference.compare_and_highlight(allo_word_phones, obtained_phones)
                st.markdown(f"Expected Pronunciation: <p>{highlighted_list1}</p>", unsafe_allow_html=True)
                st.markdown(f"Your Pronunciation: <p>{highlighted_list2}</p>", unsafe_allow_html=True)
                custom_warning("🚨"+st.session_state.performance)

if st.button("Next Word"):
    if st.session_state.performance is not None and st.session_state.current_word is not None:
        # Update the word list based on performance
        if st.session_state.performance == "Good":
            position = 7
        elif st.session_state.performance == "Needs More Practice":
            position = 3
        else:
            position = None

        if position is not None:
            st.session_state.words = insert_word_at_position(st.session_state.words, st.session_state.current_word, position)

        # Reset performance
        st.session_state.performance = None

    # Move to the next word
    if st.session_state.words:
        st.session_state.current_word = st.session_state.words.pop(0)
    else:
        st.session_state.current_word = None
    st.rerun()


#st.write("Remaining Words:", st.session_state.words)