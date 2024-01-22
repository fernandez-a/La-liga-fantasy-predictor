import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


def load_data():
    return pd.read_csv('./data/app_data.csv')

st.title("La liga Fantasy Football Predictor")

data = load_data()

stats_dict = {
    'Goals': 'g',
    'Points': 'tp',
    'Goals Against': 'ga',
    'Position': 'position',
    'Mins Played': 'mins',
    'Read Cards': 'rc'
}

data.loc[:,'position'] = data['pid'].map({1: 'PO', 2: 'DF', 3: 'MC', 4: 'DE'})
data['Temporada'] = data['Temporada'].astype(str)
position_dict = {1: 'PO', 2: 'DF', 3: 'MC', 4: 'DE'}

with st.sidebar:
    position_filter = st.multiselect("Select Position", options=["All", "PO", "DF", "MC", "DE"])
    season_filter = st.multiselect("Select Season", options=["2021", "2022", "2023"])
    gw_range = st.slider("GW range", 1, 38, (22, 25))
    search_query = st.text_input("Input")
    options =  ['player','team']
    multiselect_filter = st.multiselect("Custom Search",options)
    statistics = st.multiselect("Statistics", options=['Goals', 'Goals Against'])#['Goals', 'Assists', 'Clean Sheets', 'Saves', 'Penalties Saved', 'Penalties Missed', 'Yellow Cards', 'Red Cards', 'Own Goals', 'Bonus Points', 'Points'])
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

if statistics:
    stats_columns = [stats_dict[stat] for stat in statistics]
    filtered_data = filtered_data[stats_columns]    
if plot_stats:
    print(multiselect_filter)
    stats_columns = [stats_dict[stat] for stat in plot_stats]
    fig, axis = plt.subplots(3, 1, figsize=(10,30))
    if plot_stats != None: 
        if 'position' in stats_columns:
            position_data = filtered_data['pid'].value_counts().reset_index()
            position_data['index'] = position_data['pid'].map(position_dict) 
            axis[0].pie(position_data['pid'], labels = position_data['index'],autopct='%1.1f%%')
            axis[0].set_title('Position')
        if 'mins' in stats_columns:
            grouped_data = filtered_data.groupby('nn')['mins'].sum().sort_values(ascending=False).reset_index()
            grouped_data.plot(x='nn', y='mins', kind='line', ax=axis[1])
            axis[1].set_title('Mins')
        if 'g' in stats_columns :
            if not multiselect_filter:
                filtered_data = filtered_data.sort_values(by=['g'], ascending=False).reset_index(drop=True)
                filtered_data = filtered_data.head(60)
            grouped_data = filtered_data.groupby('nn')['g'].sum().sort_values(ascending=False).reset_index()
            grouped_data.plot(x='nn', y='g', kind='bar', ax=axis[2])
            axis[2].set_title('Goals')

    plt.tight_layout()
    st.pyplot(fig)


filtered_data = filtered_data.sort_values(by=['Jornada']).reset_index(drop=True)
st.dataframe(filtered_data)