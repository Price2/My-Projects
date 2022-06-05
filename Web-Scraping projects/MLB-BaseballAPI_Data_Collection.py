import pandas as pd
import statsapi
import requests, csv, re
from bs4 import BeautifulSoup
import pandas as pd


response = requests.get('https://statsapi.mlb.com/api/v1/sports/1/players?season=2022')
data = response.json()

playerIDList = []
for playerID in data['people']:
    playerIDList.append(playerID['id'])


playersStats = 'https://statsapi.mlb.com/api/v1/people/ID?hydrate=stats(group=[hitting,pitching,fielding],type=[gameLog])'
games = statsapi.schedule(start_date='04/07/2022',end_date='10/05/2022')
with open ('Games.csv', 'a+', newline='') as Games:
    Games_writer = csv.DictWriter(Games, ['GameID', 'HomeTeamID', 'GameDate', 'HomeTeamRuns', 'AwayTeamID', 'AwayTeamRuns'])
    Games_writer.writeheader()
    with open ('Teams.csv', 'a+', newline='') as Teams:
        teams_writer = csv.DictWriter(Teams, ['TeamID', 'Team Name'])
        teams_writer.writeheader()
        for game in games:
            Home_Team_Name = game['home_name']
            Away_Team_Name = game['away_name']
            GameID = game['game_id']
            HomeTeamID = game['home_id']
            GameDate = game['game_datetime']
            HomeTeamRuns = game['home_score']
            AwayTeamID = game['away_id']
            AwayTeamRuns = game['away_score']
            Games_writer.writerow({'GameID':GameID, 'HomeTeamID':HomeTeamID, 'GameDate':GameDate, 'HomeTeamRuns':HomeTeamRuns, 'AwayTeamID':AwayTeamID, 'AwayTeamRuns':AwayTeamRuns})
            teams_writer.writerow({'TeamID':HomeTeamID, 'Team Name': Home_Team_Name})


with open ('Players.csv', 'a+', newline='') as Players:
    players_writer = csv.DictWriter(Players, ['PlayerID', 'PlayerName'])
    players_writer.writeheader()
    with open ('Pitching.csv', 'a+', newline='') as Pitching:
        pitching_writer = csv.DictWriter(Pitching, ['PlayerID', 'TeamID', 'GameID', 'InningsPitched', 'Runs', 'Hits', 'Walks', 'HomeRuns', 'StrikeOuts', 'EarnedRuns'])
        pitching_writer.writeheader()
        with open ('Hitting.csv', 'a+', newline='') as Hitting:
            hitting_writer = csv.DictWriter(Hitting, ['PlayerID', 'TeamID', 'GameID', 'PlateAppearances', 'AtBats', 'Hits', 'Walks', 'StrikeOuts', 'Doubles', 'Triples', 'HomeRuns', 'RBIs', 'TotalBases', 'StolenBases'])
            hitting_writer.writeheader()
            for playerStat in playerIDList:
                player_ID_Link = requests.get(playersStats.replace('ID', str(playerStat)))
                player_stats_response = player_ID_Link.json()
                print(playerStat)
                if 'stats' in player_stats_response['people'][0]:
                        for displayName in player_stats_response['people'][0]['stats']:
                            if displayName['group']['displayName'] != 'fielding' and displayName['group']['displayName'] != 'pitching' :
                                    for splits in displayName['splits']:
                                        # print(splits)
                                        player_Name = splits['player']['fullName']
                                        player_ID = splits['player']['id']
                                        team_ID = splits['team']['id']
                                        game_ID = splits['game']['gamePk']
                                        PlateAppearances = splits['stat']['plateAppearances']
                                        atBats = splits['stat']['atBats']
                                        Hits = splits['stat']['hits']
                                        Walks = splits['stat']['baseOnBalls']
                                        StrikeOuts = splits['stat']['strikeOuts']
                                        Doubles = splits['stat']['doubles']
                                        Triples = splits['stat']['triples']
                                        HomeRuns = splits['stat']['homeRuns']
                                        RBIs = splits['stat']['rbi']
                                        TotalBases = splits['stat']['totalBases']
                                        StolenBases = splits['stat']['stolenBases']
                                        hitting_writer.writerow({'PlayerID':player_ID, 'TeamID':team_ID, 'GameID':game_ID, 'PlateAppearances':PlateAppearances, 'AtBats':atBats, 'Hits':Hits, 
                                        'Walks':Walks, 'StrikeOuts':StrikeOuts, 'Doubles':Doubles, 'Triples':Triples, 'HomeRuns':HomeRuns, 'RBIs':RBIs, 'TotalBases':TotalBases, 
                                        'StolenBases':StolenBases})
                                        players_writer.writerow({'PlayerID':player_ID, 'PlayerName': player_Name})
                            elif  displayName['group']['displayName'] == 'pitching':
                                for playerstat in displayName['splits']:
                                    player_Name = playerstat['player']['fullName']
                                    player_ID = playerstat['player']['id']
                                    team_ID = playerstat['team']['id']
                                    game_ID = playerstat['game']['gamePk']
                                    InningsPitched= playerstat['stat']['inningsPitched']
                                    Runs = playerstat['stat']['runs']
                                    Hits = playerstat['stat']['hits']
                                    Walks = playerstat['stat']['baseOnBalls']
                                    HomeRuns = playerstat['stat']['homeRuns']
                                    StrikeOuts = playerstat['stat']['strikeOuts']
                                    EarnedRuns = playerstat['stat']['earnedRuns']
                                    pitching_writer.writerow({'PlayerID':player_ID, 'TeamID':team_ID, 'GameID':game_ID, 'InningsPitched':InningsPitched, 'Runs':Runs,
                                    'Hits':Hits, 'Walks':Walks, 'HomeRuns':HomeRuns, 'StrikeOuts':StrikeOuts, 'EarnedRuns':EarnedRuns})
                                    players_writer.writerow({'PlayerID':player_ID, 'PlayerName': player_Name})
df = pd.read_csv('Teams.csv')
df.drop_duplicates(inplace=True)
df.to_csv('Teams.csv')