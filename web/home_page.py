import streamlit as st


st.set_page_config(
    page_title="Home page",
    page_icon="👋",
    layout="centered")

variables = ['avg_mins_last3w',
       'avg_g_last3w', 'avg_ga_last3w', 'avg_oaa_last3w', 'avg_pae_last3w',
       'avg_br_last3w', 'avg_tsa_last3w', 'avg_wc_last3w', 'avg_pla_last3w',
       'avg_mins_last5w', 'avg_g_last5w', 'avg_ga_last5w', 'avg_oaa_last5w',
       'avg_pae_last5w', 'avg_br_last5w', 'avg_tsa_last5w', 'avg_wc_last5w',
       'avg_pla_last5w', 'avg_mins_last10w', 'avg_g_last10w', 'avg_ga_last10w',
       'avg_oaa_last10w', 'avg_pae_last10w', 'avg_br_last10w',
       'avg_tsa_last10w', 'avg_wc_last10w', 'avg_pla_last10w', 'goals_per_min',
       'assists_per_min', 'recoveries_per_game']


st.title('Welcome to my points predictor!')

st.write("""
This is a project that predict the points of a player in a specific gameweek

## How it works

The visualization page gives you the option to select a player or a team and plot some stats for the different gameweeks.
The prediction page gives you the option to select a player and it will predict the points for the next gameweek.


The dictionary of the variables that are shown in the visualization page are the following:
- "tp": "puntos totales",
- "nn": "nombre jugador",
- "tm": "nombre equipo",
- "playerId": "player id",
- "tid": "team id",
- "mins": "minutos",
- "g": "goles",
- "ga": "asistencias",
- "oaa": "asistencias sin gol",
- "pae": "balones al area",
- "pw": "penaltis provocados",
- "ps": "penaltis parados",
- "s": "paradas",
- "ec": "despejes",
- "og": "goles propia puerta",
- "gc": "goles en contra",
- "yc": "tarjetas amarillas",
- "syc": "segundas tarjetas amarillas",
- "rc": "tarjetas rojas",
- "tsa": "tiros a puerta",
- "wc": "regates",
- "br": "balones recuperados",
- "pc": "penaltis cometidos",
- "pla": "posesiones perdidas",
- "pm": "puntos relevo",
- "pid": "posicion id"

Enriched variables for the last 3,5,10 matchweeks and per minut and game:
         """ + "\n- ".join(variables))
