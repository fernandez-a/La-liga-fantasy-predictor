import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt


with open('rf_regressor.pkl', 'rb') as f:
    model = pickle.load(f)


def load_data():
    return pd.read_csv('./data/enhanced_data.csv')
    

st.title("La liga Fantasy Football Predictor")


col1, col2 = st.columns(2)

with col1:
    search_query = st.text_input("Search by player")

with col2:
    gw_range = st.slider("GW range", 1, 4, 1)

data = load_data()
teamns = pd.read_csv('./data/teams_data.csv')
players = pd.read_csv('./data/players_data.csv')

data = data.drop_duplicates()

latest_season = data['Temporada'].max()
last_matchweek = data[data['Temporada'] == latest_season]['Jornada'].max()

latest_data = data[(data['Temporada'] == latest_season) & 
                            (data['Jornada'] == last_matchweek)]


def merge_forecast_data(forecast_datasets, model, weeks_to_forecast):
    df_all_merged = pd.DataFrame()

    for i in range(1, weeks_to_forecast + 1):
        week_data = forecast_datasets[f'week_{i}']
        player_ids = week_data['playerId'].values
        position_id = week_data['pid'].values
        team_ids = week_data['tid'].values

        week_predictions = model.predict(week_data)
        week_predictions = pd.DataFrame(week_predictions, columns=['Predicted Points'])
        week_predictions['playerId'] = player_ids
        week_predictions['tid'] = team_ids

        df_merged = week_predictions.merge(teamns, how='inner',on=['tid'])
        df_merged = df_merged.merge(players, how='inner',on=['playerId'])
        df_merged = df_merged.drop_duplicates(subset=['playerId', 'tid'])
        df_merged['week']  = i
        df_merged['Predicted Points'] = df_merged['Predicted Points'].round(0)
        df_all_merged = pd.concat([df_all_merged, df_merged], axis=0)

    return df_all_merged


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

df_merged = merge_forecast_data(forecast_datasets, model, weeks_to_forecast)
 
if search_query and gw_range:
    df_merged = df_merged[(df_merged['nn'].str.contains(search_query, case=False, na=False)) & df_merged['week'].isin(range(1, gw_range + 1))].reset_index(drop=True)
    df_merged    
else:
    df_merged = df_merged[df_merged['week'].isin(range(1, gw_range + 1))].reset_index(drop=True)
    df_merged         