import glob
import os
import pandas as pd

folder_path = "./data/*"
all_files = glob.glob(os.path.join(folder_path, "*.csv"))
data_frames = []

for file in all_files:
    file_name = os.path.basename(file)
    jornada, temporada = file_name.split('_')

    df = pd.read_csv(file)
    df['Temporada'] = temporada.split('Stats')[0].split('Season')[1]
    df['Jornada'] = jornada.split('Week')[1]

    data_frames.append(df)

concatenated_df = pd.concat(data_frames, ignore_index=True)

concatenated_df.to_csv("./data/all_seasons_data.csv", index=False)