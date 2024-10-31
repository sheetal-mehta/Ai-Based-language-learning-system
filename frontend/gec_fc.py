import streamlit as st
import get_pos as gp
import gec_inference as gi
import sqlite3
from sqlite3 import Error
import get_piimasking
from wordlist_variables import topic_suggestions
import random
import feedback_inference

topic_suggestion = topic_suggestions[random.randint(0, 98)]

st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
    }
    </style>
    <h1 class="centered-title">Grammatical Error Correction & Feedback</h1>
    """,
    unsafe_allow_html=True
)

# connection to the gec database. conn.execute(for executing queries here.)
con = sqlite3.connect("gec_database.db")
#cur = con.cursor()

st.info(f"Dont't Have anything in mind? Try This Topic:{topic_suggestion}, Dont like this topic? Click on Reset and Try again!")
# Initialize session state variables if not already set
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""
if "output" not in st.session_state:
    st.session_state["output"] = None

# Function to handle the "Get Results" button click
def get_results(text):
    table_data = gp.display_pos_table(text)
    st.session_state["output"] = table_data

# Function to reset the input text and clear outputs
def reset_text():
    st.session_state["input_text"] = ""
    st.session_state["output"] = None

def main():

    # Conditional handling to reset state before widget instantiation
    if st.button("Reset"):
        reset_text()
        st.rerun()

    
    with st.form(key="my_form"):
        user_input = st.text_area("Enter your text here:", key="input_text")

        
        st.markdown('<div class="center-buttons">', unsafe_allow_html=True)
        get_results_button = st.form_submit_button("Get Results")
        st.markdown('</div>', unsafe_allow_html=True)

        if get_results_button:
            st.header("Correction: ")
            with st.spinner('Correcting...'):
                correct_op = gi.correct_sentences(str(user_input), gi.tokenizer, gi.model)
            highlighted_output_gec = gi.highlight_differences(str(user_input),correct_op[0])
            st.markdown(f"<p style='font-size:20px;'>{highlighted_output_gec}</p>", unsafe_allow_html=True)
            #st.write(correct_op[0])
            get_results(correct_op[0])
            masked_input= get_piimasking.replace_tokens_with_labels(user_input)
            masked_correction  = get_piimasking.replace_tokens_with_labels(correct_op[0])

            query1 = f'Create table if not Exists gec_datapairs (Data,Correction)'
            query2 = f'INSERT INTO gec_datapairs (Data, Correction) VALUES (?, ?)'

            con.execute(query1)
            # Insert the values into the table
            con.execute(query2, (masked_input, masked_correction))

            con.commit()
            con.close()

    # Display the output after the buttons
    if st.session_state["output"] is not None:

        st.table(st.session_state["output"])

        if user_input==correct_op[0]:
            st.write("No Correction Required!!!")
        else:
            st.header("Feedback:")
            with st.spinner('Generating feedback...'):
                feedback= feedback_inference.get_feedback_llm(user_input,correct_op[0])
            
            st.write(feedback)


main()
