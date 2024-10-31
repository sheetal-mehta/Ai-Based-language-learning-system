import spacy
import streamlit as st

# Attempt to load the German language model
try:
    nlp = spacy.load('de_core_news_sm')
except OSError:
    st.write("Model 'de_core_news_sm' not found. Downloading now...")
    from spacy.cli import download
    download('de_core_news_sm')
    nlp = spacy.load('de_core_news_sm')

# mapping for part of speech tags to more readable labels
pos_mapping = {
    "NOUN": "noun",
    "VERB": "verb",
    "ADJ": "adjective",
    "ADV": "adverb",
    "PRON": "pronoun",
    "DET": "determiner",
    "ADP": "adposition",
    "NUM": "numeral",
    "CONJ": "conjunction",
    "PART": "particle",
    "INTJ": "interjection",
    "PROPN": "proper noun",
    "PUNCT": "punctuation",
    "SYM": "symbol",
    "X": "other"
}

def display_pos_table(text):
    # Process the text
    doc = nlp(text)

    # Prepare data for display
    tokens = [token.text for token in doc]
    pos_labels = [pos_mapping.get(token.pos_, token.pos_) for token in doc]

    
    table_data = {
        "Token": tokens,
        "Part of Speech": pos_labels
    }
    
    return table_data

