import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def load_data():
    return pd.read_csv('./data/app_data.csv')

st.title("La liga Fantasy Football Predictor")

data = load_data()
data = data.drop_duplicates(subset=['Jornada', 'playerId','Temporada'])


stats_dict = {
    'Goals': 'g',
    'Points': 'tp',
    'Assists': 'ga',
    'Shots converted': 'tsa',
    'Mins Played': 'mins',
    'Red Cards': 'rc',
}

data.loc[:,'position'] = data['pid'].map({1: 'PO', 2: 'DF', 3: 'MC', 4: 'DE'})
data['Temporada'] = data['Temporada'].astype(str)
position_dict = {1: 'PO', 2: 'DF', 3: 'MC', 4: 'DE'}

with st.sidebar:
    position_filter = st.multiselect("Select Position", options=["All", "PO", "DF", "MC", "DE"])
    season_filter = st.multiselect("Select Season", options=["2020","2021", "2022", "2023"])
    gw_range = st.slider("GW range", 1, 38, (22, 25))
    search_query = st.text_input("Input")
    options =  ['player','team']
    multiselect_filter = st.selectbox("Custom Search",options)
    plot_stats = st.multiselect("Select Stats to Plot", options=list(stats_dict.keys()))

filtered_data = data.copy()

if position_filter != "All":
    filtered_data = filtered_data[filtered_data['position'].isin(position_filter)]

if position_filter == "All" or filtered_data.empty:
    filtered_data = data.copy()

if season_filter:
    filtered_data = filtered_data[filtered_data['Temporada'].isin(season_filter)]

if gw_range:
    filtered_data = filtered_data[(filtered_data['Jornada'] >= gw_range[0]) & (filtered_data['Jornada'] <= gw_range[1])]

if search_query:
    if 'player' in multiselect_filter:
        filtered_data = filtered_data[filtered_data['nn'].str.contains(search_query, case=False, na=False)]
    if 'team' in multiselect_filter:
        filtered_data = filtered_data[filtered_data['tn'].str.contains(search_query, case=False, na=False)]
if plot_stats and search_query:
    stats_columns = [stats_dict[stat] for stat in plot_stats]
    if multiselect_filter == 'team' and search_query:
        if not filtered_data.empty: 
            fig, axis = plt.subplots(3, 2, figsize=(15,15))
            if 'mins' in stats_columns:
                temp_data = filtered_data.copy()
                grouped_data = temp_data.groupby('nn')['mins'].sum().sort_values(ascending=False).reset_index()
                grouped_data.plot(x='nn', y='mins', kind='line', ax=axis[0,0])
                axis[0,0].set_title('Mins')
            if 'tp' in stats_columns :
                temp_data = filtered_data.copy()  
                grouped_data = temp_data.groupby('nn')['tp'].sum().sort_values(ascending=False).reset_index()
                grouped_data.plot(x='nn', y='tp', kind='bar', ax=axis[0,1], color='red')
                axis[0,1].set_title('Total Points')
            if 'ga' in stats_columns :
                temp_data = filtered_data.copy()  
                grouped_data = temp_data.groupby('nn')['ga'].sum().sort_values(ascending=False).reset_index()
                grouped_data.plot(x='nn', y='ga', kind='bar', ax=axis[1,0], color='green')
                axis[1,0].set_title('Assists')
            if 'tsa' in stats_columns :
                temp_data = filtered_data.copy()
                temp_data['%tsa_converted'] = temp_data['tsa'] / temp_data['g']
                temp_data['%tsa_converted'] = temp_data['%tsa_converted'].replace([np.inf, -np.inf], np.nan)
                temp_data['%tsa_converted'] = temp_data['%tsa_converted'].fillna(temp_data['%tsa_converted'].mean())
                grouped_data = temp_data.groupby('nn')['%tsa_converted'].sum().sort_values(ascending=False).reset_index()
                grouped_data.plot(x='nn', y='%tsa_converted', kind='bar', ax=axis[1,1])
                axis[1,1].set_title('% Shots Converted')
            if 'g' in stats_columns :
                temp_data = filtered_data.copy()  
                grouped_data = temp_data.groupby('nn')['g'].sum().sort_values(ascending=False).reset_index()
                grouped_data.plot(x='nn', y='g', kind='bar', ax=axis[2,0])
                axis[2,0].set_title('Goals')
            if 'rc' in stats_columns :
                temp_data = filtered_data.copy()
                grouped_data = temp_data.groupby('nn')['rc'].sum().sort_values(ascending=False).reset_index()
                grouped_data.plot(x='nn', y='rc', kind='bar', ax=axis[2,1])
                axis[2,1].set_title('Red Cards')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.write("No data to plot")

    elif multiselect_filter == 'player' and search_query:
        if not filtered_data.empty:
            fig, axis = plt.subplots(3, 2, figsize=(15,15))
            if 'mins' in stats_columns:
                temp_data = filtered_data.copy()
                grouped_data = temp_data.groupby(['Jornada','nn'])['mins'].sum().sort_values(ascending=False).reset_index()
                grouped_data.plot(x='nn', y='mins', kind='line', ax=axis[0,0])
                axis[0,0].set_title('Mins')
            if 'tp' in stats_columns :
                temp_data = filtered_data.copy()  
                grouped_data = temp_data.groupby(['Jornada','nn'])['tp'].sum().sort_values(ascending=False).reset_index()
                grouped_data.plot(x='nn', y='tp', kind='bar', ax=axis[0,1], color='red')
                axis[0,1].set_title('Total Points')
            if 'ga' in stats_columns :
                temp_data = filtered_data.copy()  
                grouped_data = temp_data.groupby(['Jornada','nn'])['ga'].sum().sort_values(ascending=False).reset_index()
                grouped_data.plot(x='nn', y='ga', kind='bar', ax=axis[1,0], color='green')
                axis[1,0].set_title('Assists')
            if 'tsa' in stats_columns :
                temp_data = filtered_data.copy()
                temp_data['%tsa_converted'] = temp_data['tsa'] / temp_data['g']
                temp_data['%tsa_converted'] = temp_data['%tsa_converted'].replace([np.inf, -np.inf], np.nan)
                temp_data['%tsa_converted'] = temp_data['%tsa_converted'].fillna(temp_data['%tsa_converted'].mean())
                grouped_data = temp_data.groupby(['Jornada','nn'])['%tsa_converted'].sum().sort_values(ascending=False).reset_index()
                grouped_data.plot(x='nn', y='%tsa_converted', kind='bar', ax=axis[1,1])
                axis[1,1].set_title('% Shots Converted')
            if 'g' in stats_columns :
                temp_data = filtered_data.copy()  
                grouped_data = temp_data.groupby(['Jornada','nn'])['g'].sum().sort_values(ascending=False).reset_index()
                grouped_data.plot(x='nn', y='g', kind='bar', ax=axis[2,0])
                axis[2,0].set_title('Goals')
            if 'rc' in stats_columns :
                temp_data = filtered_data.copy()
                grouped_data = temp_data.groupby(['Jornada','nn'])['rc'].sum().sort_values(ascending=False).reset_index()
                grouped_data.plot(x='nn', y='rc', kind='bar', ax=axis[2,1], color='pink')
                axis[2,1].set_title('Red Cards')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.write("No data to plot")
    else:
        st.write("No data to plot")
        


if not filtered_data.empty:
    filtered_data = filtered_data.sort_values(by=['Jornada']).reset_index(drop=True)
    st.dataframe(filtered_data)