import { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import { checkBackendHealth } from "./services/api";

import Login from "./pages/Login";
import SignUp from "./pages/SignUp";
import Welcome from "./pages/Welcome";

import RiskCenter from "./pages/RiskCenter";
import Prediction from "./pages/Prediction";
import ProjectList from "./pages/ProjectList";
import ProjectDetail from "./pages/ProjectDetail";
import ProjectCreate from "./pages/ProjectCreate";
import ScenarioSimulation from "./pages/ScenarioSimulation";
import EarlyWarning from "./pages/EarlyWarning";
import Investigation from "./pages/Investigation";
import ProjectReport from "./pages/ProjectReport";
import LoadingState from "./pages/LoadingState";
import EmptyState from "./pages/EmptyState";
import ErrorState from "./pages/ErrorState";

import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  const [backendStatus, setBackendStatus] = useState("");

  useEffect(() => {
    checkBackendHealth()
      .then((data) => {
        setBackendStatus(data.status);
      })
      .catch(() => {
        setBackendStatus("backend connection failed");
      });
  }, []);

  return (
    <>
      <div
        style={{
          position: "fixed",
          top: "10px",
          right: "10px",
          padding: "8px 12px",
          backgroundColor:
            backendStatus === "healthy" ? "#16a34a" : "#dc2626",
          color: "white",
          borderRadius: "6px",
          zIndex: 9999,
          fontSize: "14px",
        }}
      >
        Backend: {backendStatus || "checking..."}
      </div>

      <BrowserRouter>
        <Routes>
          {/* Login */}
          <Route path="/" element={<Login />} />

          {/* Sign Up */}
          <Route path="/signup" element={<SignUp />} />
          <Route path="/welcome" element={<Welcome />} />

          {/* Risk Center */}
          <Route
            path="/risk-center"
            element={
              <ProtectedRoute>
                <RiskCenter />
              </ProtectedRoute>
            }
          />

          {/* Prediction */}
          <Route
            path="/prediction"
            element={
              <ProtectedRoute>
                <Prediction />
              </ProtectedRoute>
            }
          />

          {/* Projects */}
          <Route
            path="/projects"
            element={
              <ProtectedRoute>
                <ProjectList />
              </ProtectedRoute>
            }
          />

          {/* Project Detail */}
          <Route
            path="/project-detail"
            element={
              <ProtectedRoute>
                <ProjectDetail />
              </ProtectedRoute>
            }
          />

          {/* Create Project */}
          <Route
            path="/create-project"
            element={
              <ProtectedRoute>
                <ProjectCreate />
              </ProtectedRoute>
            }
          />

          {/* Scenario Simulation */}
          <Route
            path="/scenario-simulation"
            element={
              <ProtectedRoute>
                <ScenarioSimulation />
              </ProtectedRoute>
            }
          />

          {/* Early Warning */}
          <Route
            path="/early-warning"
            element={
              <ProtectedRoute>
                <EarlyWarning />
              </ProtectedRoute>
            }
          />

          {/* Investigation */}
          <Route
            path="/investigation"
            element={
              <ProtectedRoute>
                <Investigation />
              </ProtectedRoute>
            }
          />
<Route
  path="/project-report"
  element={
    <ProtectedRoute>
      <ProjectReport />
    </ProtectedRoute>
  }
/>
          {/* Loading */}
          <Route
            path="/loading"
            element={
              <ProtectedRoute>
                <LoadingState />
              </ProtectedRoute>
            }
          />

          {/* Empty */}
          <Route
            path="/empty"
            element={
              <ProtectedRoute>
                <EmptyState />
              </ProtectedRoute>
            }
          />

          {/* Error */}
          <Route
            path="/error"
            element={
              <ProtectedRoute>
                <ErrorState />
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;