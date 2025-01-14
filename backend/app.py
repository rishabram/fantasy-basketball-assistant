from flask import Flask, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin from React

def get_db_connection():
    conn = sqlite3.connect('fantasy.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/players', methods=['GET'])
def get_players():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM player_stats').fetchall()
    conn.close()
    players = [dict(row) for row in rows]
    return jsonify(players)

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM player_stats').fetchall()
    conn.close()

    def calculate_score(p):
        points = p.get('points', 0)
        rebounds = p.get('rebounds', 0)
        assists = p.get('assists', 0)
        steals = p.get('steals', 0)
        blocks = p.get('blocks', 0)
        injury = p.get('injury_status', 'Healthy')

        score = (
            points * 1.0 +
            rebounds * 1.2 +
            assists * 1.5 +
            steals * 3 +
            blocks * 3
        )
        if injury == 'Out':
            score -= 50
        elif injury == 'Day-to-day':
            score -= 10
        return score

    players = []
    for row in rows:
        p = dict(row)
        p['score'] = calculate_score(p)
        players.append(p)

    # Sort descending by 'score'
    players.sort(key=lambda x: x['score'], reverse=True)

    # Return top 10
    return jsonify(players[:10])

@app.route('/teams', methods=['GET'])
def get_teams():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM nba_teams').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/livescores', methods=['GET'])
def get_livescores():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM nba_live_scores').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)  # Explicitly set host and port


