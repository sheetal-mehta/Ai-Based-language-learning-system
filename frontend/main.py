import streamlit as st
import sqlite3
import hashlib

# Set page configuration
st.set_page_config(layout="wide")

    # CSS to hide the red strip and center the buttons
hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .center-buttons {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 20px;
        }
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Below function hashes the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# This function is to verify the hashed password
def verify_password(stored_password, provided_password):
    return stored_password == hash_password(provided_password)

# connect to the database
def get_user(username):
    conn = sqlite3.connect('gec_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# creating a simple login page
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.success(f"Welcome, {st.session_state.username}!")
        return True

    st.title("Login")

    username = st.text_input("Username",placeholder="Enter your username")
    password = st.text_input("Password", type="password",placeholder="Enter your password")

    if st.button("Login"):
        if username and password:
            user = get_user(username)
            if user:
                stored_username, stored_password = user
                if verify_password(stored_password, password):
                    st.session_state.logged_in = True
                    st.session_state.username = stored_username
                    st.rerun()  # Refresh the page to load the main content
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Invalid username or password")
        else:
            st.error("Please enter both username and password")

    return False

# load the app after successful login
def load_app():
    
    # Define pages and app files related to them
    home_page = st.Page("home_page.py", title="Home Page", icon=":material/home:")
    audio_fc = st.Page("audio_fc.py", title="Learn & Pronounce", icon=":material/menu_book:")
    allo = st.Page("allo_fc.py", title="Pronunciation Assessment", icon=":material/select_check_box:")
    gec = st.Page("gec_fc.py", title="Grammatical Error Correction & Feedback", icon=":material/spellcheck:")
    theo = st.Page("theso.py", title="Thesaurus", icon=":material/list_alt:")

    # Navigation
    pg = st.navigation([home_page, audio_fc, allo, gec, theo])
    pg.run()

def main():
    
    if login():
        # loading the app only if the app login is successful.
        load_app()

if __name__ == "__main__":
    main()
