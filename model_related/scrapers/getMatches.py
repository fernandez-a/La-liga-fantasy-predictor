import pickle
import requests
from bs4 import BeautifulSoup

class getMatches:
    def getMatches(self,seasons):
            matches_all_seasons = [] 
            for season in seasons:
                response = requests.request("GET",f"https://fbref.com/en/comps/12/{season}/schedule/{season}-La-Liga-Scores-and-Fixtures", headers=self.headers_list)
                soup = BeautifulSoup(response.text, 'html.parser')
                dict = {}
                dict["season"] = season
                all_matches = soup.find_all("td", {"data-stat": "match_report"})
                matches = []
                for i in all_matches:
                    if i.find("a"):
                        if i.find("a").text == "Match Report":
                            matches.append(i.find("a").get("href"))
                dict["matches"] = matches
                matches_all_seasons.append(dict)  
            return matches_all_seasons  


matches = getMatches()

seasons = ["2017-2018","2018-2019","2019-2020","2020-2021"]
matches_all_seasons = matches.getMatches(seasons)

with open('matches_all_season.pkl', 'wb') as f:
    pickle.dump(matches_all_seasons, f)