import glob
import os
import pandas as pd

seasons = [f"{year}-{year+1}" for year in range(2017, 2024)]
folder_path = "./all_seassons_data/"

def concatenate(season):
    all_files = glob.glob(os.path.join(folder_path, f"{season}/*.csv"))

    df = pd.read_csv(all_files[0])

    # Loop over the remaining CSV files and merge them with the first one
    for file in all_files[1:]:
        df_other = pd.read_csv(file)
        df = pd.merge(df, df_other, on=['player', 'shirtnumber','nationality','nationality','age','minutes'])
        df.head()
    os.makedirs("./season_data", exist_ok=True)
    df.to_csv(f"./all_seassons/season_{season}.csv", index=False)

concatenate('2017-2018')