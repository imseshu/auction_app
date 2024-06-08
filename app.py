from flask import Flask, render_template, request, send_file
import pandas as pd
from datetime import datetime
import os

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


# Save auction results to Excel file
def save_results_to_excel(teams):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'auction_results_{timestamp}.xlsx'
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

    for team in teams:
        team_name = team['Team Name']
        team_df = pd.DataFrame(team['Players'])
        team_df.to_excel(writer, sheet_name=team_name, index=False)

    writer._save()
    return output_file


# Load the initial data
players, teams = load_data_from_excel('auction_data.xlsx')

# Auction variables
current_player_index = 0
current_player = players[current_player_index]
current_bid = current_player['Base Price']
highest_bid_team = None
last_bid_team = None
auction_complete = False
results_file = None
first_bid = 0
remaining = {}
for team in teams:
    remaining[team['Team Name']] = team['Budget']

@app.route('/')
def index():
    global current_player, current_bid, highest_bid_team, auction_complete, results_file
    return render_template('index.html',
                           current_player=current_player,
                           current_bid=current_bid,
                           highest_bid_team=highest_bid_team,
                           teams=teams,
                           players=players,
                           auction_complete=auction_complete,
                           results_file=results_file,
                           remaining=remaining)


@app.route('/bid/<team_name>', methods=['GET'])
def bid(team_name):
    global current_bid, highest_bid_team, current_player, last_bid_team, first_bid, remaining

    if last_bid_team == team_name:
        return index()  # Prevent the same team from bidding twice consecutively

    if current_bid == current_player['Base Price']:
        if first_bid == 0:
            current_bid += 0
            first_bid = 1
        else:
            if remaining[team_name] >= current_bid + 10:
                current_bid += 10  # Initial increment
            else:
                return index()
    else:
        if current_bid < 2 * current_player['Base Price'] and remaining[team_name] >= current_bid + 10:
            increment = 10
        else:
            if remaining[team_name] >= current_bid + 20:
                increment = 20
            else:
                return index()
        current_bid += increment

    highest_bid_team = team_name
    last_bid_team = team_name

    return index()


@app.route('/finalize', methods=['GET'])
def finalize():
    global current_player_index, current_player, current_bid, highest_bid_team, auction_complete, results_file, last_bid_team, first_bid, remaining
    first_bid=0

    if highest_bid_team:
        for team in teams:
            if team['Team Name'] == highest_bid_team:
                team['Players'].append({'name': current_player['Player Name'], 'bid': current_bid})
                current_player['Status'] = 'Sold'
                remaining[team['Team Name']] -= current_bid
                current_player['Final Price'] = current_bid
                current_player['Sold To'] = highest_bid_team  # Record the team the player was sold to
                break
    else:
        current_player['Status'] = 'Unsold'
        current_player['Final Price'] = '-'
        current_player['Sold To'] = '-'  # Indicate no team

    # Move to the next player
    current_player_index += 1
    if current_player_index < len(players):
        current_player = players[current_player_index]
        current_bid = current_player['Base Price']
        highest_bid_team = None
        last_bid_team = None
    else:
        current_player = None
        auction_complete = True
        results_file = save_results_to_excel(teams)  # Save results to Excel

    return index()


@app.route('/download', methods=['GET'])
def download():
    return send_file(results_file, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
