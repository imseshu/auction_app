# 🎯 Player Auction App# auction_app

A beautiful, interactive web application for running player auctions using Flask. Upload player and team data dynamically, manage real-time bidding, and export results.

## ✨ Features

- **Dynamic File Uploads**: Upload players and teams as simple text files
- **Real-time Bidding**: Live auction interface with team-based bidding
- **Budget Tracking**: Automatic budget management for each team
- **Flexible Team Creation**: Upload teams or create them manually on the app
- **Player Attributes**: Support for Batting Style, Bowling Style, and Base Price
- **Export Results**: Automatically generate Excel files with auction results
- **Beautiful UI**: Modern, responsive interface with color-coded teams

## 📋 Quick Start

### Prerequisites
- Docker and Docker Desktop installed
- Git

### Option 1: Upload Both Files (Recommended)

1. **Create `players.txt`**:
   ```
   Player Name,Batting Style,Bowling Style,Base Price
   Virat Kohli,Right Hand,NA,1000
   Rohit Sharma,Right Hand,NA,950
   MS Dhoni,Right Hand,NA,900
   Jasprit Bumrah,Right Hand,Right Arm Fast,850
   ```

2. **Create `teams.txt`**:
   ```
   Team Name,Budget,Color
   Mumbai Indians,5000,#1f77b4
   Chennai Super Kings,4800,#FFD700
   Royal Challengers,4500,#FF6347
   Kolkata Knight,5200,#800080
   Delhi Capitals,4900,#003DA5
   ```

3. **Run the Application**:
   ```bash
   # Clone the repo
   git clone https://github.com/imseshu/auction_app.git
   cd auction_app

   # Build Docker image
   docker build -t auction-app .

   # Run the app
   docker run -p 6924:6924 auction-app

   # Open browser to http://localhost:6924/
   ```

4. **Upload Files**:
   - Click "Begin Auction"
   - Upload both `players.txt` and `teams.txt`
   - Auction starts automatically!

### Option 2: Upload Players Only

1. Create `players.txt` file
2. Upload the file
3. Create teams manually on the team creation page
4. Auction starts!

## 📁 File Formats

### players.txt
Required format for player data:
```
Player Name,Batting Style,Bowling Style,Base Price
Virat Kohli,Right Hand,NA,1000
Rohit Sharma,Right Hand,NA,950
Jasprit Bumrah,Right Hand,Right Arm Fast,850
Ravindra Jadeja,Left Hand,Left Arm Orthodox,750
```

**Fields:**
- `Player Name`: Full name of the player
- `Batting Style`: Right Hand / Left Hand
- `Bowling Style`: Bowling type (e.g., Right Arm Fast, Left Arm Orthodox) or NA
- `Base Price`: Starting price for auction

### teams.txt
Required format for team data:
```
Team Name,Budget,Color
Mumbai Indians,5000,#1f77b4
Chennai Super Kings,4800,#FFD700
Royal Challengers,4500,#FF6347
Kolkata Knight,5200,#800080
Delhi Capitals,4900,#003DA5
Punjab Kings,5100,#FF0000
Rajasthan Royals,4700,#0099CC
Sunrisers Hyderabad,5000,#FF8C00
```

**Fields:**
- `Team Name`: Name of the team
- `Budget`: Total budget for purchases
- `Color`: Hex color code for UI (optional, defaults to white)

## 🎮 How to Use the Auction

1. **View Current Player**: Top section shows the current player up for auction
2. **View Current Bid**: Middle shows the current bid amount
3. **Place Bids**: Click on team buttons to place bids
4. **Finalize Bid**: Click "Finalize Current Bid" when done bidding
5. **Track Progress**: View all players and team purchases in real-time
6. **Export Results**: Download results as Excel file when auction completes

## 🐳 Docker Setup

### Build Image
```bash
docker build -t auction-app .
```

### Run Container
```bash
docker run -p 6924:6924 auction-app
```

### Access Application
Open browser: `http://localhost:6924/`

## 📦 Project Structure

```
auction_app/
├── app.py                      # Flask application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── README.md                   # This file
├── players_sample.txt          # Sample player data
├── teams_sample.txt            # Sample team data
├── static/
│   └── images/                 # Application images
│       ├── background.jpg
│       └── icon.png
├── templates/
│   ├── welcome.html           # Welcome page
│   ├── upload.html            # File upload page
│   ├── create_teams.html      # Manual team creation
│   └── index.html             # Main auction interface
└── .gitignore                 # Git configuration
```

## 🔧 Dependencies

See `requirements.txt`:
- Flask 2.3.3
- Pandas 2.1.4
- NumPy 1.26.2
- OpenPyXL 3.1.2
- XlsxWriter 3.1.2

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Teams file not found | Upload a `teams.txt` file or use the manual team creation page |
| Players not showing | Ensure `players.txt` format is correct with comma-separated values |
| Auction not starting | Verify you have at least 1 player and 1 team |
| Docker won't start | Ensure Docker Desktop is running |
| Port 6924 already in use | Change port: `docker run -p 8000:6924 auction-app` |

## 🚀 Features in Detail

### Dynamic Player Upload
- No hardcoded player data
- Easy CSV-like text format
- Support for player attributes

### Flexible Team Management
- Upload teams from file
- Create teams manually in the app
- Automatic color assignment if not provided

### Real-time Bidding
- Increment-based bidding (50 units, then 100)
- Budget validation
- Prevent consecutive bids from same team
- Live budget tracking

### Results Export
- Automatically generates Excel file
- One sheet per team
- Lists all players and purchase prices

## 📝 Example Auction Flow

1. **Upload Files** → Select players.txt and teams.txt
2. **View Current Player** → Virat Kohli (Base Price: 1000)
3. **Teams Bid** → Click team buttons to place bids
4. **Finalize** → Click "Finalize Current Bid"
5. **Next Player** → Auction moves to next player
6. **Repeat** → Continue until all players sold
7. **Export** → Download results as Excel file

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created by [imseshu](https://github.com/imseshu)

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Happy Auctioning! 🎉**
