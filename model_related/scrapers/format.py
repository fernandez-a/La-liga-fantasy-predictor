import pandas as pd

df1 = pd.read_csv("./season_data/season_2017-2018.csv")
df2 = pd.read_csv("./season_data/season_2018-2019.csv")
df3 = pd.read_csv("./season_data/season_2019-2020.csv")
df4 = pd.read_csv("./season_data/season_2020-2021.csv")
df5 = pd.read_csv("./season_data/season_2021-2022.csv")
df6 = pd.read_csv("./season_data/season_2022-2023.csv")


df = pd.concat([df1, df2, df3, df4, df5, df6])

print(df.shape)
#df.to_csv("./season_data/all_seasons.csv", index=False)