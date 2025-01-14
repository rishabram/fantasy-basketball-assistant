# data_ingestion.py

import sqlite3
import random
import pandas as pd

from nba_api.stats.endpoints import commonteamyears, commonteamroster
from nba_api.live.nba.endpoints import scoreboard as live_scoreboard

def create_db():
    """
    Create or verify the SQLite schema: 'nba_teams', 'player_stats', 'nba_live_scores'.
    """
    conn = sqlite3.connect('fantasy.db')
    cur = conn.cursor()

    # TEAMS
    cur.execute('''
        CREATE TABLE IF NOT EXISTS nba_teams (
            team_id INTEGER PRIMARY KEY,
            team_name TEXT,
            team_code TEXT
        );
    ''')

    # PLAYERS
    cur.execute('''
        CREATE TABLE IF NOT EXISTS player_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT,
            team TEXT,
            position TEXT,
            points REAL,
            rebounds REAL,
            assists REAL,
            steals REAL,
            blocks REAL,
            fg_percentage REAL,
            ft_percentage REAL,
            threepm REAL,
            injury_status TEXT,
            next_opponent TEXT
        );
    ''')

    # LIVE SCORES
    cur.execute('''
        CREATE TABLE IF NOT EXISTS nba_live_scores (
            game_id TEXT PRIMARY KEY,
            home_team TEXT,
            away_team TEXT,
            home_score INTEGER,
            away_score INTEGER,
            game_status TEXT
        );
    ''')

    conn.commit()
    conn.close()

def load_teams():
    """
    Calls commonteamyears.CommonTeamYears() =>
    DataFrame with columns e.g. ['TEAM_ID','MIN_YEAR','MAX_YEAR','ABBREVIATION','LEAGUE_ID'].
    We'll store:
      - team_id
      - team_name = row['ABBREVIATION']
      - team_code = "MIN_YEAR-MAX_YEAR" as extra reference
    """
    cty = commonteamyears.CommonTeamYears()
    df = cty.get_data_frames()[0]

    print("Columns from commonteamyears:", df.columns.tolist())

    conn = sqlite3.connect('fantasy.db')
    cur = conn.cursor()

    # Clear old data
    cur.execute("DELETE FROM nba_teams;")

    for _, row in df.iterrows():
        team_id = row['TEAM_ID']
        team_name = row['ABBREVIATION']
        team_code = f"{row['MIN_YEAR']}-{row['MAX_YEAR']}"
        cur.execute('''
            INSERT INTO nba_teams (team_id, team_name, team_code)
            VALUES (?, ?, ?)
        ''', (team_id, team_name, team_code))

    conn.commit()
    conn.close()
    print(f"Inserted {len(df)} rows into nba_teams from commonteamyears.")

def load_team_roster(team_id):
    """
    For a specific team_id, calls commonteamroster (season='2022-23') => roster DataFrame.
    Then we insert random stats into player_stats so we can see non-zero "recommendations" scores.
    """
    roster = commonteamroster.CommonTeamRoster(team_id=team_id, season='2022-23')
    df = roster.get_data_frames()[0]

    conn = sqlite3.connect('fantasy.db')
    cur = conn.cursor()

    for _, row in df.iterrows():
        name = row['PLAYER']
        position = row['POSITION']
        team_label = f"TEAM_{team_id}"

        # Random stats so "recommendations" won't be zero
        points = random.uniform(5, 30)
        rebounds = random.uniform(1, 10)
        assists = random.uniform(0, 8)
        steals = random.uniform(0, 3)
        blocks = random.uniform(0, 2)
        fg_percent = random.uniform(0.3, 0.6)
        ft_percent = random.uniform(0.5, 0.9)
        threepm = random.uniform(0, 5)
        injury_status = "Healthy"
        next_opponent = "Unknown"

        cur.execute('''
            INSERT INTO player_stats (
                player_name, team, position,
                points, rebounds, assists, steals, blocks,
                fg_percentage, ft_percentage, threepm,
                injury_status, next_opponent
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, team_label, position,
            points, rebounds, assists, steals, blocks,
            fg_percent, ft_percent, threepm,
            injury_status, next_opponent
        ))

    conn.commit()
    conn.close()
    print(f"Inserted {len(df)} players for team_id={team_id} into player_stats.")

def load_daily_scoreboard():
    """
    Fetch today's scoreboard from nba_api.live.nba.endpoints.scoreboard.ScoreBoard().
    Insert into nba_live_scores.
    """
    sb = live_scoreboard.ScoreBoard()
    data = sb.get_dict()
    games = data.get('scoreboard', {}).get('games', [])

    conn = sqlite3.connect('fantasy.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM nba_live_scores;")

    for g in games:
        game_id = g['gameId']
        home_team = g['homeTeam']['teamName']
        away_team = g['awayTeam']['teamName']
        home_score = g['homeTeam']['score']
        away_score = g['awayTeam']['score']
        game_status = g['gameStatusText']

        cur.execute('''
            INSERT OR REPLACE INTO nba_live_scores (
                game_id, home_team, away_team,
                home_score, away_score, game_status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (game_id, home_team, away_team, home_score, away_score, game_status))

    conn.commit()
    conn.close()
    print(f"Inserted {len(games)} games into nba_live_scores.")

if __name__ == "__main__":
    create_db()

    # Load all NBA teams
    load_teams()

    # Load rosters for a few example teams (Lakers, Warriors, Sixers, etc.)
    for tid in [1610612747, 1610612744, 1610612755]:
        load_team_roster(tid)

    # Load today's scoreboard
    load_daily_scoreboard()

    print("Data ingestion completed successfully!")



