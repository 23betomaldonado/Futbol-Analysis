import React, { useState } from "react";
import TopNav from "./shared/TopNav";
import Footer from "./shared/Footer";
import Home from "./home_tab/Home";
import Compare from "./compare_tab/Compare";

export default function App() {
  const [currentPage, setCurrentPage] = useState("home");

  return (
    <div>
      <TopNav currentPage={currentPage} onNavigate={setCurrentPage} />

      {currentPage === "home" && <Home />}
      {currentPage === "compare" && <Compare />}
      {currentPage !== "home" && (
        <div style={{ padding: 40 }}>
          <p>This page hasn't been built yet — coming soon.</p>
        </div>
      )}

      <Footer />
    </div>
  );
}