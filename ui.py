import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime

# Config
st.set_page_config(layout="wide", page_title="⚽ Fantasy Football Manager", page_icon="⚽")
API_URL = "http://127.0.0.1:5000"  # Flask API URL

# Custom CSS for cards
st.markdown("""
<style>
.player-card {
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    transition: 0.3s;
}
.player-card:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}
.team-card {
    background-color: black;
    border-left: 5px solid #ff4b4b;
}
</style>
""", unsafe_allow_html=True)

# Helper functions
def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        return response.json() if response.status_code == 200 else None
    except:
        st.error("Failed to connect to API. Is Flask running?")
        return None

def post_data(endpoint):
    try:
        response = requests.post(f"{API_URL}/{endpoint}")
        return response.json() if response.status_code == 200 else None
    except:
        return None

# Initialize session state
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

# Header
st.title("⚽ Fantasy Football Manager")
st.caption(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")

# Dashboard columns
col1, col2 = st.columns([3, 2])

with col1:
    st.header("💰 Budget & Team Value")
    budget_data = fetch_data("team/value")
    
    if budget_data:
        cols = st.columns(2)
        with cols[0]:
            st.metric("Remaining Budget", f"${budget_data['remaining_budget']:,}")
        with cols[1]:
            st.metric("Team Value", f"${budget_data['team_value']:,}")
        
        # Budget progress bar
        budget_used = (budget_data['team_value'] / 
                      (budget_data['team_value'] + budget_data['remaining_budget'])) * 100
        st.progress(int(budget_used))

with col2:
    st.header("🔍 Player Search")
    search_term = st.text_input("Search by name or club", key="search")
    position_filter = st.multiselect(
        "Filter by position",
        ["GK", "DEF", "MID", "FW"],
        default=["GK", "DEF", "MID", "FW"]
    )

# Player marketplace
st.header("🏆 Player list")
data = fetch_data("players")

if data:
    # Convert to DataFrame for filtering
    df = pd.DataFrame(data['all_players'])
    
    # Apply filters
    if search_term:
        df = df[df['name'].str.contains(search_term, case=False) | 
                df['club'].str.contains(search_term, case=False)]
    
    if position_filter:
        df = df[df['position'].isin(position_filter)]
    
    # Display players
    for _, player in df.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.subheader(f"{player['name']} ({player['position']})")
                st.caption(f"🏟️ {player['club']} | 💵 ${player['price']:,}")
                
                # Stats radar chart
                stats = player['stats']
                st.write(f"""
                🏃‍ Pace: {stats['pace']} | ⚽ Shooting: {stats['shooting']}  
                🎯 Passing: {stats['passing']} | ✨ Dribbling: {stats['dribbling']}  
                🛡️ Defending: {stats['defending']} | 💪 Physical: {stats['physical']}
                """)
            
            with col3:
                if player['id'] in [p['id'] for p in data['my_team']]:
                    if st.button(f"🚫 Sell {player['name'].split()[0]}", key=f"sell_{player['id']}"):
                        result = post_data(f"sell/{player['id']}")
                        if result:
                            st.success(result['message'])
                            st.session_state.last_update = datetime.now()
                            st.rerun()
                else:
                    if st.button(f"🛒 Buy {player['name'].split()[0]}", key=f"buy_{player['id']}"):
                        result = post_data(f"buy/{player['id']}")
                        if result:
                            st.success(result['message'])
                            st.session_state.last_update = datetime.now()
                            st.rerun()

            st.markdown("---")

    # My Team section
    st.header("🌟 My Squad")
    if data['my_team']:
        # Categorize players by position
        positions = {
            "GK": [],
            "DEF": [],
            "MID": [],
            "FW": []
        }
        
        for player in data['my_team']:
            pos = player['position']
            if pos in ["CB", "LB", "RB", "LWB", "RWB"]:
                positions["DEF"].append(player)
            elif pos in ["CM", "CDM", "CAM", "LM", "RM"]:
                positions["MID"].append(player)
            elif pos in ["ST", "CF", "LW", "RW"]:
                positions["FW"].append(player)
            else:
                positions["GK"].append(player)
        
        # Display players in simple cards by position group
        for position_group, players in positions.items():
            if players:
                st.subheader(f"{position_group}s ({len(players)})")
                for player in players:
                    st.markdown(f"""
                    <div class="player-card team-card">
                        <b>{player['name']}</b><br>
                        {player['position']} | {player['club']}<br>
                        ${player['price']:,} | ⭐ {sum(player['stats'].values())//6} avg
                    </div>
                    """, unsafe_allow_html=True)
        
        # Export options
        st.download_button(
            label="📤 Export Team to CSV",
            data=pd.DataFrame(data['my_team']).to_csv(index=False),
            file_name="my_fantasy_team.csv",
            mime="text/csv"
        )
    else:
        st.warning("Your team is empty! Buy players from the marketplace above.")

else:
    st.error("Failed to load player data. Please try again later.")