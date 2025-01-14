import React, { useEffect, useState } from 'react';

function App() {
  const [players, setPlayers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [liveScores, setLiveScores] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/recommendations')
      .then(res => res.json())
      .then(data => setPlayers(data))
      .catch(err => console.error("Error fetching /recommendations:", err));
  }, []);

  useEffect(() => {
    fetch('http://localhost:5000/teams')
      .then(res => res.json())
      .then(data => setTeams(data))
      .catch(err => console.error("Error fetching /teams:", err));
  }, []);

  useEffect(() => {
    fetch('http://localhost:5000/livescores')
      .then(res => res.json())
      .then(data => setLiveScores(data))
      .catch(err => console.error("Error fetching /livescores:", err));
  }, []);

  return (
    <div style={{ margin: '2rem' }}>
      <h1>Fantasy Basketball Recommendations (nba_api)</h1>
      <table border="1" cellPadding="6" cellSpacing="0">
        <thead>
          <tr>
            <th>Player</th>
            <th>Team</th>
            <th>Position</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {players.map((p, idx) => (
            <tr key={idx}>
              <td>{p.player_name}</td>
              <td>{p.team}</td>
              <td>{p.position}</td>
              <td>{p.score?.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Teams</h2>
      <ul>
        {teams.map((t, idx) => (
          <li key={idx}>
            {t.team_name} (ID: {t.team_id}) - Code: {t.team_code}
          </li>
        ))}
      </ul>

      <h2>Live Scores</h2>
      <table border="1" cellPadding="6" cellSpacing="0">
        <thead>
          <tr>
            <th>Home Team</th>
            <th>Away Team</th>
            <th>Home Score</th>
            <th>Away Score</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {liveScores.map((g, idx) => (
            <tr key={idx}>
              <td>{g.home_team}</td>
              <td>{g.away_team}</td>
              <td>{g.home_score}</td>
              <td>{g.away_score}</td>
              <td>{g.game_status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
