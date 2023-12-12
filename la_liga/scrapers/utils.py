import pandas as pd
import glob
import os
import re
#1
def concatenateChunks(season, folder_path, rounds):
    all_files = glob.glob(os.path.join(folder_path, f"{season}/*.csv"))
    data_frames = []
    for i in range(rounds):
        regex = re.compile(f'.*_chunk_{i}_.*')
        matched_files = [f for f in all_files if regex.match(os.path.basename(f))]
        chunk_data_frames = [pd.read_csv(file) for file in matched_files]
        df_chunk = pd.concat(chunk_data_frames, ignore_index=True)
        data_frames.append(df_chunk)
        
        chunk_dir = os.path.join(folder_path, f"{season}/gw_{i}")
        os.makedirs(chunk_dir, exist_ok=True)
        
        for file in matched_files:
            os.rename(file, os.path.join(chunk_dir, os.path.basename(file)))
            
    all_seasons_df = pd.concat(data_frames, ignore_index=True)
    os.makedirs("../season_data", exist_ok=True)
    all_seasons_df.to_csv(f"./season_data/season_{season}.csv", index=False)
    print(f'Succesfully merged into season {season}')
#2
def mergeGw(season, folder_path,rounds):
    for i in range(rounds):
        all_files = glob.glob(os.path.join(folder_path, f"{season}/gw_{i}/*.csv"))
        df = pd.read_csv(all_files[0])
        df['unique_id'] = df['player'] + '_' + df['Equipo'] + '_' + df['Matchweek'].astype(str)
        data_frames = []
        for file in all_files[1:]:
            df_other = pd.read_csv(file)
            if 'goalkeepers' in file:
                continue
                # df_other['unique_id'] = df_other['player'] + '_' + df_other['Equipo'] + '_' + df_other['Matchweek'].astype(str)
                # df = pd.merge(df, df_other, on=['unique_id'],how='inner', suffixes = ('','_remove'))
                # df = df.reset_index(drop=True)
                # df = df[df.columns.drop(list(df.filter(regex='_remove')))]
        data_frames.append(df)
        all_seasons_df = pd.concat(data_frames, axis=0)
        os.makedirs(f"../season_data/{season}", exist_ok=True)
        all_seasons_df.to_csv(f"./season_data/{season}/season_{season}_gw{i}_gk.csv", index=False)
    print(f'Succesfully merged into season {season}')


#3
def concatenateGw(season, folder_path):
    all_files = glob.glob(os.path.join(folder_path, f"{season}/*.csv"))
    data_frames = []
    for file in all_files:
        if 'gk' in file:
            df = pd.read_csv(file)
            df = df.drop_duplicates(subset=['unique_id'])
            data_frames.append(df)
    all_seasons_df = pd.concat(data_frames, axis=0)
    os.makedirs("../season_data", exist_ok=True)
    all_seasons_df.to_csv(f"./season_data/season_{season}_gk.csv", index=False)
    print(f'Succesfully merged into season {season}')


#4 
def concatenate_all(folder_path):
    all_files = glob.glob(os.path.join(folder_path, f"*_gk.csv"))

    data_frames = []

    for file in all_files:
        df = pd.read_csv(file)
        data_frames.append(df)
    
    all_seasons_df = pd.concat(data_frames, ignore_index=True)
    all_seasons_df.to_csv(f"./season_data/all_seasons_gk.csv", index=False)
    print(f'Succesfully merged all seasons')
