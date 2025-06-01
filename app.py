from flask import Flask, jsonify, request, abort
import json
import os
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

DATA_FILE = "data.json"
BUDGET = 500_000_000

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)
    
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({
        "error": e.name,
        "message": e.description
    }), e.code

@app.route('/players', methods=['GET'])
def list_players():
    data = load_data()
    return jsonify({
        "all_players": data["all_players"],
        "my_team": data["my_team"],
        "budget": data["budget"]
    })

@app.route('/buy/<int:player_id>', methods=['POST'])
def buy_player(player_id):
    data = load_data()
    
    player = next((p for p in data["all_players"] if p["id"] == player_id), None)
    if not player:
        abort(404, description="Player not found")
    
    if player in data["my_team"]:
        abort(400, description="Player already in your team")
    
    if data["budget"] < player["price"]:
        abort(400, description="Insufficient budget")
    
    data["my_team"].append(player)
    data["budget"] -= player["price"]
    save_data(data)
    
    return jsonify({"message": f"Successfully bought {player['name']}", "budget": data["budget"]})

@app.route('/sell/<int:player_id>', methods=['POST'])
def sell_player(player_id):
    data = load_data()
    
    player = next((p for p in data["my_team"] if p["id"] == player_id), None)
    if not player:
        abort(404, description="Player not found in your team")
    
    data["my_team"].remove(player)
    data["budget"] += player["price"]
    save_data(data)
    
    return jsonify({"message": f"Sold {player['name']}", "budget": data["budget"]})

@app.route('/team/value', methods=['GET'])
def team_value():
    data = load_data()
    total_value = sum(p["price"] for p in data["my_team"])
    return jsonify({
        "team_value": total_value,
        "remaining_budget": data["budget"]
    })

if __name__ == '__main__':
    # Initialize sample data if not exists
    if not os.path.exists(DATA_FILE):
        load_data()
    app.run(debug=True)