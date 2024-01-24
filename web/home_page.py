import streamlit as st


st.set_page_config(
    page_title="Home page",
    page_icon="👋",
    layout="centered")


# Add a title
st.title('Welcome to my points predictor!')

# Add some text
st.write("""
This is a project that predict the points of a player in a specific gameweek

## How it works

The visualization page gives you the option to select a player or a team and plot some stats for the different gameweeks.
The prediction page gives you the option to select a player and it will predict the points for the next gameweek.

""")
