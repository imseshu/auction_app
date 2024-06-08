from flask import Flask, render_template, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# Load the Excel file
def load_data():
    players_df = pd.read_excel('auction_data.xlsx', sheet_name='Players')
    teams_df = pd.read_excel('auction_data.xlsx', sheet_name='Teams')
    bids_df = pd.read_excel('auction_data.xlsx', sheet_name='Bidding Log')
    current_player_index = 0
    if os.path.exists('current_player_index.txt'):
        with open('current_player_index.txt', 'r') as file:
            current_player_index = int(file.read().strip())
    return players_df, teams_df, bids_df, current_player_index

# Save the Excel file
def save_data(players_df, teams_df, bids_df, current_player_index):
    with pd.ExcelWriter('auction_data.xlsx') as writer:
        players_df.to_excel(writer, sheet_name='Players', index=False)
        teams_df.to_excel(writer, sheet_name='Teams', index=False)
        bids_df.to_excel(writer, sheet_name='Bidding Log', index=False)
    with open('current_player_index.txt', 'w') as file:
        file.write(str(current_player_index))

@app.route('/')
def index():
    players_df, teams_df, bids_df, current_player_index = load_data()
    players = players_df.to_dict('records')
    teams = teams_df.to_dict('records')

    if current_player_index >= len(players):
        return "Auction completed!"

    current_player = players[current_player_index]
    current_bids = bids_df[bids_df['Player Name'] == current_player['Player Name']]
    if not current_bids.empty:
        current_bid = current_bids['Bid Amount'].max()
        highest_bid_team = current_bids.loc[current_bids['Bid Amount'].idxmax(), 'Team Name']
    else:
        current_bid = current_player['Base Price']
        highest_bid_team = None

    # Update player status
    for player in players:
        if not bids_df[bids_df['Player Name'] == player['Player Name']].empty:
            player['Status'] = 'Sold'
        else:
            player['Status'] = 'Pending'

    return render_template('index.html', current_player=current_player, current_bid=current_bid, highest_bid_team=highest_bid_team, teams=teams, players=players, bids_df=bids_df)

@app.route('/bid/<team_name>')
def bid(team_name):
    players_df, teams_df, bids_df, current_player_index = load_data()
    players = players_df.to_dict('records')
    current_player = players[current_player_index]
    player_name = current_player['Player Name']
    base_price = current_player['Base Price']

    # Get the current highest bid
    current_bids = bids_df[bids_df['Player Name'] == player_name]
    if not current_bids.empty:
        current_bid = current_bids['Bid Amount'].max()
    else:
        current_bid = base_price

    # Determine the bid increment
    if current_bid >= base_price * 5:
        bid_increment = 10
    else:
        bid_increment = 5

    new_bid = current_bid + bid_increment

    # Update the bidding log
    new_bid_entry = pd.DataFrame({
        'Player Name': [player_name],
        'Team Name': [team_name],
        'Bid Amount': [new_bid],
        'Status': ['Pending']
    })

    bids_df = pd.concat([bids_df, new_bid_entry], ignore_index=True)

    save_data(players_df, teams_df, bids_df, current_player_index)
    return redirect(url_for('index'))

@app.route('/finalize')
def finalize():
    players_df, teams_df, bids_df, current_player_index = load_data()
    players = players_df.to_dict('records')

    current_player = players[current_player_index]
    player_name = current_player['Player Name']

    # Get the highest bid for the current player
    current_bids = bids_df[bids_df['Player Name'] == player_name]
    if not current_bids.empty:
        highest_bid = current_bids.iloc[current_bids['Bid Amount'].idxmax()]
        winning_team = highest_bid['Team Name']
        bid_amount = highest_bid['Bid Amount']

        # Update the teams data
        team_index = teams_df[teams_df['Team Name'] == winning_team].index[0]
        teams_df.at[team_index, 'Players'] = str(teams_df.at[team_index, 'Players']) + ',' + player_name
        teams_df.at[team_index, 'Budget'] -= bid_amount

        # Update the bid status
        bids_df.loc[(bids_df['Player Name'] == player_name) & (bids_df['Team Name'] == winning_team), 'Status'] = 'Won'

        save_data(players_df, teams_df, bids_df, current_player_index)
        current_player_index += 1

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
