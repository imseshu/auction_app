# 🎯 Auction App - Updated Version

## Quick Start Guide

### Option 1: Upload Both Files (Recommended)

1. **Create a Players File** (`players.txt`):
   ```
   Player Name,Batting Style,Bowling Style,Base Price
   Virat Kohli,Right Hand,NA,1000
   Rohit Sharma,Right Hand,NA,950
   MS Dhoni,Right Hand,NA,900
   Jasprit Bumrah,Right Hand,Right Arm Fast,850
   ```

2. **Create a Teams File** (`teams.txt`):
   ```
   Team Name,Budget,Color
   Mumbai Indians,5000,#1f77b4
   Chennai Super Kings,4800,#FFD700
   Royal Challengers,4500,#FF6347
   Kolkata Knight,5200,#800080
   ```

3. **Upload Both Files**:
   - Go to http://localhost:6924/
   - Click "Begin Auction"
   - Upload both files
   - Auction starts automatically!

### Option 2: Upload Players File Only

1. Create and upload `players.txt`
2. The app will redirect to a team creation page
3. Manually create teams on the webpage
4. Each team needs a name and budget
5. Auction starts automatically!

## File Formats

### players.txt
```
Player Name,Batting Style,Bowling Style,Base Price
John Doe,Right Hand,NA,500
Jane Smith,Left Hand,Right Arm Fast,600
```

### teams.txt
Text file with "Teams" sheet containing:
```
Team Name,Budget,Color
Mumbai Indians,5000,#1f77b4
Chennai Super Kings,4800,#FFD700
```

## Features

✅ Upload players dynamically (no hardcoded data)
✅ Upload teams or create manually
✅ Automatic budget tracking
✅ Auction results exported to Excel
✅ Beautiful UI with real-time updates
✅ Support for player attributes (Batting/Bowling Style)

## Running the App

```bash
# Build Docker image
docker build -t auction-app .

# Run the app
docker run -p 6924:6924 auction-app

# Access at http://localhost:6924/
```

## Error Solutions

### "Teams file not found"
→ Solution: Upload a teams.xlsx file OR use the manual team creation page

### Players not showing up
→ Solution: Ensure players.txt format is correct with comma-separated values

### Auction not starting
→ Solution: Ensure you have at least 1 player and 1 team
