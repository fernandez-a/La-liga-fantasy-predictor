import os
from getData import GetData
from get2023 import GetData2023

if __name__ == "__main__":
    data_retriever = GetData()
    data_2023 = GetData2023()
    season = ['2020', '2021', '2022']
    weeks_to_fetch = [str(i) for i in range(1, 39)]

    for season in season:
        for week in weeks_to_fetch:
            file_name = f'./data/{season}/Week{week}_Season{season}Stats.csv'
            if os.path.exists(file_name):
                print(f"File {file_name} already exists, skipping.")
                continue

            data = data_retriever.retrieve_data(season, week)

            if data:
                print(f"Data retrieved for Season {season}, Week {week}")
                os.makedirs(f'./data/{season}', exist_ok=True)
                data_retriever.save_data_to_csv(data, file_name)

    season_2023 = ['2023']

    rounds = data_2023.retrieve_rounds()

    for week in rounds:
        file_name = f'./data/{season_2023[0]}/Week{week}_Season{season_2023[0]}Stats.csv'
        if os.path.exists(file_name):
            print(f"File {file_name} already exists, skipping.")
            continue

        data = data_2023.retrieve_data(week=week)
        if data:
            print(f"Data retrieved for Season 2023, Week {week}")
            os.makedirs(f'./data/{season_2023[0]}', exist_ok=True)
            data_retriever.save_data_to_csv(data, file_name)