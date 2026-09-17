/*
  This purpose of this file is titles, fonts, font styles, and font size
  */
import React from "react";

export function Micro({ children, color = "#7A7A7A" }) {
  return (
    <div style={{ fontSize: "0.72rem", fontWeight: 700, letterSpacing: ".13em",
                  textTransform: "uppercase", color }}>
      {children}
    </div>
  );
}

export function Body({ children, color = "#454545" }) {
  return (
    <p style={{ fontSize: "0.95rem", lineHeight: 1.62, color }}>
      {children}
    </p>
  );
}