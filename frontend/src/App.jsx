import React from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import FlagsPage from "./pages/FlagsPage";
import EvaluatePage from "./pages/EvaluatePage";
import AuditPage from "./pages/AuditPage";

function App() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <div className="brand">Flagship</div>
          <div className="brand-subtitle">Feature delivery control plane</div>
        </div>

        <nav className="nav">
          <NavLink to="/">Flags</NavLink>
          <NavLink to="/evaluate">Evaluate</NavLink>
          <NavLink to="/audit">Audit</NavLink>
        </nav>
      </aside>

      <main className="main">
        <Routes>
          <Route path="/" element={<FlagsPage />} />
          <Route path="/evaluate" element={<EvaluatePage />} />
          <Route path="/audit" element={<AuditPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
