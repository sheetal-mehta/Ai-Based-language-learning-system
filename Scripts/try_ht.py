import streamlit as st

phonemes1 = "i:x b i n"
phonemes2 = "i:es b i n"

# Function to highlight differences
def highlight_differences(p1, p2):
    p1_parts = p1.split()
    p2_parts = p2.split()
    highlighted_p1 = []
    highlighted_p2 = []

    for part1, part2 in zip(p1_parts, p2_parts):
        if part1 != part2:
            highlighted_p1.append(f"<span style='color: green'>{part1}</span>")
            highlighted_p2.append(f"<span style='color: red'>{part2}</span>")
        else:
            highlighted_p1.append(part1)
            highlighted_p2.append(part2)
    
    return " ".join(highlighted_p1), " ".join(highlighted_p2)

# Highlight differences
highlighted_phonemes1, highlighted_phonemes2 = highlight_differences(phonemes1, phonemes2)

# Streamlit app
st.title("Phoneme Comparison")

st.markdown("**Phonemes 1:**")
st.markdown(f"<p>{highlighted_phonemes1}</p>", unsafe_allow_html=True)

st.markdown("**Phonemes 2:**")
st.markdown(f"<p>{highlighted_phonemes2}</p>", unsafe_allow_html=True)
