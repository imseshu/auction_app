from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load data from Excel file
def load_data_from_excel(file_path):
    players_df = pd.read_excel(file_path, sheet_name='Players')
    teams_df = pd.read_excel(file_path, sheet_name='Teams')
    players = players_df.to_dict(orient='records')
    teams = teams_df.to_dict(orient='records')

    # Initialize the players in each team
    for team in teams:
        team['Players'] = []

    return players, teams

# Load the initial data
players, teams = load_data_from_excel('/mnt/data/auction_data.xlsx')

# Auction variables
current_player_index = 0
current_player = players[current_player_index]
current_bid = current_player['Base Price']
highest_bid_team = None

@app.route('/')
def index():
    global current_player, current_bid, highest_bid_team
    return render_template('index.html',
                           current_player=current_player,
                           current_bid=current_bid,
                           highest_bid_team=highest_bid_team,
                           teams=teams,
                           players=players)

@app.route('/bid/<team_name>', methods=['GET'])
def bid(team_name):
    global current_bid, highest_bid_team
    current_bid += 1  # Increment bid by 1
    highest_bid_team = team_name
    return index()

@app.route('/finalize', methods=['GET'])
def finalize():
    global current_player_index, current_player, current_bid, highest_bid_team

    if highest_bid_team:
        for team in teams:
            if team['Team Name'] == highest_bid_team:
                team['Players'].append({'name': current_player['Player Name'], 'bid': current_bid})
                break

    # Move to the next player
    current_player_index += 1
    if current_player_index < len(players):
        current_player = players[current_player_index]
        current_bid = current_player['Base Price']
        highest_bid_team = None
    else:
        current_player = None

    return index()

if __name__ == '__main__':
    app.run(debug=True)
