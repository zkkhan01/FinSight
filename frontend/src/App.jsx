import React, { useEffect, useState } from "react";
import Home from "./pages/Home.jsx";
import Dashboard from "./pages/Dashboard.jsx";

export default function App() {
  const [route, setRoute] = useState("home");
  const [theme, setTheme] = useState("dark");

  // Listen for hash updates (#home, #dashboard)
  useEffect(() => {
    const applyRoute = () => {
      const r = window.location.hash.replace("#", "");
      setRoute(r || "home");
    };
    window.addEventListener("hashchange", applyRoute);
    applyRoute();
    return () => window.removeEventListener("hashchange", applyRoute);
  }, []);

  // Apply theme change to HTML root
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  return (
    <div className="layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <img src="/brand/finsight.png" alt="FinSight" />
          <span>FinSight</span>
        </div>

        <nav className="nav">
          <a href="#home" className={route === "home" ? "active" : ""}>Home</a>
          <a href="#dashboard" className={route === "dashboard" ? "active" : ""}>Dashboard</a>
        </nav>

        <div style={{ marginTop: "auto" }}>
          <div className="seg">
            <button className={theme === "dark" ? "on" : ""} onClick={() => setTheme("dark")}>Dark</button>
            <button className={theme === "light" ? "on" : ""} onClick={() => setTheme("light")}>Light</button>
          </div>
        </div>
      </aside>

      {/* Main page */}
      <main className="main">
        {route === "dashboard" ? <Dashboard /> : <Home />}
      </main>
    </div>
  );
}
