# NBA Fantasy & Live Data Project

## Overview

This project is a **full-stack** application that fetches **NBA data** from the official [`nba_api`](https://github.com/swar/nba_api) library, stores it in a local SQLite database, and serves it through a **Flask** backend for a **React** frontend. 

**Main Features**:
1. **Data Ingestion**: Pulls official NBA team info, rosters, and live scoreboard data, storing them in a local `fantasy.db`.
2. **Fantasy Player Stats**: Random or placeholder stats for each player (for demonstration), used by a simple “recommendation” formula.  
3. **Live Scores**: Real-time scores from [`nba_api.live.nba.endpoints.scoreboard`](https://github.com/swar/nba_api#nba-live-data), showing current NBA games in progress or final scores.
4. **Flask API**: Exposes endpoints to retrieve players’ data, recommendations, teams, and live scores.  
5. **React Frontend**: Displays a table of recommended players, a list of teams, and live scoreboard data.

---

## Why This Project?

- **Full-Stack**: Showcases the synergy between Python (Flask, `nba_api`), a database (SQLite), and a React UI.
- **Practical**: Integrates real NBA data (teams & daily scoreboard) instead of mocked placeholders only.
- **Extendable**: You can easily add advanced stats, trend tracking, or a player search to highlight further analytics or a fantasy sports scenario.

**Note**: Some player stats are currently populated with **random** values (points, rebounds, etc.) to simulate scoring for a fantasy-like recommendation feature. Live scoreboard data, however, is **real** from official NBA endpoints.

---

## Tech Stack

1. **Python 3.7+**  
2. **Flask** (for the API server)  
3. **SQLite** (for local data storage)  
4. **`nba_api`** (official Python client for NBA.com stats & live data)  
5. **React** (front-end library for UI)

---

## How It Works

1. **Data Ingestion**  
   - `data_ingestion.py` creates/updates `fantasy.db`.  
   - **Steps**:  
     1. Fetch **all** NBA teams from `commonteamyears.CommonTeamYears()` (or `nba_api.stats.static.teams` in some versions).  
     2. For selected team IDs (Lakers, Warriors, Sixers, etc.), fetch rosters with `commonteamroster.CommonTeamRoster`.  
     3. **Random Stats**: Insert random points/rebounds/assists for each player to produce non-zero recommendation scores.  
     4. Fetch **live scoreboard** from `nba_api.live.nba.endpoints.scoreboard.ScoreBoard`, storing real-time game data.  
   - The result is a local DB with `nba_teams`, `player_stats`, and `nba_live_scores`.

2. **Flask Backend** (`app.py`)  
   - Exposes routes:
     - `GET /players` – All players in `player_stats`.
     - `GET /recommendations` – Returns top players based on a simple fantasy formula. (Sort by `(points + rebounds*1.2 + assists*1.5 + steals*3 + blocks*3)`.)
     - `GET /teams` – All teams from `nba_teams`.
     - `GET /livescores` – Real-time scoreboard from `nba_live_scores`.
   - Runs on **port 5000** by default.  

3. **React Frontend** (`App.js`)  
   - Connects to `<http://localhost:5000>` to fetch:
     1. **Recommendations**: Displays top 10 players in a table.  
     2. **Teams**: Simple list of team names and IDs.  
     3. **Live Scores**: A scoreboard table with home/away teams, scores, and status.  
   - Runs on **port 3000**.  
   - Shows how to handle cross-origin requests (CORS) and display data in a user-friendly way.

---

## Setup & Installation

1. **Clone This Repo**  
   ```bash
   git clone https://github.com/<YourUsername>/<YourRepoName>.git
   cd <YourRepoName>
