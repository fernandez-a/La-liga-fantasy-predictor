from getData import GetData
from get2023 import GetData2023


if __name__ == "__main__":
    data_retriever = GetData()
    data_2023 = GetData2023()
    season = ['2020', '2021', '2022']
    weeks_to_fetch = [str(i) for i in range(1, 39)]

    for season in season:
        for week in weeks_to_fetch:
            data = data_retriever.retrieve_data(season, week)

            if data:
                print(f"Data retrieved for Season {season}, Week {week}")
                file_name = f'Week{week}_Season{season}Stats.xlsx'
                data_retriever.save_data_to_excel(data, file_name)
    
    season_2023 = ['2023']

    rounds = data_2023.retrieve_rounds(season_2023)

    for week in rounds:
        data = data_2023.retrieve_data(season_2023, week=week)
        if data:
            print(f"Data retrieved for Season 2023, Week {week}")
            file_name = f'Week{week}_Season2023Stats.xlsx'
            data_retriever.save_data_to_excel(data, file_name)
