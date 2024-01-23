import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt


with open('rf_regressor.pkl', 'rb') as f:
    model = pickle.load(f)


def load_data():
    return pd.read_csv('./data/enhanced_data.csv')
    

st.title("La liga Fantasy Football Predictor")


col1, col2, col3 = st.columns(3)

with col1:
    search_query = st.text_input("Search by player")

with col2:
    position_filter = st.multiselect("Select Position", options=["All", "PO", "DF", "MC", "DE"])


data = load_data()
teamns = pd.read_csv('./data/teams_data.csv')
players = pd.read_csv('./data/players_data.csv')

data = data.drop_duplicates()

latest_season = data['Temporada'].max()
last_matchweek = data[data['Temporada'] == latest_season]['Jornada'].max()

latest_data = data[(data['Temporada'] == latest_season) & 
                            (data['Jornada'] == last_matchweek)]
print(last_matchweek)

def update_rolling_features(df, weeks=1):
    for week in range(weeks):
        for col in df.columns:
            if 'last' in col:
                num_weeks = last_matchweek
                new_col = col.replace(f'last{num_weeks}w', f'last{num_weeks+1}w')
                if new_col in df.columns:
                    df[col] = df[new_col].shift(1)
    return df

weeks_to_forecast = 4
forecast_datasets = {}

for i in range(1, weeks_to_forecast + 1):
    updated_data = update_rolling_features(latest_data.copy(), weeks=i)
    updated_data.drop(['Jornada', 'Temporada','avg','tp'], axis=1, inplace=True)
    updated_data.fillna(0, inplace=True)
    forecast_datasets[f'week_{i}'] = updated_data


week_1_data = forecast_datasets['week_4']
player_ids = week_1_data['playerId'].values
position_id = week_1_data['pid'].values
team_ids = week_1_data['tid'].values


week_1_predictions = model.predict(week_1_data)
week_1_predictions = pd.DataFrame(week_1_predictions, columns=['Predicted Points'])
week_1_predictions['playerId'] = player_ids
week_1_predictions['tid'] = team_ids

df_merged = week_1_predictions.merge(teamns, how='inner',on=['tid'])
df_merged = df_merged.merge(players, how='inner',on=['playerId'])
df_merged = df_merged[df_merged['nn'] != 'Vinícius Jr.']
df_merged = df_merged.drop_duplicates()
df_merged = df_merged.drop_duplicates(subset=['playerId'])

if search_query:
    df_merged = df_merged[df_merged['nn'].str.contains(search_query, case=False, na=False)]
    df_merged[['nn', 'tn', 'Predicted Points']]