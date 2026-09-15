import React, { useState } from "react";
import { Flag } from "../shared/flags";
import { TOURNAMENTS, TEAM_APPEARANCES } from "../shared/tournaments";
import { Micro, Body } from "../shared/typography";

function ChampionsBox() {
  const [selectedYear, setSelectedYear] = useState(2026);
  const detail = TOURNAMENTS.find((t) => t.year === selectedYear);

  return (
    <div className="fa-card" style={{ marginTop: 20 }}>
      <Micro color="var(--color-red)">Every World Cup</Micro>
      <div className="fa-heading" style={{ fontSize: "1.5rem", marginTop: 4 }}>Champions</div>

      <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginTop: 20 }}>
        {[...TOURNAMENTS].reverse().map((t) => (
          <button
            key={t.year}
            onClick={() => setSelectedYear(t.year)}
            style={{
              border: t.year === selectedYear ? "2px solid var(--color-gold)" : "1px solid #000",
              background: t.year === selectedYear ? "#FDF0D0" : "#fff",
              padding: "15px 10px",
              cursor: "pointer",
              textAlign: "center",
            }}
          >
            <Flag nation={t.champion} w={60} />
            <div style={{ fontSize: "1.2rem", marginTop: 6 }}>{t.year}</div>
          </button>
        ))}
      </div>

      {detail && (
        <div style={{ marginTop: 20, borderTop: "1px solid #000", paddingTop: 16 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <Flag nation={detail.champion} w={60} />
            <div className="fa-heading" style={{ fontSize: "1.2rem" }}>
              {detail.champion} <span style={{ color: "var(--color-grey)" }}>— {detail.year} champions</span>
            </div>
          </div>
          <Body>Host: {detail.host}</Body>
          <Body>Runner-up: {detail.runnerUp}</Body>
          <Body>Top scorer: {detail.scorer} ({detail.scorerGoals} goals)</Body>
        </div>
      )}
    </div>
  );
}

function TeamsBox() {
  return (
    <div className="fa-card" style={{ marginTop: 20 }}>
      <Micro color="var(--color-blue)">Every nation</Micro>
      <div className="fa-heading" style={{ fontSize: "1.5rem", marginTop: 4 }}>Most World Cup appearances</div>
      <Body style={{ fontSize: "0.72rem", color: "var(--color-grey)", marginTop: 16 }}>
        Historical nations are merged into their modern successor (West Germany → Germany,
        Soviet Union → Russia, Yugoslavia → Serbia, Czechoslovakia → Czech Republic).
      </Body>
      <div style={{ marginTop: 20 }}>
        {TEAM_APPEARANCES.map((t, i) => (
          <div key={t.nation} style={{ display: "flex", alignItems: "center", gap: 12,
                                        padding: "10px 0", borderTop: i === 0 ? "none" : "1px solid #000" }}>
            <div className="fa-heading" style={{ fontSize: "1.2rem", color: "#ccc", width: 30, textAlign: "right" }}>
              {i + 1}
            </div>
            <Flag nation={t.nation} w={22} />
            <div style={{ flex: 1, fontWeight: 700 }}>{t.nation}</div>
            <div>{t.apps}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function Home() {
  return (

<div>
    <div style={{
        backgroundImage: "url('/world_cup.JPG')",
        backgroundColor: "var(--color-black)",
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center",
        color: "#fff",
        padding: 40,
        minHeight: 500,
        display: "flex",
        flexDirection: "column",
        justifyContent: "flex-end",
      }}>
        <Micro color="rgba(255, 3, 3, 0.8)">Fútbol Analysis</Micro>
        <div className="fa-heading" style={{ fontSize: "2rem", marginTop: 10 }}>
          A World Cup model that shows its work
        </div>
        <Body color="rgba(17, 0, 255, 0.9)">
          Trained on real match data. 
        </Body>
      </div>

      <ChampionsBox />
      <TeamsBox />
    </div>
  );
}