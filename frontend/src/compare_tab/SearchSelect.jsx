import React, { useState } from "react";

export default function SearchSelect({ teams, value, onSelect }) {
  const [query, setQuery] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  const filtered = teams.filter((team) =>
    team.toLowerCase().includes(query.toLowerCase())
  );

  function handlePick(team) {
    onSelect(team);
    setQuery(team);
    setIsOpen(false);
  }

  return (
    <div style={{ position: "relative" }}>
      <input
        type="text"
        value={isOpen ? query : (value || "")}
        onChange={(e) => {
          setQuery(e.target.value);
          setIsOpen(true);
        }}
        onFocus={() => {
          setQuery("");
          setIsOpen(true);
        }}
        placeholder="Search for a team..."
        style={{ width: "100%", padding: "10px 12px", border: "1px solid #000", fontSize: "0.95rem" }}
      />

      {isOpen && (
        <div style={{ position: "absolute", top: "100%", left: 0, right: 0, background: "#fff",
                      border: "1px solid #000", borderTop: "none", maxHeight: 200, overflowY: "auto", zIndex: 10 }}>
          {filtered.map((team) => (
            <div key={team} onClick={() => handlePick(team)} style={{ padding: "8px 12px", cursor: "pointer" }}>
              {team}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}