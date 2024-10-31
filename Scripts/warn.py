import streamlit as st

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

# Example usage of custom warning box
st.success("This is excellent")
custom_warning("This is a custom warning box with a red background and black text color!")
st.warning("This is info")
