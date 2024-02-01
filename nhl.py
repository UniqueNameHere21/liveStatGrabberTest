import requests
from pprint import pprint

# Define the base URL
base_url = "https://api-web.nhle.com/v1"

# Append the endpoint for Sidney Crosby's game log
player_id = "8471675"  # Sidney Crosby's player ID
season = "20232024"  # Season
game_type = "2"  # Regular season
game_log_endpoint = f"/player/{player_id}/game-log/{season}/{game_type}"

# Construct the full URL
full_url = f"{base_url}{game_log_endpoint}"

# Make a GET request to the NHL API
response = requests.get(full_url)

# Parse the response to JSON
data = response.json()

# Print the game log data
# Iterate over the gameLog list
for game in data['gameLog']:
    # Print the desired fields for each game in a single line with shorthand for each header
    print(f"M: {game['commonName']['default']} vs {game['opponentCommonName']['default']}, D: {game['gameDate']}, G: {game['goals']}, A: {game['assists']}, P: {game['points']}, HTs: {game.get('hits', 'N/A')}, S: {game['shots']}, PIM: {game['pim']}, B: {game.get('blocks', 'N/A')}")