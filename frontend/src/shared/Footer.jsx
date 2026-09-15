import React from "react";

export default function Footer() {
  return (
    <footer style={{ borderTop: "1px solid #000", padding: "20px", marginTop: 40 }}>
      <div style={{ fontSize: "0.72rem", color: "var(--color-grey)" }}>
        Fútbol Analysis: 964 World Cup matches, (1930–2022)
      </div>
      <div style={{ fontSize: "0.72rem", color: "var(--color-grey)", marginTop: 4 }}>
        Created by Roberto A.
      </div>
    </footer>
  );
}