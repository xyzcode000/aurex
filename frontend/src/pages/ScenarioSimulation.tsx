import { useState } from "react";

function ScenarioSimulation() {
  const [budgetChange, setBudgetChange] = useState(0);
  const [timelineChange, setTimelineChange] = useState(0);
  const [result, setResult] = useState(false);
const activeProject = JSON.parse(
  localStorage.getItem("aurex_active_project") ||
    '{"project_id":"AUREX-001","project_name":"Metro Construction"}'
);
  // -----------------------------
  // SIMULATION ENGINE
  // -----------------------------

  const calculateRiskScore = () => {
    const score = 24 + budgetChange * 1.15 + timelineChange * 1.25;
    return Math.min(100, Math.round(score));
  };

  const simulatedScore = calculateRiskScore();

  const getRiskLevel = () => {
    if (simulatedScore >= 70) return "HIGH";
    if (simulatedScore >= 45) return "MEDIUM";
    return "LOW";
  };

  const riskLevel = getRiskLevel();

  const getRiskColor = () => {
    if (riskLevel === "HIGH") return "#f87171";
    if (riskLevel === "MEDIUM") return "#fbbf24";
    return "#4ade80";
  };

  // -----------------------------
  // DYNAMIC EVIDENCE
  // -----------------------------

  const getEvidence = () => {
    const evidence: string[] = [];

    if (budgetChange === 0) {
      evidence.push("No simulated budget increase detected.");
    } else if (budgetChange <= 10) {
      evidence.push(
        `Budget deviation is limited to +${budgetChange}%, indicating relatively low cost exposure.`
      );
    } else if (budgetChange <= 20) {
      evidence.push(
        `Budget deviation of +${budgetChange}% indicates increasing cost exposure.`
      );
    } else {
      evidence.push(
        `Budget deviation of +${budgetChange}% indicates significant cost exposure.`
      );
    }

    if (timelineChange === 0) {
      evidence.push("No simulated timeline extension detected.");
    } else if (timelineChange <= 10) {
      evidence.push(
        `Timeline extension of +${timelineChange}% remains within a relatively stable range.`
      );
    } else if (timelineChange <= 20) {
      evidence.push(
        `Timeline extension of +${timelineChange}% may increase delivery pressure.`
      );
    } else {
      evidence.push(
        `Timeline extension of +${timelineChange}% creates significant schedule exposure.`
      );
    }

    if (budgetChange > 20 && timelineChange > 20) {
      evidence.push(
        "Both cost and schedule deviations are high, increasing overall project exposure."
      );
    } else if (budgetChange > 10 && timelineChange > 10) {
      evidence.push(
        "Combined budget and timeline changes indicate moderate project exposure."
      );
    } else {
      evidence.push(
        "The combined scenario remains within a comparatively controlled range."
      );
    }

    return evidence;
  };

  // -----------------------------
  // DYNAMIC IMPACT
  // -----------------------------

  const getImpact = () => {
    if (riskLevel === "HIGH") {
      return "The simulated scenario creates significant project exposure. Cost escalation and schedule extension may affect project delivery and require management attention.";
    }

    if (riskLevel === "MEDIUM") {
      return "The simulated scenario introduces moderate project exposure. Budget and schedule should be monitored closely.";
    }

    return "The simulated scenario has limited impact on the project. Current changes remain within a relatively stable range.";
  };

  // -----------------------------
  // DYNAMIC AI ENGINE
  // -----------------------------

  const getAIInsight = () => {
    if (riskLevel === "HIGH") {
      return {
        title: "High-risk scenario detected",
        insight:
          "The simulated budget and timeline changes create significant project exposure. The combined deviation may increase cost pressure and delivery risk.",
        recommendation:
          "Review budget drivers, reassess the project timeline, and investigate the causes of the simulated deviations before proceeding.",
      };
    }

    if (riskLevel === "MEDIUM") {
      return {
        title: "Moderate-risk scenario detected",
        insight:
          "The simulated changes indicate increasing project exposure. The project may remain manageable, but cost and schedule should be monitored closely.",
        recommendation:
          "Review resource allocation and monitor budget and timeline performance to prevent further risk escalation.",
      };
    }

    return {
      title: "Stable scenario detected",
      insight:
        "The simulated changes remain within a relatively low-impact range. The project is not showing significant additional exposure under this scenario.",
      recommendation:
        "Continue monitoring project performance and maintain the current budget and timeline controls.",
    };
  };

  const aiInsight = getAIInsight();
  const evidence = getEvidence();

  const runSimulation = () => {
    setResult(true);
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        padding: "40px 5%",
        boxSizing: "border-box",
        color: "#f8fafc",
        background:
          "radial-gradient(circle at 10% 10%, rgba(37,99,235,0.22), transparent 30%), radial-gradient(circle at 90% 20%, rgba(124,58,237,0.22), transparent 30%), linear-gradient(135deg, #07163f 0%, #090c2c 65%, #18075a 100%)",
      }}
    >
      {/* HEADER */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "14px",
          marginBottom: "45px",
        }}
      >
        <div
          style={{
            width: "42px",
            height: "42px",
            borderRadius: "12px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "20px",
            fontWeight: "800",
            background: "linear-gradient(135deg, #2563eb, #7c3aed)",
            boxShadow: "0 0 25px rgba(79,70,229,0.45)",
          }}
        >
          A
        </div>

        <div>
          <div
            style={{
              fontSize: "22px",
              fontWeight: "800",
            }}
          >
            AUREX
          </div>

          <div
            style={{
              fontSize: "12px",
              color: "#8f9dbb",
              letterSpacing: "1px",
            }}
          >
            PROJECT INTELLIGENCE PLATFORM
          </div>
        </div>
      </div>

      <div style={{ maxWidth: "1050px", margin: "0 auto" }}>
        {/* TITLE */}
        <div
          style={{
            textAlign: "center",
            marginBottom: "38px",
          }}
        >
          <div
            style={{
              display: "inline-block",
              padding: "8px 15px",
              borderRadius: "20px",
              fontSize: "12px",
              fontWeight: "700",
              color: "#c4b5fd",
              background: "rgba(124,58,237,0.16)",
              border: "1px solid rgba(139,92,246,0.35)",
              marginBottom: "16px",
            }}
          >
            WHAT-IF ANALYSIS
          </div>

          <h1
            style={{
              margin: 0,
              fontSize: "clamp(34px, 5vw, 50px)",
              fontWeight: "800",
              letterSpacing: "-1.5px",
            }}
          >
            Scenario{" "}
            <span
              style={{
                background:
                  "linear-gradient(90deg, #38bdf8, #8b5cf6, #d946ef)",
                WebkitBackgroundClip: "text",
                backgroundClip: "text",
                color: "transparent",
              }}
            >
              Simulation
            </span>
          </h1>

          <p
            style={{
              marginTop: "12px",
              color: "#aeb9d5",
              fontSize: "15px",
            }}
          >
            Simulate changes in project budget and timeline to understand
            potential project risk.
          </p>
        </div>

        {/* PROJECT */}
        <div
          style={{
            padding: "22px",
            borderRadius: "18px",
            marginBottom: "25px",
            background:
              "linear-gradient(145deg, rgba(255,255,255,0.09), rgba(255,255,255,0.035))",
            border: "1px solid rgba(110,140,255,0.20)",
            boxShadow: "0 18px 45px rgba(0,0,0,0.22)",
            backdropFilter: "blur(18px)",
          }}
        >
          <div
            style={{
              color: "#8f9dbb",
              fontSize: "12px",
              marginBottom: "6px",
            }}
          >
            SIMULATING PROJECT
          </div>

          <div
            style={{
              fontSize: "22px",
              fontWeight: "750",
            }}
          >
            {activeProject.project_name}
          </div>

          <div
            style={{
              color: "#8f9dbb",
              fontSize: "13px",
              marginTop: "5px",
            }}
          >
            Project ID: {activeProject.project_id}
          </div>
        </div>

        {/* MAIN GRID */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1.25fr 0.75fr",
            gap: "20px",
          }}
        >
          {/* INPUTS */}
          <div
            style={{
              padding: "28px",
              borderRadius: "20px",
              background:
                "linear-gradient(145deg, rgba(255,255,255,0.09), rgba(255,255,255,0.035))",
              border: "1px solid rgba(110,140,255,0.20)",
              boxShadow: "0 18px 45px rgba(0,0,0,0.25)",
              backdropFilter: "blur(18px)",
            }}
          >
            <div
              style={{
                fontSize: "18px",
                fontWeight: "750",
                marginBottom: "25px",
              }}
            >
              Scenario Inputs
            </div>

            {/* BUDGET */}
            <div style={{ marginBottom: "30px" }}>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginBottom: "10px",
                }}
              >
                <span style={{ color: "#b8c4df" }}>Budget Change</span>

                <strong style={{ color: "#60a5fa" }}>
                  +{budgetChange}%
                </strong>
              </div>

              <input
                type="range"
                min="0"
                max="50"
                value={budgetChange}
                onChange={(e) => {
                  setBudgetChange(Number(e.target.value));
                  setResult(false);
                }}
                style={{
                  width: "100%",
                  accentColor: "#7c3aed",
                  cursor: "pointer",
                }}
              />

              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginTop: "7px",
                  fontSize: "11px",
                  color: "#647394",
                }}
              >
                <span>0%</span>
                <span>25%</span>
                <span>50%</span>
              </div>
            </div>

            {/* TIMELINE */}
            <div>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginBottom: "10px",
                }}
              >
                <span style={{ color: "#b8c4df" }}>Timeline Change</span>

                <strong style={{ color: "#a78bfa" }}>
                  +{timelineChange}%
                </strong>
              </div>

              <input
                type="range"
                min="0"
                max="50"
                value={timelineChange}
                onChange={(e) => {
                  setTimelineChange(Number(e.target.value));
                  setResult(false);
                }}
                style={{
                  width: "100%",
                  accentColor: "#7c3aed",
                  cursor: "pointer",
                }}
              />

              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginTop: "7px",
                  fontSize: "11px",
                  color: "#647394",
                }}
              >
                <span>0%</span>
                <span>25%</span>
                <span>50%</span>
              </div>
            </div>

            <button
              onClick={runSimulation}
              style={{
                width: "100%",
                marginTop: "30px",
                padding: "14px",
                border: "none",
                borderRadius: "11px",
                color: "#ffffff",
                fontWeight: "750",
                fontSize: "14px",
                cursor: "pointer",
                background:
                  "linear-gradient(90deg, #2563eb, #7c3aed)",
                boxShadow: "0 10px 25px rgba(79,70,229,0.30)",
              }}
            >
              Run Simulation →
            </button>
          </div>

          {/* RISK PREVIEW */}
          <div
            style={{
              padding: "28px",
              borderRadius: "20px",
              background:
                "linear-gradient(145deg, rgba(255,255,255,0.09), rgba(255,255,255,0.035))",
              border: "1px solid rgba(110,140,255,0.20)",
              boxShadow: "0 18px 45px rgba(0,0,0,0.25)",
              backdropFilter: "blur(18px)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              textAlign: "center",
            }}
          >
            <div
              style={{
                color: "#8f9dbb",
                fontSize: "11px",
                fontWeight: "700",
                letterSpacing: "1px",
              }}
            >
              CURRENT SCENARIO
            </div>

            <div
              style={{
                marginTop: "20px",
                width: "120px",
                height: "120px",
                borderRadius: "50%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                background: `radial-gradient(circle, ${getRiskColor()}22, transparent 65%)`,
                border: `2px solid ${getRiskColor()}66`,
                boxShadow: `0 0 35px ${getRiskColor()}22`,
              }}
            >
              <span
                style={{
                  fontSize: "26px",
                  fontWeight: "850",
                  color: getRiskColor(),
                }}
              >
                {riskLevel}
              </span>
            </div>

            <div
              style={{
                marginTop: "15px",
                fontSize: "24px",
                fontWeight: "800",
              }}
            >
              {simulatedScore}%
            </div>

            <div
              style={{
                marginTop: "4px",
                color: "#8f9dbb",
                fontSize: "12px",
              }}
            >
              Simulated Risk Score
            </div>

            <div
              style={{
                marginTop: "18px",
                display: "flex",
                gap: "10px",
                flexWrap: "wrap",
                justifyContent: "center",
                fontSize: "12px",
              }}
            >
              <span
                style={{
                  padding: "7px 10px",
                  borderRadius: "8px",
                  background: "rgba(59,130,246,0.10)",
                  color: "#93c5fd",
                }}
              >
                Budget +{budgetChange}%
              </span>

              <span
                style={{
                  padding: "7px 10px",
                  borderRadius: "8px",
                  background: "rgba(139,92,246,0.10)",
                  color: "#c4b5fd",
                }}
              >
                Timeline +{timelineChange}%
              </span>
            </div>
          </div>
        </div>

        {/* SIMULATION RESULT */}
        {result && (
          <>
            <div
              style={{
                marginTop: "20px",
                padding: "26px",
                borderRadius: "18px",
                background:
                  "linear-gradient(145deg, rgba(255,255,255,0.09), rgba(255,255,255,0.035))",
                border: `1px solid ${getRiskColor()}55`,
                boxShadow: "0 18px 45px rgba(0,0,0,0.20)",
                backdropFilter: "blur(18px)",
              }}
            >
              <div
                style={{
                  color: getRiskColor(),
                  fontSize: "12px",
                  fontWeight: "800",
                  letterSpacing: "0.8px",
                }}
              >
                SIMULATED RESULT
              </div>

              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  gap: "20px",
                  flexWrap: "wrap",
                  marginTop: "10px",
                }}
              >
                <div>
                  <div
                    style={{
                      fontSize: "25px",
                      fontWeight: "800",
                    }}
                  >
                    {riskLevel} RISK
                  </div>

                  <div
                    style={{
                      color: "#8f9dbb",
                      fontSize: "13px",
                      marginTop: "5px",
                    }}
                  >
                    Simulated Risk Score: {simulatedScore}%
                  </div>
                </div>

                <div
                  style={{
                    padding: "10px 15px",
                    borderRadius: "10px",
                    background: `${getRiskColor()}18`,
                    color: getRiskColor(),
                    fontSize: "12px",
                    fontWeight: "700",
                  }}
                >
                  SIMULATED • NOT ACTUAL
                </div>
              </div>

              {/* EVIDENCE */}
              <div
                style={{
                  marginTop: "25px",
                  paddingTop: "20px",
                  borderTop: "1px solid rgba(255,255,255,0.08)",
                }}
              >
                <div
                  style={{
                    fontSize: "15px",
                    fontWeight: "750",
                    marginBottom: "14px",
                  }}
                >
                  🔎 Why is the risk {riskLevel}?
                </div>

                {evidence.map((item, index) => (
                  <div
                    key={index}
                    style={{
                      display: "flex",
                      gap: "10px",
                      marginBottom: "10px",
                      color: "#b8c4df",
                      fontSize: "13px",
                      lineHeight: "1.6",
                    }}
                  >
                    <span style={{ color: getRiskColor() }}>●</span>
                    <span>{item}</span>
                  </div>
                ))}
              </div>

              {/* IMPACT */}
              <div
                style={{
                  marginTop: "20px",
                  padding: "16px",
                  borderRadius: "12px",
                  background: "rgba(255,255,255,0.035)",
                }}
              >
                <div
                  style={{
                    color: "#93c5fd",
                    fontSize: "11px",
                    fontWeight: "800",
                    letterSpacing: "0.7px",
                    marginBottom: "7px",
                  }}
                >
                  SIMULATED IMPACT
                </div>

                <div
                  style={{
                    color: "#b8c4df",
                    fontSize: "13px",
                    lineHeight: "1.6",
                  }}
                >
                  {getImpact()}
                </div>
              </div>
            </div>

            {/* AI WHAT-IF ENGINE */}
            <div
              style={{
                marginTop: "20px",
                padding: "25px",
                borderRadius: "18px",
                background:
                  "linear-gradient(145deg, rgba(59,130,246,0.10), rgba(124,58,237,0.08))",
                border: `1px solid ${getRiskColor()}35`,
                boxShadow: "0 18px 45px rgba(0,0,0,0.18)",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                }}
              >
                <div
                  style={{
                    width: "34px",
                    height: "34px",
                    borderRadius: "10px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    background: "rgba(96,165,250,0.12)",
                    fontSize: "17px",
                  }}
                >
                  ✦
                </div>

                <div>
                  <div
                    style={{
                      color: "#60a5fa",
                      fontSize: "11px",
                      fontWeight: "800",
                      letterSpacing: "0.8px",
                    }}
                  >
                    AUREX WHAT-IF ENGINE
                  </div>

                  <div
                    style={{
                      fontSize: "17px",
                      fontWeight: "750",
                      marginTop: "3px",
                    }}
                  >
                    {aiInsight.title}
                  </div>
                </div>
              </div>

              <div
                style={{
                  marginTop: "18px",
                  color: "#b8c4df",
                  fontSize: "14px",
                  lineHeight: "1.7",
                }}
              >
                {aiInsight.insight}
              </div>

              {/* RECOMMENDATION */}
              <div
                style={{
                  marginTop: "18px",
                  padding: "17px",
                  borderRadius: "12px",
                  background: "rgba(255,255,255,0.04)",
                  border: "1px solid rgba(255,255,255,0.07)",
                }}
              >
                <div
                  style={{
                    color: "#a78bfa",
                    fontSize: "11px",
                    fontWeight: "800",
                    letterSpacing: "0.7px",
                    marginBottom: "7px",
                  }}
                >
                  AUREX RECOMMENDATION
                </div>

                <div
                  style={{
                    color: "#d5ddf0",
                    fontSize: "13px",
                    lineHeight: "1.6",
                  }}
                >
                  {aiInsight.recommendation}
                </div>
              </div>
            </div>
          </>
        )}

        {/* ENGINE STATUS */}
        {!result && (
          <div
            style={{
              marginTop: "20px",
              padding: "18px",
              borderRadius: "15px",
              background: "rgba(59,130,246,0.06)",
              border: "1px solid rgba(59,130,246,0.15)",
              textAlign: "center",
            }}
          >
            <div
              style={{
                color: "#60a5fa",
                fontSize: "11px",
                fontWeight: "800",
                letterSpacing: "0.8px",
              }}
            >
              AUREX WHAT-IF ENGINE
            </div>

            <div
              style={{
                marginTop: "7px",
                color: "#9eabc8",
                fontSize: "13px",
              }}
            >
              Configure the scenario and run the simulation to generate
              evidence, impact analysis, AI insight, and recommendation.
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ScenarioSimulation;