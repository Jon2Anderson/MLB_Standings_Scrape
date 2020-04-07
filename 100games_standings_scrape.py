import requests, os, datetime, json, collections as co
from bs4 import BeautifulSoup
from collections import Counter
import pandas as pd

al_east = ['NYY','TBR','BOS','TOR','BAL']
al_cent  = ['CLE','MIN','CHW','KCR','DET']
al_west = ['HOU','OAK','TEX','LAA','SEA']
nl_east = ['ATL','WAS','PHI','NYM','MIA']
nl_cent = ['STL','MIL','CHC','CIN','PIT']
nl_west = ['LAD','ARI','SFG','COL','SDP']

divisiondict = {'NYY': 'ALEast', 'TBR': 'ALEast', 'BOS': 'ALEast', 'TOR': 'ALEast', 'BAL': 'ALEast',
                'CLE': 'ALCent', 'MIN': 'ALCent', 'CHW': 'ALCent', 'KCR': 'ALCent', 'DET': 'ALCent',
                'HOU': 'ALWest', 'OAK': 'ALWest', 'LAA': 'ALWest', 'SEA': 'ALWest', 'TEX': 'ALWest',
                'ARI': 'NLWest', 'SFG': 'NLWest', 'SDP': 'NLWest', 'COL': 'NLWest', 'LAD': 'NLWest',
                'CHC': 'NLCent', 'MIL': 'NLCent', 'STL': 'NLCent', 'CIN': 'NLCent', 'PIT': 'NLCent',
                'ATL': 'NLEast', 'WSN': 'NLEast', 'NYM': 'NLEast', 'PHI': 'NLEast', 'MIA': 'NLEast'}

teams = ['NYY','TBR','BOS','TOR','BAL','CLE','MIN','CHW','KCR','DET', 'HOU',
         'OAK','TEX','LAA','SEA','ATL','WSN','PHI','NYM','MIA','STL','MIL',
         'CHC','CIN','PIT', 'LAD','ARI','SFG','COL','SDP']
years = ['2019','2018','2017','2016','2015']

masterdf = pd.DataFrame(columns=['Tm','Wins','Year','Div'])
for year in years:
  print(year)
  team_winpct_dict = {}
  for team in teams:
    url = 'https://www.baseball-reference.com/teams/{}/{}-schedule-scores.shtml'.format(team,year)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    table = soup.find('table', {'id': 'team_schedule'})

    table_head = table.find('thead')
    table_body = table.find('tbody')

    header=['Date', 'Blank1', 'Tm', 'Blank2', 'Opp', 'W/L', 'R', 'RA', 'Inn', 'W-L', 'Rank','GB','Win','Loss','Save','Time','D/N','Attend','Streak','Orig']
    trlist=[]
    for tr in table_body.findAll('tr'):
        trlist.append(tr)

    listofdicts=[]
    for row in trlist:
        the_row=[]
        for td in row.findAll('td'):
            the_row.append(td.text)
        od = co.OrderedDict(zip(header, the_row))
        listofdicts.append(od)

    df = pd.DataFrame(listofdicts)
    df = df.dropna()
    df = df[['Tm','W-L']]
    df["W-L"]= df["W-L"].str.split("-", n = 1, expand = True)
    wins = int(df.iloc[99,1])
    team_winpct_dict.update({team: wins})

  # Build a DataFrame
  finaldf = pd.DataFrame.from_dict(team_winpct_dict, orient='index', columns=['Wins'])
  finaldf = finaldf.reset_index()
  finaldf.columns = ['Tm', 'Wins']
  finaldf['Year'] = year
  finaldf['Div'] = finaldf['Tm'].map(divisiondict)
  finaldf = finaldf.sort_values(by='Wins', ascending=False)
  #finaldf.to_csv('{}_100Games_Standings.csv'.format(year))
  masterdf = pd.concat([masterdf, finaldf])

masterdf.to_csv('MLB_Standings_100G.csv')