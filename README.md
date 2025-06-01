# Fantasy Football Manager

## Overview
Fantasy Football Manager is a full-stack web application that enables users to build and manage a virtual football team. The system consists of a Flask backend API that handles data operations, where data regarding players is loaded from a data.json file and a Streamlit frontend that provides an interactive user interface. Users can browse players, manage their squad within a set budget, and track team statistics.

## Key Features
1. **Player Management**
   - Browse a database of 50+ professional football players
   - Filter players by name, club, or position (GK, DEF, MID, FW)
   - View detailed player statistics (pace, shooting, passing, etc.)

2. **Team Operations**
   - Add players to your squad within a $500 million budget
   - Remove players from your team
   - Automatic budget calculation after each transaction

3. **Data Visualization**
   - Real-time budget tracking with progress bar
   - Team value calculation
   - Player statistics display

4. **Data Export**
   - Export team roster as CSV file

## Technical Architecture

### Backend (Flask API)
- **Framework**: Flask 2.0
- **Data Storage**: JSON file (data.json)
- **Endpoints**:
  - `GET /players` - Retrieve all players and current team
  - `POST /buy/<player_id>` - Add player to team
  - `POST /sell/<player_id>` - Remove player from team
  - `GET /team/value` - Get current team value and budget

### Frontend (Streamlit)
- **Framework**: Streamlit 1.10
- **UI Components**:
  - Interactive player cards
  - Search and filter functionality
  - Budget tracking dashboard
  - Team management interface

## Project Structure
```
fantasy-football-manager/
├── app.py           # Flask backend
├── data.json        # Player database
├── ui.py            # Streamlit frontend (to be created next)
└── requirements.txt
```

## Installation Guide

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fantasy-football-manager.git
   cd fantasy-football-manager
   ```
### 2. Install Dependencies

Make sure you're in a virtual environment (optional but recommended):

```bash
pip install -r requirements.txt
```

### 3. Run the Backend (Flask)

```bash
python app.py
```

The API will be running at `http://127.0.0.1:5000`.

### 4. Run the Frontend (Streamlit)

In a new terminal:

```bash
streamlit run ui.py
```

This will open up the user interface in your browser.
