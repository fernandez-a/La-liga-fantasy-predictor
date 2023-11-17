import glob
import os
import pandas as pd

folder_path = "./data"

# Lee todos los archivos Excel en la carpeta especificada data
all_files = glob.glob(os.path.join(folder_path, "*.xlsx"))

data_frames = []

# Lee cada archivo Excel, agrega columnas de temporada y jornada, y almacena su contenido en la lista
for file in all_files:
    # Extrae información de temporada y jornada del nombre del archivo
    file_name = os.path.basename(file)
    jornada, temporada = file_name.split('_')  # Asumiendo que el nombre del archivo contiene "temporada_jornada.xlsx"

    df = pd.read_excel(file)

    # Agrega columnas de temporada y jornada
    df['Temporada'] = temporada.split('Stats')[0]
    df['Jornada'] = jornada

    data_frames.append(df)

# Concatena todos los DataFrames en uno
concatenated_df = pd.concat(data_frames, ignore_index=True)

# Guarda el DataFrame concatenado en un nuevo archivo Excel
concatenated_df.to_csv("all_seasons_data.csv", index=False)