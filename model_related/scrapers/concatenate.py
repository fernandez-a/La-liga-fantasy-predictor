import glob
import os
import pandas as pd

seasons = [f"{year}-{year+1}" for year in range(2017, 2024)]
folder_path = "./data/"

def concatenate(season):
    all_files = glob.glob(os.path.join(folder_path, f"{season}/*.csv"))

    data_frames = []

    for file in all_files:
        df = pd.read_csv(file)
        data_frames.append(df)

    concatenated_df = pd.concat(data_frames, ignore_index=True)

    os.makedirs("./season_data", exist_ok=True)
    concatenated_df.to_csv(f"./season_data/season_{season}.csv", index=False)

for season in seasons:
    concatenate(season)