import streamlit as st
import pandas as pd
import pickle

with open('rf_regressor.pkl', 'rb') as f:
    model = pickle.load(f)


def load_data():
    return pd.read_csv('./data/app_data.csv')
    

st.title("La liga Fantasy Football Predictor")


col1, col2, col3 = st.columns(3)

with col1:

    search_query = st.text_input("Search by player or team")

with col2:

    position_filter = st.selectbox("Select Position", options=["All", "GK", "DEF", "MID", "FWD"])

with col3:
    jornada_filter = st.select_slider("Rango de Jornada", options=range(1,5))  


data = load_data()


filtered_search = data[data['nn'].str.contains(search_query, case=False, na=False)]

col1, col2 = st.columns((1,1))
with col1:
    st.write(filtered_search['nn'].to_list()[0])

