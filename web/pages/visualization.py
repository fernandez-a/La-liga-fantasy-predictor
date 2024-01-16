import streamlit as st
import pandas as pd
import pickle
import re

with open('rf_regressor.pkl', 'rb') as f:
    model = pickle.load(f)


def load_data():
    return pd.read_csv('./data/app_data.csv')
    

st.title("La liga Fantasy Football Predictor")


with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        position_filter = st.selectbox("Select Position", options=["All", "GK", "DEF", "MID", "FWD"])

    with col2:
        season_filter = st.selectbox("Select Season", options=["2020", "2021", "2022", "2023"])

    with col3:
        gw_range = st.slider("GW range", 1, 38, (22, 25))

    with col4:
        search_query = st.text_input("Input")

    with col5:
        options =  ['player','team']
        multiselect_filter = st.multiselect("Custom Search",options)

data = load_data()


if multiselect_filter == ['player']:
    print(search_query, multiselect_filter)  
    filtered_search = data[data['nn'].str.contains(search_query, case=False, na=False)]
    if filtered_search.empty:
        st.write("No results found")
    else:
        col1, col2 = st.columns((1,1))
        with col1:
            st.write(filtered_search['nn'].to_list()[0])
elif multiselect_filter == ['player','team']:
    filtered_search = data[data['nn'].str.contains(search_query, case=False, na=False) & data['tn'].str.contains(search_query, case=False, na=False)]

    if filtered_search.empty:
        st.write("No results found")
    else:

        col1, col2 = st.columns((1,1))
        with col1:
            st.write(filtered_search['nn'].to_list()[0])
            st.write(filtered_search['tn'].to_list()[0])
elif multiselect_filter == ['team']:
    filtered_search = data[data['tn'].str.contains(search_query, case=False, na=False)]
    if filtered_search.empty:
        st.write("No results found")
    else:
        col1, col2 = st.columns((1,1))
        with col1:
            st.write(filtered_search['tn'].to_list()[0])


# if search_query:
#     filtered_search = data[data['nn'].str.contains(search_query, case=False, na=False)]
#     col1, col2 = st.columns((1,1))
#     with col1:
#         st.write(filtered_search['nn'].to_list()[0])
# elif search_query_team:
#     filtered_search = data[data['tn'].str.contains(search_query_team, case=False, na=False)]
#     col1, col2 = st.columns((1,1))
#     with col1:
#         st.write(filtered_search['nn'].to_list()[0])
# elif search_query and search_query_team:
#     filtered_search = data[data['nn'].str.contains(search_query, case=False, na=False) & data['tn'].str.contains(search_query_team, case=False, na=False)]
#     print(filtered_search)
#     if filtered_search.empty:
#         st.write("No results found")
#     col1, col2 = st.columns((1,1))
#     with col1:
#         st.write(filtered_search['nn'].to_list()[0])
#         st.write(filtered_search['tn'].to_list()[0])


# if len(data[data['nn'].str.contains(search_query, case=False, na=False)]) > 0:
#     filtered_search = data[data['nn'].str.contains(search_query, case=False, na=False)]
#     col1, col2 = st.columns((1,1))
#     with col1:
#         st.write(filtered_search['nn'].to_list()[0])
# else:
#     filtered_search = data[data['tn'].str.contains(search_query, case=False, na=False)]
#     col1, col2 = st.columns((1,1))
#     with col1:
#         st.write(filtered_search['nn'].to_list()[0])