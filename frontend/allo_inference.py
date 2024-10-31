import streamlit as st
import regex as re

def split_phonemes(phoneme_string):
    # List of phonemes
    phonemes_list = [
        'a', 'aː', 'b', 'd', 'd̠', 'd̺', 'e', 'eː', 'f', 'h', 'i', 'iː', 'j', 'k', 'kʰ', 'l', 'm', 'n', 
        'oː', 'p', 'pʰ', 's', 't', 'tʰ', 't̠', 'u', 'uː', 'v', 'x', 'y', 'yː', 'z', 'øː', 'ŋ', 'œ', 'ɐ', 
        'ɔ', 'ə', 'ɛ', 'ɛː', 'ɡ', 'ɪ', 'ʀ', 'ʁ', 'ʃ', 'ʊ', 'ʏ', 'ʏː', 'ʒ', 'ʔ', 'ʋ', 'ɕ', 'o', 'ɔɪ', 
        'ç', 'ɑː', 'ɑ', 'r', 'ts', 'p͡f', 'ø', 'tʃ', 'dʒ', 'aɪ', 'aʊ', 'g', 't͡s', 'ɔʏ'
    ]
    
    # Sort phonemes by length in descending order to match the longest phonemes first
    phonemes_list.sort(key=len, reverse=True)
    
    # Create a regex pattern to match any of the phonemes
    pattern = re.compile('|'.join(re.escape(phoneme) for phoneme in phonemes_list))
    
    # Find all matches in the input string
    matches = pattern.findall(phoneme_string)
    
    return matches

def compare_phoneme_lists(list1, list2):
    # Determine the length of the longer list
    max_length = max(len(list1), len(list2))
    
    # Initialize match count
    match_count = 0
    
    # Iterate over both lists and count matches
    for phoneme1, phoneme2 in zip(list1, list2):
        if phoneme1 == phoneme2:
            match_count += 1
    
    # Calculate the similarity percentage
    similarity_percentage = (match_count / max_length) * 100
    
    return similarity_percentage

def compare_and_highlight(list1, list2):
    # Determine the length of the longer list
    max_length = max(len(list1), len(list2))
    
    # Initialize the highlighted results
    highlighted_list1 = []
    highlighted_list2 = []
    
    # Iterate over both lists and compare phonemes
    for i in range(max_length):
        if i < len(list1) and i < len(list2):
            if list1[i] == list2[i]:
                highlighted_list1.append(list1[i])
                highlighted_list2.append(list2[i])
            else:
                highlighted_list1.append(f'<span style="color:green">{list1[i]}</span>')
                highlighted_list2.append(f'<span style="color:red">{list2[i]}</span>')
        elif i < len(list1):
            highlighted_list1.append(f'<span style="color:green">{list1[i]}</span>')
        elif i < len(list2):
            highlighted_list2.append(f'<span style="color:red">{list2[i]}</span>')
    
    return ' '.join(highlighted_list1), ' '.join(highlighted_list2)


# list1 = ['aɪ', 'n', 's']
# list2 = ['aɪ', 'n', 'z', 't']

# highlighted_list1, highlighted_list2 = compare_and_highlight(list1, list2)

# # Display using Streamlit
# st.markdown(f"List 1: <p>{highlighted_list1}</p>", unsafe_allow_html=True)
# st.markdown(f"List 2: <p>{highlighted_list2}</p>", unsafe_allow_html=True)
