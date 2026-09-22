import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import RiskCard from "../components/RiskCard";
import { getProjectRisk } from "../services/api";
import { riskTrendData } from "../mocks/riskTrendData";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface RiskData {
  project_id: string;
  cost_risk: number;
  schedule_risk: number;
  progress_risk: number;
  anomaly_score: number;
  overall_risk: number;
  risk_level: string;
  evidence: string[];
}

function RiskCenter() {
  const navigate = useNavigate();

  const [riskData, setRiskData] = useState<RiskData | null>(null);
  const [loading, setLoading] = useState(true);
  const [backendError, setBackendError] = useState("");

  const [selectedEvidence, setSelectedEvidence] = useState<number | null>(
    null
  );

  const evidenceDetails = [
    {
      title: "Cost Overrun Risk",
      icon: "!",
      color: "#ff4f70",
      problem: "Project cost is above the planned budget.",
      impact:
        "Continued overspending may increase the final project cost and put pressure on available funds.",
      detection:
        "Aurex identified a cost risk score of 82% from the project risk data.",
      action:
        "Review current expenditure, identify high-cost activities, and apply cost-control measures.",
    },
    {
      title: "Schedule Delay Risk",
      icon: "▣",
      color: "#ff9f43",
      problem: "The project schedule is showing signs of delay.",
      impact:
        "Continued delays may affect important milestones and the overall delivery date.",
      detection:
        "Aurex identified a schedule risk score of 74% from the project risk data.",
      action:
        "Review delayed activities, identify the causes, and prioritize critical milestones.",
    },
    {
      title: "Progress Deviation",
      icon: "↗",
      color: "#8b5cf6",
      problem: "Current project progress is below the expected level.",
      impact:
        "Lower progress can increase schedule pressure and affect successful project delivery.",
      detection:
        "Aurex identified a progress risk score of 91% from the project risk data.",
      action:
        "Review blocked activities and focus resources on critical tasks.",
    },
    {
      title: "Anomaly Detected",
      icon: "⚠",
      color: "#22b7ff",
      problem: "Unusual activity has been detected in recent project data.",
      impact:
        "Unexpected patterns may indicate an emerging project issue that requires investigation.",
      detection:
        "Aurex identified an anomaly score of 63% in the project risk data.",
      action:
        "Investigate the unusual activity and compare recent data with expected project patterns.",
    },
  ];

  useEffect(() => {
    const activeProject = JSON.parse(
  localStorage.getItem("aurex_active_project") || '{"project_id":"AUREX-001"}'
);

getProjectRisk(activeProject.project_id)
      .then((data) => {
        setRiskData(data);
      })
      .catch(() => {
        setBackendError("Unable to connect to Aurex backend.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="risk-page">
        <div className="loading-box">
          <div className="loading-spinner" />
          <h2>Loading Risk Intelligence...</h2>
          <p>Aurex is analyzing project signals.</p>
        </div>
      </div>
    );
  }

  if (!riskData) {
    return (
      <div className="risk-page">
        <div className="loading-box">
          <div style={{ fontSize: "42px" }}>⚠️</div>

          <h2>Unable to Load Risk Data</h2>

          <p>{backendError}</p>

          <button
            className="primary-button"
            onClick={() => window.location.reload()}
          >
            Try Again →
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="risk-page">
      <div className="background-glow glow-blue" />
      <div className="background-glow glow-purple" />

      {/* Header */}
      <header className="risk-header">
        <div className="brand">
          <div className="brand-logo">A</div>
          <span>Aurex</span>
        </div>

        <div className="header-nav">
          <button onClick={() => navigate("/projects")}>⌂ Home</button>

          <button className="active-nav">Risk Center</button>
        </div>
      </header>

      {/* Main */}
      <main className="risk-main">
        {/* Hero */}
        <section className="risk-hero">
          <div className="hero-icon">🛡</div>

          <h1>
            Aurex <span>Risk Center</span>
          </h1>

          <div className="risk-level-badge">
            <span className="risk-dot">!</span>

            Risk Level: {riskData.risk_level}
          </div>

          <p className="project-id">
            Project ID: {riskData.project_id}
          </p>
        </section>

        {/* Risk Cards */}
        <section className="risk-grid">
          <RiskCard
            title="Cost Risk"
            value={riskData.cost_risk}
            icon="▤"
            accent="#ff4f70"
          />

          <RiskCard
            title="Schedule Risk"
            value={riskData.schedule_risk}
            icon="▣"
            accent="#ff9f43"
          />

          <RiskCard
            title="Progress Risk"
            value={riskData.progress_risk}
            icon="⌁"
            accent="#8b5cf6"
          />

          <RiskCard
            title="Anomaly Score"
            value={riskData.anomaly_score}
            icon="⚠"
            accent="#22b7ff"
          />

          <RiskCard
            title="Overall Risk"
            value={riskData.overall_risk}
            icon="♢"
            accent="#d946ef"
          />
        </section>

        {/* Chart + Evidence */}
        <section className="dashboard-grid">
          {/* Risk Trend */}
          <div className="glass-panel chart-panel">
            <div className="panel-header">
              <div>
                <h2>↗ Risk Trend</h2>

                <p>Project risk trend over time</p>
              </div>

              <div className="period-badge">◷ Last 7 Days</div>
            </div>

            <div className="chart-wrapper">
              <ResponsiveContainer width="100%" height={320}>
                <LineChart data={riskTrendData}>
                  <CartesianGrid
                    stroke="rgba(255,255,255,0.08)"
                    strokeDasharray="3 3"
                  />

                  <XAxis
                    dataKey="day"
                    stroke="#94a3b8"
                    tick={{
                      fill: "#94a3b8",
                      fontSize: 12,
                    }}
                    axisLine={false}
                    tickLine={false}
                  />

                  <YAxis
                    stroke="#94a3b8"
                    tick={{
                      fill: "#94a3b8",
                      fontSize: 12,
                    }}
                    axisLine={false}
                    tickLine={false}
                    domain={[0, 100]}
                  />

                  <Tooltip
                    contentStyle={{
                      background: "rgba(10,18,50,0.95)",
                      border: "1px solid rgba(139,92,246,0.45)",
                      borderRadius: "12px",
                      color: "#fff",
                      boxShadow: "0 10px 30px rgba(0,0,0,0.35)",
                    }}
                  />

                  <Line
                    type="monotone"
                    dataKey="risk"
                    stroke="#8b5cf6"
                    strokeWidth={4}
                    dot={{
                      r: 5,
                      fill: "#8b5cf6",
                      stroke: "#fff",
                      strokeWidth: 2,
                    }}
                    activeDot={{
                      r: 8,
                    }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="chart-legend">
              <span>
                <i className="legend-dot purple" />
                Overall Risk
              </span>
            </div>
          </div>

          {/* Risk Evidence */}
          <div className="glass-panel evidence-panel">
            <div className="panel-header">
              <div>
                <h2>▤ Risk Evidence</h2>

                <p>Key factors contributing to high risk</p>
              </div>
            </div>

            <div className="evidence-list">
              {riskData.evidence.map((item, index) => {
                const itemStyle =
                  evidenceDetails[index] || evidenceDetails[0];

                return (
                  <div
                    className="evidence-item"
                    key={index}
                    onClick={() => setSelectedEvidence(index)}
                    style={{
                      cursor: "pointer",
                    }}
                  >
                    <div
                      className="evidence-icon"
                      style={{
                        background: `${itemStyle.color}22`,
                        border: `1px solid ${itemStyle.color}55`,
                        color: itemStyle.color,
                        boxShadow: `0 0 18px ${itemStyle.color}20`,
                      }}
                    >
                      {itemStyle.icon}
                    </div>

                    <div className="evidence-text">
                      <strong>{itemStyle.title}</strong>

                      <span>{item}</span>
                    </div>

                    <div className="evidence-arrow">→</div>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* Evidence Details Modal */}
        {selectedEvidence !== null && (
          <div
            onClick={() => setSelectedEvidence(null)}
            style={{
              position: "fixed",
              inset: 0,
              zIndex: 99999,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: "20px",
              background: "rgba(2, 6, 23, 0.78)",
              backdropFilter: "blur(14px)",
              WebkitBackdropFilter: "blur(14px)",
            }}
          >
            <div
              onClick={(e) => e.stopPropagation()}
              style={{
                width: "min(560px, 100%)",
                maxHeight: "90vh",
                overflowY: "auto",
                padding: "30px",
                borderRadius: "24px",
                background:
                  "linear-gradient(145deg, rgba(24,32,65,0.98), rgba(12,17,43,0.98))",
                border: `1px solid ${
                  evidenceDetails[selectedEvidence].color
                }77`,
                boxShadow: `0 25px 80px rgba(0,0,0,0.6), 0 0 45px ${evidenceDetails[selectedEvidence].color}25`,
              }}
            >
              {/* Modal Header */}
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "16px",
                  marginBottom: "24px",
                }}
              >
                <div
                  style={{
                    width: "52px",
                    height: "52px",
                    borderRadius: "16px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: "24px",
                    color: evidenceDetails[selectedEvidence].color,
                    background: `${
                      evidenceDetails[selectedEvidence].color
                    }18`,
                    border: `1px solid ${
                      evidenceDetails[selectedEvidence].color
                    }55`,
                    boxShadow: `0 0 25px ${
                      evidenceDetails[selectedEvidence].color
                    }20`,
                  }}
                >
                  {evidenceDetails[selectedEvidence].icon}
                </div>

                <div>
                  <div
                    style={{
                      fontSize: "11px",
                      fontWeight: 800,
                      letterSpacing: "1.3px",
                      textTransform: "uppercase",
                      color: evidenceDetails[selectedEvidence].color,
                      marginBottom: "5px",
                    }}
                  >
                    Risk Evidence
                  </div>

                  <h2
                    style={{
                      margin: 0,
                      color: "#ffffff",
                      fontSize: "24px",
                    }}
                  >
                    {evidenceDetails[selectedEvidence].title}
                  </h2>
                </div>
              </div>

              {/* Problem */}
              <div
                style={{
                  marginBottom: "18px",
                  padding: "18px",
                  borderRadius: "16px",
                  background: "rgba(255,255,255,0.045)",
                  border: "1px solid rgba(255,255,255,0.08)",
                }}
              >
                <div
                  style={{
                    fontSize: "11px",
                    fontWeight: 800,
                    letterSpacing: "1.2px",
                    textTransform: "uppercase",
                    color: evidenceDetails[selectedEvidence].color,
                    marginBottom: "7px",
                  }}
                >
                  Problem
                </div>

                <p
                  style={{
                    margin: 0,
                    color: "#dbe4ff",
                    lineHeight: 1.6,
                  }}
                >
                  {evidenceDetails[selectedEvidence].problem}
                </p>
              </div>

              {/* Impact */}
              <div
                style={{
                  marginBottom: "18px",
                  padding: "18px",
                  borderRadius: "16px",
                  background: "rgba(255,255,255,0.045)",
                  border: "1px solid rgba(255,255,255,0.08)",
                }}
              >
                <div
                  style={{
                    fontSize: "11px",
                    fontWeight: 800,
                    letterSpacing: "1.2px",
                    textTransform: "uppercase",
                    color: evidenceDetails[selectedEvidence].color,
                    marginBottom: "7px",
                  }}
                >
                  Potential Impact
                </div>

                <p
                  style={{
                    margin: 0,
                    color: "#dbe4ff",
                    lineHeight: 1.6,
                  }}
                >
                  {evidenceDetails[selectedEvidence].impact}
                </p>
              </div>

              {/* Aurex Detection */}
              <div
                style={{
                  marginBottom: "18px",
                  padding: "18px",
                  borderRadius: "16px",
                  background: "rgba(255,255,255,0.045)",
                  border: "1px solid rgba(255,255,255,0.08)",
                }}
              >
                <div
                  style={{
                    fontSize: "11px",
                    fontWeight: 800,
                    letterSpacing: "1.2px",
                    textTransform: "uppercase",
                    color: evidenceDetails[selectedEvidence].color,
                    marginBottom: "7px",
                  }}
                >
                  Aurex Detection
                </div>

                <p
                  style={{
                    margin: 0,
                    color: "#dbe4ff",
                    lineHeight: 1.6,
                  }}
                >
                  {evidenceDetails[selectedEvidence].detection}
                </p>
              </div>

              {/* Recommended Action */}
              <div
                style={{
                  marginBottom: "24px",
                  padding: "18px",
                  borderRadius: "16px",
                  background: `${evidenceDetails[selectedEvidence].color}10`,
                  border: `1px solid ${evidenceDetails[selectedEvidence].color}30`,
                }}
              >
                <div
                  style={{
                    fontSize: "11px",
                    fontWeight: 800,
                    letterSpacing: "1.2px",
                    textTransform: "uppercase",
                    color: evidenceDetails[selectedEvidence].color,
                    marginBottom: "7px",
                  }}
                >
                  Recommended Action
                </div>

                <p
                  style={{
                    margin: 0,
                    color: "#dbe4ff",
                    lineHeight: 1.6,
                  }}
                >
                  {evidenceDetails[selectedEvidence].action}
                </p>
              </div>

              {/* Close */}
              <button
                onClick={() => setSelectedEvidence(null)}
                style={{
                  width: "100%",
                  padding: "13px 18px",
                  borderRadius: "12px",
                  border: `1px solid ${evidenceDetails[selectedEvidence].color}55`,
                  background: `${evidenceDetails[selectedEvidence].color}18`,
                  color: "#ffffff",
                  fontWeight: 700,
                  cursor: "pointer",
                  transition: "0.2s ease",
                }}
              >
                Close Details
              </button>
            </div>
          </div>
        )}

        {/* AI Insight */}
        <section className="ai-insight">
          <div className="ai-icon">✦</div>

          <div className="ai-content">
            <h3>AI Insight</h3>

            <p>
              The project is currently at high risk due to cost
              overrun, schedule delay, and progress deviation.
              Immediate attention is recommended to reduce further
              impact on the delivery timeline.
            </p>
          </div>

          <button
            className="report-button"
            onClick={() => navigate("/investigation")}
          >
            View Detailed Report →
          </button>
        </section>
      </main>
    </div>
  );
}

export default RiskCenter;