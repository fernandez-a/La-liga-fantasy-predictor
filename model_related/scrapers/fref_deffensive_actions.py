import itertools
from bs4 import BeautifulSoup
import re
import pandas as pd
import pickle
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

seasons = [f"{year}-{year+1}" for year in range(2017, 2024)]

class Scraper:
    def __init__(self):
        self.user_agents = itertools.cycle([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15A372 Safari/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Mobile/15E148 Safari/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4.1 Mobile/15E148 Safari/605.1.15"])
        options = Options()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.javascript": 2})
        options.add_argument(f"user-agent={next(self.user_agents)}")
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(options=options)
        with open('../pickles/all_matches.pkl', 'rb') as f:
            self.matches_all_season = pickle.load(f)
        self.headers_list = {
            'authority': 'fbref.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7,nl;q=0.6,fr;q=0.5',
                'cache-control': 'max-age=0',
                'if-modified-since': 'Sat, 02 Dec 2023 19:36:43 GMT',
                'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'sec-gpc': '1',
                'upgrade-insecure-requests': '1'
                 }


    def extract_table_data(self,url,headers_list, season):
        self.driver.get('https://www.google.com')
        self.driver.get(url)

        try:
            self.driver.find_element(By.XPATH,'//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]').click()
        except NoSuchElementException:
            pass
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        player_stats = soup.find_all('div', id=re.compile('all_player_stats_.*')) 
        headers = [th.get('data-stat') for th in player_stats[0].find('div',id = re.compile('div_stats_.*_defense')).find('thead').find_all('tr')[1].find_all('th')]
        matchweek_string = soup.find(string=re.compile('Matchweek \d+')).strip()
        matchweek = int(re.search(r'\d+', matchweek_string).group())
        headers.append('Matchweek')
        headers.append('Season')
        rows = []
        for i in player_stats:
            i = i.find('div',id = re.compile('div_stats_.*_defense'))
            for tr in i.find('tbody').find_all('tr'):
                row = [tr.find('th').text]
                row.extend([td.text for td in tr.find_all('td')])
                row.append(matchweek)
                row.append(season)
                rows.append(row)
                

        return headers, rows , matchweek

scraper = Scraper()

for i in scraper.matches_all_season:
    season = i["season"]
    matches = i['matches']
    match_chunks = [matches[n:n+10] for n in range(0, len(matches), 10)]

    os.makedirs(f"../all_seasons_data/{season}", exist_ok=True)
    
    for chunk_index, chunk in enumerate(match_chunks):
        filename = f"../all_seasons_data/{season}/{season}_chunk_{chunk_index}_deffensive.csv"
        if os.path.exists(filename):
            print(f"File {filename} already exists. Skipping...")
            continue

        headers = []
        all_rows = []
        for match in chunk:
            url = f"https://fbref.com{match}"
            headers, rows , matchweek = scraper.extract_table_data(url, scraper.headers_list, season)
            all_rows.extend(rows)
            common_headers = headers

        df = pd.DataFrame(all_rows, columns=common_headers)
        df.to_csv(filename, index=False)
        print(f"Saved {filename}")