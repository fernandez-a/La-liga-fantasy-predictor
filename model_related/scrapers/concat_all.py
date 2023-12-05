import glob
import os
import pandas as pd

seasons = [f"{year}-{year+1}" for year in range(2017, 2024)]
folder_path = "./season_data/"

def concatenate(season):
    all_files = glob.glob(os.path.join(folder_path, f"season_{season}.csv"))

    data_frames = []

    for file in all_files:
        df = pd.read_csv(file)
        data_frames.append(df)

    return pd.concat(data_frames, ignore_index=True)

season_dataframes = []
for season in seasons:
    season_df = concatenate(season)
    season_dataframes.append(season_df)

all_seasons_df = pd.concat(season_dataframes, ignore_index=True)
all_seasons_df.to_csv(f"season_data/all_seasons.csv", index=False)