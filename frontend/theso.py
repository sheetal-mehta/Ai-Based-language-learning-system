import streamlit as st
import requests

#end point used - https://www.openthesaurus.de/synonyme/search?q=haus&format=application/json

st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
    }
    </style>
    <h1 class="centered-title">German Thesaurus</h1>
    """,
    unsafe_allow_html=True
)
# here added the text box and default word.
user_input = st.text_input("Enter the Word", "haus")
# defining end point
url_string = "https://www.openthesaurus.de/synonyme/search?q="+str(user_input)+"&format=application/json&substring=true"
# getting response.
response = requests.get(url_string)

st.header("Synonyms and Related Words-")
# Adding in try in case the word is not present in the database.
try:
    data = response.json()
    # getting related sentences
    words_resp = data["synsets"]
    for i in words_resp:
        term_list = []
        terms = i["terms"]
        for t in terms:
            term_list.append(t["term"])
        st.write(','.join(term_list))
    # getting related sentences. 
    sent_resp = data["substringterms"]
    st.header("Related Sentences-")
    for sent in sent_resp:
        st.write(sent["term"])

except:
    st.write("Word not found!!! Please check and try again.")

