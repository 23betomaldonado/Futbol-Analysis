import React, { useState, useEffect } from "react";
import SearchSelect from "./SearchSelect";
import { Micro, Body } from "../shared/typography";

function TeamsCompare() {
  const [allTeams, setAllTeams] = useState([]);
  const [teamA, setTeamA] = useState(null);
  const [teamB, setTeamB] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [teamsError, setTeamsError] = useState(false);
  const [predictError, setPredictError] = useState(false);

  useEffect(() => {
    fetch("/api/teams")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to load teams");
        return res.json();
      })
      .then((data) => setAllTeams(data.teams.map((t) => t.name)))
      .catch(() => setTeamsError(true));
  }, []);

  useEffect(() => {
    if (!teamA || !teamB) {
      setResult(null);
      return;
    }
    setLoading(true);
    setPredictError(false);
    fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ home_team: teamA, away_team: teamB }),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Prediction failed");
        return res.json();
      })
      .then((data) => {
        setResult(data);
        setLoading(false);
      })
      .catch(() => {
        setPredictError(true);
        setLoading(false);
      });
  }, [teamA, teamB]);

  const teamsForA = allTeams.filter((t) => t !== teamB);
  const teamsForB = allTeams.filter((t) => t !== teamA);

  const home = result ? Math.round(result.probabilities[`${teamA} Win`] * 100) : 0;
  const draw = result ? Math.round(result.probabilities["Draw"] * 100) : 0;
  const away = result ? Math.round(result.probabilities[`${teamB} Win`] * 100) : 0;

  return (
    <>
      <div className="fa-card">
        <div style={{ display: "flex", gap: 20 }}>
          <div style={{ flex: 1 }}>
            <Micro color="var(--color-blue)">Team A</Micro>
            <SearchSelect teams={teamsForA} value={teamA} onSelect={setTeamA} />
          </div>
          <div style={{ flex: 1 }}>
            <Micro color="var(--color-red)">Team B</Micro>
            <SearchSelect teams={teamsForB} value={teamB} onSelect={setTeamB} />
          </div>
        </div>
      </div>

      {teamsError && (
        <Body style={{ marginTop: 20, color: "var(--color-red)" }}>
          Couldn't load the team list. Is the backend running?
        </Body>
      )}

      {loading && <Body style={{ marginTop: 20 }}>Loading prediction…</Body>}

      {predictError && !loading && (
        <Body style={{ marginTop: 20, color: "var(--color-red)" }}>
          Couldn't get a prediction. Is the backend running?
        </Body>
      )}

      {result && !loading && !predictError && (
        <div className="fa-card" style={{ marginTop: 20 }}>
          <Body>{teamA} vs {teamB}</Body>
          <div style={{ display: "flex", height: 30, marginTop: 10, border: "1px solid #000" }}>
            <div style={{ width: `${home}%`, background: "var(--color-blue)" }} />
            <div style={{ width: `${draw}%`, background: "#ccc" }} />
            <div style={{ width: `${away}%`, background: "var(--color-red)" }} />
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", marginTop: 8, fontSize: "0.72rem" }}>
            <span>{teamA} {home}%</span>
            <span>Draw {draw}%</span>
            <span>{teamB} {away}%</span>
          </div>
        </div>
      )}
    </>
  );
}

const PROFILE_FIELDS = [
  { key: "age", label: "Age" },
  { key: "height_cm", label: "Height (cm)" },
  { key: "weight_kg", label: "Weight (kg)" },
  { key: "jersey_number", label: "Jersey #" },
  { key: "market_value_eur", label: "Market Value" },
];

const PERFORMANCE_STATS = [
  { key: "goals", label: "Goals" },
  { key: "assists", label: "Assists" },
  { key: "key_passes", label: "Key Passes" },
  { key: "pass_accuracy", label: "Pass Accuracy %" },
  { key: "successful_dribbles", label: "Successful Dribbles" },
  { key: "tackles", label: "Tackles" },
  { key: "interceptions", label: "Interceptions" },
  { key: "aerial_duels_won", label: "Aerial Duels Won" },
  { key: "distance_covered_km", label: "Distance Covered (km)" },
  { key: "player_rating", label: "Player Rating" },
];

const DISCIPLINE_STATS = [
  { key: "fouls_committed", label: "Fouls Committed" },
  { key: "yellow_cards", label: "Yellow Cards" },
  { key: "red_cards", label: "Red Cards" },
  { key: "offsides", label: "Offsides" },
];

