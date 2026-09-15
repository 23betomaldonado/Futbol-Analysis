import React from "react";

const TABS = [
  { id: "home", label: "Home", color: "var(--color-red)" },
  { id: "compare", label: "Compare", color: "var(--color-blue)" },
  { id: "history", label: "History", color: "var(--color-green)" },
  { id: "accuracy", label: "Accuracy", color: "var(--color-orange)" },
];

export default function TopNav({ currentPage, onNavigate }) {
  return (
    <nav style={{ display: "flex", borderBottom: "2px solid #000", padding: "12px 20px", gap: 8 }}>
      {TABS.map((tab) => {
        const isActive = tab.id === currentPage;
        return (
          <button
            key={tab.id}
            onClick={() => onNavigate(tab.id)}
            className="fa-heading"
            style={{
              border: "none",
              padding: "8px 16px",
              fontSize: "1.1rem",
              cursor: "pointer",
              background: isActive ? tab.color : "transparent",
              color: isActive ? "#fff" : tab.color,
            }}
          >
            {tab.label}
          </button>
        );
      })}
    </nav>
  );
}