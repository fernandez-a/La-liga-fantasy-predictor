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
        
        # Move the matched files to the new directory
        for file in matched_files:
            os.rename(file, os.path.join(chunk_dir, os.path.basename(file)))
            
    all_seasons_df = pd.concat(data_frames, ignore_index=True)
    os.makedirs("./season_data", exist_ok=True)
    all_seasons_df.to_csv(f"./season_data/season_{season}.csv", index=False)
    print(f'Succesfully merged into season {season}')
#2
def mergeGw(season, folder_path,rounds):
    for i in range(rounds):
        all_files = glob.glob(os.path.join(folder_path, f"{season}/gw_{i}/*.csv"))
        df = pd.read_csv(all_files[0])
        df = df.set_index('player')
        data_frames = []
        for file in all_files[1:]:
            if 'goalkeepers' in str(file):
                continue
                #df_other = pd.read_csv(file)
                #df_other['position'] = 'GK'
            else:
                df_other = pd.read_csv(file)
            df1 = pd.merge(df, df_other, on=['player'], suffixes=('','_remove'))
            data_frames.append(df1)
        os.makedirs(f"./season_data/{season}", exist_ok=True)
        all_seasons_df = pd.concat(data_frames, ignore_index=True)
        all_seasons_df.to_csv(f"./season_data/{season}/season_{season}_gw{i}.csv", index=False)
    print(f'Succesfully merged into season {season}')


#3
def concatenateGw(season, folder_path):
    all_files = glob.glob(os.path.join(folder_path, f"{season}/*.csv"))
    data_frames = []
    for file in all_files:
        df = pd.read_csv(file)
        data_frames.append(df)
    all_seasons_df = pd.concat(data_frames, ignore_index=True)
    os.makedirs("./season_data", exist_ok=True)
    all_seasons_df.to_csv(f"./season_data/season_{season}.csv", index=False)
    print(f'Succesfully merged into season {season}')


#4 
def concatenate_all(folder_path):
    all_files = glob.glob(os.path.join(folder_path, f"*.csv"))

    data_frames = []

    for file in all_files:
        df = pd.read_csv(file)
        data_frames.append(df)
    
    all_seasons_df = pd.concat(data_frames, ignore_index=True)
    all_seasons_df.to_csv(f"./season_data/all_seasons.csv", index=False)
    print(f'Succesfully merged all seasons')
