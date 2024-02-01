from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore
from pprint import pprint
from datetime import datetime
import json
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

games = scoreboard.ScoreBoard()
# stat = boxscore.BoxScore()

sb = games.get_dict()["scoreboard"]

#pprint(sb)

# print out all games today
# tracks live score of game and live stats for all the players playing
for game in sb["games"]:

    #GAME DATA
    game_time = datetime.strptime(game['gameTimeUTC'], "%Y-%m-%dT%H:%M:%SZ")

    if game_time.date().day != datetime.utcnow().date().day:
        break

    print("---------------------------------------------------------")
    print("Game ID: ", game['gameId'])
    print("Game Time (UTC): ", game_time.strftime("%A, %B %d, %Y, %I:%M %p"))
    print(f"{game['awayTeam']['teamName']} ({game['awayTeam']['wins']}-{game['awayTeam']['losses']}) @ {game['homeTeam']['teamName']} ({game['homeTeam']['wins']}-{game['homeTeam']['losses']})")
    print(game['gameClock'])
    print(game['awayTeam']['score'], " - ", game['homeTeam']['score'])
    print()
    for i, (away_period, home_period) in enumerate(zip(game['awayTeam']['periods'], game['homeTeam']['periods']), start=1):
        print(f"Q{i}: {away_period['score']} - {home_period['score']}")

    #BOXSCORE
    try:
        bs = boxscore.BoxScore(game["gameId"]).get_dict()
        
        with open('boxscore.json', 'w') as f:
            json.dump(bs, f, indent=4)

        ps = bs["game"]
        keys = ['name', 'fieldGoalsMade', 'fieldGoalsAttempted', 'threePointersMade', 'points', 'assists', 'reboundsTotal', 'blocks', 'steals', 'turnovers']
        shortKeys = ["Name", "FGM", "FGA", "3PM", "P", "A", "R", "BLKs", "STLs", "TOs"]
        print("{:<20} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format(*shortKeys))

        for player in ps['awayTeam']['players'] + ps['homeTeam']['players']:
            stats = player['statistics']
            values = [player['name'], stats['fieldGoalsMade'], stats['fieldGoalsAttempted'], stats['threePointersMade'], stats['points'], stats['assists'], stats['reboundsTotal'], stats['blocks'], stats['steals'], stats['turnovers']]
            print("{:<20} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format(*values))
    except:
        print("ERROR FETCHING BOXSCORE")
        
    


print("---------------------------------------")
print("Sir Kevin Knox II")

#Grabbing individual player stats
kevinKnox = [player for player in players.get_players() if player["full_name"] == "Kevin Knox II"][0]
knoxId = kevinKnox["id"]

knoxLog = playergamelog.PlayerGameLog(player_id=knoxId)
knoxGames = knoxLog.get_dict()["resultSets"][0]["rowSet"]

for game in knoxGames:
    date = game[3]
    matchup = game[4]
    FGM = game[8]
    FGA = game[9]
    _3PM = game[11]
    P = game[24]
    A = game[21]
    R = game[22]
    BLKs = game[19]
    STLs = game[18]
    TOs = game[20]
    print(f"Date: {date}, Matchup: {matchup}, FGM: {FGM}, FGA: {FGA}, 3PM: {_3PM}, P: {P}, A: {A}, R: {R}, BLKs: {BLKs}, STLs: {STLs}, TOs: {TOs}")

    