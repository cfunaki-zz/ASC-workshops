# http://www.gregreda.com/2015/02/15/web-scraping-finding-the-api/

import requests
import pandas as pd

shots_url = 'http://stats.nba.com/stats/playerdashptshotlog?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0&PlayerID=2544&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision='

# request the URL and parse the JSON
response = requests.get(shots_url)
response.raise_for_status() # raise exception if invalid response

# Load the JSON data into litss
headers = response.json()['resultSets'][0]['headers']
shots = response.json()['resultSets'][0]['rowSet']

# Put the data into a DataFrame
shots_df = pd.DataFrame(shots, columns=headers)