function StatBar({ playerA, playerB, statKey, color }) {
  const max = Math.max(playerA[statKey], playerB[statKey]) || 1;
  const widthA = (playerA[statKey] / max) * 100;
  const widthB = (playerB[statKey] / max) * 100;
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      <span style={{ fontSize: "0.72rem", width: 30, textAlign: "right" }}>{playerA[statKey]}</span>
      <div style={{ flex: 1, display: "flex", justifyContent: "flex-end", height: 12, background: "#eee" }}>
        <div style={{ width: `${widthA}%`, background: color }} />
      </div>
      <div style={{ flex: 1, display: "flex", height: 12, background: "#eee" }}>
        <div style={{ width: `${widthB}%`, background: color }} />
      </div>
      <span style={{ fontSize: "0.72rem", width: 30 }}>{playerB[statKey]}</span>
    </div>
  );
}

function PlayersCompare() {
  const [allPlayers, setAllPlayers] = useState([]);
  const [playerAName, setPlayerAName] = useState(null);
  const [playerBName, setPlayerBName] = useState(null);
  const [playersError, setPlayersError] = useState(false);

  useEffect(() => {
    fetch("/api/players")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to load players");
        return res.json();
      })
      .then((data) => setAllPlayers(data.players))
      .catch(() => setPlayersError(true));
  }, []);

  const allPlayerNames = allPlayers.map((p) => p.player_name);
  const namesForA = allPlayerNames.filter((n) => n !== playerBName);
  const namesForB = allPlayerNames.filter((n) => n !== playerAName);

  const playerA = allPlayers.find((p) => p.player_name === playerAName);
  const playerB = allPlayers.find((p) => p.player_name === playerBName);

  return (
    <>
      <div className="fa-card">
        <div style={{ display: "flex", gap: 20 }}>
          <div style={{ flex: 1 }}>
            <Micro color="var(--color-blue)">Player A</Micro>
            <SearchSelect teams={namesForA} value={playerAName} onSelect={setPlayerAName} />
          </div>
          <div style={{ flex: 1 }}>
            <Micro color="var(--color-red)">Player B</Micro>
            <SearchSelect teams={namesForB} value={playerBName} onSelect={setPlayerBName} />
          </div>
        </div>
      </div>

      {playersError && (
        <Body style={{ marginTop: 20, color: "var(--color-red)" }}>
          Couldn't load the player list. Is the backend running?
        </Body>
      )}

      {playerA && playerB && (
        <div className="fa-card" style={{ marginTop: 20 }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontWeight: 700, marginBottom: 16 }}>
            <span>{playerA.player_name} ({playerA.position})</span>
            <span>{playerB.player_name} ({playerB.position})</span>
          </div>

          <Micro>Profile</Micro>
          <div style={{ marginTop: 6 }}>
            {PROFILE_FIELDS.map(({ key, label }) => (
              <div key={key} style={{ display: "flex", justifyContent: "space-between", padding: "3px 0" }}>
                <span style={{ fontSize: "0.72rem" }}>
                  {key === "market_value_eur" ? `€${playerA[key].toLocaleString()}` : playerA[key]}
                </span>
                <Micro>{label}</Micro>
                <span style={{ fontSize: "0.72rem" }}>
                  {key === "market_value_eur" ? `€${playerB[key].toLocaleString()}` : playerB[key]}
                </span>
              </div>
            ))}
          </div>

          <Micro color="var(--color-green)" style={{ marginTop: 20, display: "block" }}>Performance</Micro>
          <div style={{ marginTop: 8, display: "flex", flexDirection: "column", gap: 10 }}>
            {PERFORMANCE_STATS.map(({ key, label }) => (
              <div key={key}>
                <Micro style={{ textAlign: "center" }}>{label}</Micro>
                <StatBar playerA={playerA} playerB={playerB} statKey={key} color="var(--color-green)" />
              </div>
            ))}
          </div>

          <Micro color="var(--color-red)" style={{ marginTop: 20, display: "block" }}>Discipline</Micro>
          <Body style={{ fontSize: "0.72rem", marginTop: 2 }}>
            Shown for context, not as a "who's better" comparison — more here isn't a good thing.
          </Body>
          <div style={{ marginTop: 8, display: "flex", flexDirection: "column", gap: 10 }}>
            {DISCIPLINE_STATS.map(({ key, label }) => (
              <div key={key}>
                <Micro style={{ textAlign: "center" }}>{label}</Micro>
                <StatBar playerA={playerA} playerB={playerB} statKey={key} color="var(--color-red)" />
              </div>
            ))}
          </div>

          <Body style={{ marginTop: 16, fontSize: "0.72rem", color: "var(--color-grey)" }}>
            Real aggregated stats, synthetic player identities.
          </Body>
        </div>
      )}
    </>
  );
}

export default function Compare() {
  return (
    <div style={{ padding: 40 }}>
      <Micro color="var(--color-blue)">Compare</Micro>
      <div className="fa-heading" style={{ fontSize: "1.5rem", marginTop: 4, marginBottom: 20 }}>
        Pick two teams
      </div>
      <TeamsCompare />

      <div className="fa-heading" style={{ fontSize: "1.5rem", marginTop: 40, marginBottom: 20 }}>
        Pick two players
      </div>
      <PlayersCompare />
    </div>
  );
}