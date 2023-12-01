from getData import GetData
from get2023 import GetData2023

def retrieve_and_save_data(data_retriever, seasons, weeks):
    for season in seasons:
        for week in weeks:
            data = data_retriever.retrieve_data(season, week)
            if data:
                print(f"Data retrieved for Season {season}, Week {week}")
                file_name = f'Week{week}_Season{season}Stats.xlsx'
                data_retriever.save_data_to_excel(data, file_name)

if __name__ == "__main__":
    data_retriever = GetData()
    data_2023 = GetData2023()
    weeks_to_fetch = [str(i) for i in range(1, 39)]
    
    seasons = ['2020', '2021', '2022']
    retrieve_and_save_data(data_retriever, seasons, weeks_to_fetch)
    
    season_2023 = ['2023']
    rounds = data_2023.retrieve_rounds(season_2023)
    retrieve_and_save_data(data_2023, season_2023, rounds)