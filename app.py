from flask import Flask, render_template, request, send_file, redirect, url_for
import pandas as pd
from datetime import datetime
import os, sys
import importlib

app = Flask(__name__)


# Load data from Excel file
def parse_text_file(file_path):
    """Parse text file with format: Player Name,Batting Style,Bowling Style,Base Price"""
    players = []
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:  # Skip header
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) >= 4:
                        players.append({
                            'Player Name': parts[0].strip(),
                            'Batting Style': parts[1].strip(),
                            'Bowling Style': parts[2].strip(),
                            'Base Price': int(parts[3].strip()),
                            'Status': 'Pending',
                            'Final Price': '-',
                            'Sold To': '-'
                        })
    except Exception as e:
        print(f"Error parsing file: {e}")
    return players


def parse_teams_file(file_path):
    """Parse text file with format: Team Name,Budget,Color"""
    teams = []
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:  # Skip header
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        teams.append({
                            'Team Name': parts[0].strip(),
                            'Budget': int(parts[1].strip()),
                            'Color': parts[2].strip() if len(parts) > 2 else '#FFFFFF',
                            'Players': []
                        })
    except Exception as e:
        print(f"Error parsing teams file: {e}")
    return teams


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


@app.route('/')
def welcome():
    return render_template('welcome.html')


UPLOAD_FOLDER = './'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def save_uploaded_file(file, filename):
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global players, teams, current_player_index, current_player, current_bid, highest_bid_team, auction_complete, results_file, remaining, first_bid, last_bid_team
    
    if request.method == 'POST':
        # Check for players file
        if 'players_file' not in request.files:
            return "No players file uploaded"
        
        players_file = request.files['players_file']
        
        if players_file.filename == '':
            return "No players file selected"
        
        # Check for teams file (optional)
        teams_file = request.files.get('teams_file') if 'teams_file' in request.files else None
        
        if players_file:
            # Save players file
            save_uploaded_file(players_file, 'players.txt')
            players = parse_text_file('players.txt')
            
            # Load teams from uploaded file or use default
            if teams_file and teams_file.filename != '':
                save_uploaded_file(teams_file, 'teams.txt')
                teams = parse_teams_file('teams.txt')
            elif os.path.exists('teams.txt'):
                teams = parse_teams_file('teams.txt')
            else:
                # Create default teams if no file provided
                return redirect(url_for('create_teams', num_players=len(players)))
            
            # Initialize auction variables
            current_player_index = 0
            current_player = players[0] if players else None
            current_bid = current_player['Base Price'] if current_player else 0
            highest_bid_team = None
            last_bid_team = None
            auction_complete = False
            results_file = None
            first_bid = 0
            
            # Initialize remaining budget
            remaining = {}
            for team in teams:
                remaining[team['Team Name']] = team['Budget']
            
            return redirect('/auction')
    
    return render_template('upload.html')


@app.route('/create_teams/<int:num_players>', methods=['GET', 'POST'])
def create_teams(num_players):
    global teams
    
    if request.method == 'POST':
        # Get team data from form
        team_names = request.form.getlist('team_name[]')
        team_budgets = request.form.getlist('team_budget[]')
        
        teams = []
        for name, budget in zip(team_names, team_budgets):
            if name and budget:
                teams.append({
                    'Team Name': name.strip(),
                    'Budget': int(budget),
                    'Players': [],
                    'Color': f'#{hash(name) % 0x1000000:06x}'
                })
        
        if teams:
            return redirect('/auction')
        else:
            return "Please provide at least one team"
    
    return render_template('create_teams.html', num_players=num_players)


@app.route('/auction')
def index():
    global current_player, current_bid, highest_bid_team, highest_bid_team_color, auction_complete, results_file, remaining, scrolling
    
    return render_template('index.html',
                           current_player=current_player,
                           current_bid=current_bid,
                           highest_bid_team=highest_bid_team,
                           highest_bid_team_color=highest_bid_team_color,
                           teams=teams,
                           players=players,
                           auction_complete=auction_complete,
                           results_file=results_file,
                           remaining=remaining,
                           scrolling=scrolling)


# Load the initial data
players = []
teams = []
current_player_index = 0
current_player = None
current_bid = 0
highest_bid_team = None
last_bid_team = None
auction_complete = False
results_file = None
first_bid = 0
scrolling = ""
remaining = {}
highest_bid_team_color = "#FFFFFF"
@app.route('/bid/<team_name>', methods=['GET'])
def bid(team_name):
    global current_bid, highest_bid_team, highest_bid_team_color, current_player, last_bid_team, first_bid, remaining

    if last_bid_team == team_name:
        return index()  # Prevent the same team from bidding twice consecutively

    if current_bid == current_player['Base Price']:
        if first_bid == 0:
            current_bid += 0
            first_bid = 1
        else:
            if remaining[team_name] >= current_bid + 50:
                current_bid += 50  # Initial increment
            else:
                return index()
    else:
        if current_bid < 2 * current_player['Base Price'] and remaining[team_name] >= current_bid + 50:
            increment = 50
        else:
            if remaining[team_name] >= current_bid + 100:
                increment = 100
            else:
                return index()
        current_bid += increment

    highest_bid_team = team_name
    last_bid_team = team_name

    for team in teams:
        if team['Team Name'] == highest_bid_team:
            highest_bid_team_color = team['Color']
            break

    return index()


@app.route('/finalize', methods=['GET'])
def finalize():
    global current_player_index, current_player, current_bid, highest_bid_team, auction_complete, results_file, last_bid_team, first_bid, remaining, scrolling
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
    scrolling = ""
    for team in teams:
        scrolling += team['Team Name'] + " (Remaining Purse: " + str(remaining[team['Team Name']]) + " U) Players Purchased - "
        for player in team['Players']:
            scrolling += player['name'] + " " + str(player['bid']) + " U, "
        scrolling += " | "
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
    app.run(host='0.0.0.0', port=6924, debug=True)
