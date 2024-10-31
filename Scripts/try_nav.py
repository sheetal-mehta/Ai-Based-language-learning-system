import streamlit as st

# Initialize session state for page if not already set
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Define a function to change the page
def navigate_to(page):
    st.session_state.page = page

# Sidebar for navigation
st.sidebar.title("Navigation")
st.sidebar.button("Home", on_click=navigate_to, args=("home",))
st.sidebar.button("About", on_click=navigate_to, args=("about",))

# Main content based on the current page
if st.session_state.page == 'home':
    st.title("Home Page")
    if st.button("Go to About Page"):
        navigate_to("about")
    st.markdown("""
    This is the home page content.
    You can go to the About Page from this paragraph by clicking the button above.
    """)
elif st.session_state.page == 'about':
    st.title("About Page")
    if st.button("Go to Home Page"):
        navigate_to("home")
    st.markdown("""
    This is the about page content.
    You can go back to the Home Page from this paragraph by clicking the button above.
    """)

