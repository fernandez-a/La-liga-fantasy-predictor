import requests
import json
import pandas as pd


class GetData:
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7,nl;q=0.6,fr;q=0.5',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6ImFsZWZlcmFyMjJAZ21haWwuY29tIiwicm9sZSI6Ikd1ZXN0IiwibmJmIjoxNjk3Mzk3MTcxLCJleHAiOjE2OTk5ODkxNzEsImlhdCI6MTY5NzM5NzE3MX0.FPM1tZ2wxCX5rBPD3A5DyOyE_Yqe9oksw5PXxRDtvdo',
        'Connection': 'keep-alive',
        'Origin': 'https://www.analiticafantasy.com',
        'Referer': 'https://www.analiticafantasy.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1',
    }

    def retrieve_data(self, season, week):
        params = {
        'temporada': f'{season}',
        'jornadaActiva': f'{week}',
        }

        response = requests.get('https://api.analiticafantasy.com/api/lfmPlayers/playersStats', params=params, headers=self.headers)

        if response.status_code == 200:
            
            data_json = response.json()['players']
            
            return data_json
        else:
            print(f"Error: {response.status_code} - Unable to fetch data.")
            return None

    def save_data_to_excel(self, data, file_name):
        # Create a DataFrame from the JSON data
        df = pd.DataFrame(data)

        file_name = f'data/{file_name}'
        df.to_excel(file_name, index=False)
        print(f"Data saved to {file_name}")

