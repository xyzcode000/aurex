import { useState } from "react";

function Investigation() {
  const [selectedFinding, setSelectedFinding] = useState<string | null>(null);
const activeProject = JSON.parse(
  localStorage.getItem("aurex_active_project") ||
    '{"project_id":"AUREX-001","project_name":"Metro Construction","risk_level":"HIGH"}'
);
  const findings = [
    {
      title: "Budget Investigation",
      status: "Critical",
      factor: "Cost Risk",
      details: "Project spending is higher than the planned budget.",
      evidence:
        "Current project spending is above the planned budget baseline.",
      impact: "Higher spending may increase the overall project cost risk.",
    },
    {
      title: "Schedule Investigation",
      status: "Warning",
      factor: "Schedule Risk",
      details: "Some project activities are delayed.",
      evidence:
        "Recent project activities indicate schedule slippage.",
      impact: "Continued delays may affect the expected project timeline.",
    },
    {
      title: "Progress Investigation",
      status: "Critical",
      factor: "Progress Risk",
      details:
        "Actual project progress is below the expected progress.",
      evidence:
        "Reported project progress is below the expected project trajectory.",
      impact:
        "Lower progress can increase the likelihood of schedule and delivery problems.",
    },
  ];

  const getStatusStyle = (status: string) => {
    if (status === "Critical") {
      return {
        color: "#fca5a5",
        background: "rgba(239,68,68,0.14)",
        border: "1px solid rgba(239,68,68,0.35)",
      };
    }

    return {
      color: "#fcd34d",
      background: "rgba(245,158,11,0.14)",
      border: "1px solid rgba(245,158,11,0.35)",
    };
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
      {/* Header */}
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
        {/* Heading */}
        <div style={{ textAlign: "center", marginBottom: "38px" }}>
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
            AI INVESTIGATION CENTER
          </div>

          <h1
            style={{
              margin: 0,
              fontSize: "clamp(34px, 5vw, 50px)",
              fontWeight: "800",
              letterSpacing: "-1.5px",
            }}
          >
            Why Is This Project{" "}
            <span
              style={{
                background:
                  "linear-gradient(90deg, #38bdf8, #8b5cf6, #d946ef)",
                WebkitBackgroundClip: "text",
                backgroundClip: "text",
                color: "transparent",
              }}
            >
              At Risk?
            </span>
          </h1>

          <p
            style={{
              marginTop: "12px",
              color: "#aeb9d5",
              fontSize: "15px",
            }}
          >
            Investigate contributing factors, evidence, findings and
            potential impact behind important project risks.
          </p>
        </div>

        {/* Project Summary */}
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
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              flexWrap: "wrap",
              gap: "15px",
            }}
          >
            <div>
              <div
                style={{
                  color: "#8f9dbb",
                  fontSize: "12px",
                  marginBottom: "5px",
                }}
              >
                INVESTIGATING PROJECT
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

            <div
              style={{
                padding: "9px 16px",
                borderRadius: "20px",
                color: "#fca5a5",
                background: "rgba(239,68,68,0.14)",
                border: "1px solid rgba(239,68,68,0.35)",
                fontSize: "12px",
                fontWeight: "800",
              }}
            >
              OVERALL RISK: HIGH
            </div>
          </div>
        </div>

        {/* Investigation Flow */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: "15px",
            marginBottom: "30px",
          }}
        >
          {[
            ["01", "Risk", "HIGH"],
            ["02", "Factors", "3 detected"],
            ["03", "Evidence", "3 signals"],
          ].map(([number, label, value]) => (
            <div
              key={number}
              style={{
                padding: "18px",
                borderRadius: "15px",
                background: "rgba(255,255,255,0.05)",
                border: "1px solid rgba(255,255,255,0.09)",
              }}
            >
              <div
                style={{
                  color: "#8b5cf6",
                  fontSize: "12px",
                  fontWeight: "800",
                }}
              >
                {number}
              </div>

              <div
                style={{
                  marginTop: "6px",
                  color: "#94a3c2",
                  fontSize: "12px",
                }}
              >
                {label}
              </div>

              <div
                style={{
                  marginTop: "4px",
                  fontSize: "18px",
                  fontWeight: "700",
                }}
              >
                {value}
              </div>
            </div>
          ))}
        </div>

        {/* Findings */}
        <div
          style={{
            display: "grid",
            gap: "18px",
          }}
        >
          {findings.map((finding, index) => {
            const statusStyle = getStatusStyle(finding.status);
            const isOpen = selectedFinding === finding.title;

            return (
              <div
                key={index}
                style={{
                  padding: "25px",
                  borderRadius: "20px",
                  background:
                    "linear-gradient(145deg, rgba(255,255,255,0.09), rgba(255,255,255,0.035))",
                  border: "1px solid rgba(110,140,255,0.20)",
                  boxShadow: "0 18px 45px rgba(0,0,0,0.25)",
                  backdropFilter: "blur(18px)",
                }}
              >
                {/* Finding Header */}
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    gap: "15px",
                    flexWrap: "wrap",
                  }}
                >
                  <div>
                    <div
                      style={{
                        fontSize: "21px",
                        fontWeight: "750",
                      }}
                    >
                      {finding.title}
                    </div>

                    <div
                      style={{
                        marginTop: "6px",
                        color: "#8f9dbb",
                        fontSize: "13px",
                      }}
                    >
                      Contributing Factor: {finding.factor}
                    </div>
                  </div>

                  <div
                    style={{
                      ...statusStyle,
                      padding: "7px 13px",
                      borderRadius: "20px",
                      fontSize: "11px",
                      fontWeight: "800",
                    }}
                  >
                    {finding.status}
                  </div>
                </div>

                {/* Details */}
                <div
                  style={{
                    marginTop: "20px",
                    color: "#dbe4f5",
                    fontSize: "14px",
                    lineHeight: "1.6",
                  }}
                >
                  {finding.details}
                </div>

                {/* Evidence */}
                <div
                  style={{
                    marginTop: "18px",
                    padding: "16px",
                    borderRadius: "12px",
                    background: "rgba(5,8,22,0.35)",
                    border: "1px solid rgba(255,255,255,0.06)",
                  }}
                >
                  <div
                    style={{
                      color: "#7180a3",
                      fontSize: "11px",
                      fontWeight: "700",
                      marginBottom: "7px",
                    }}
                  >
                    EVIDENCE / SIGNAL
                  </div>

                  <div
                    style={{
                      color: "#b9c5df",
                      fontSize: "13px",
                      lineHeight: "1.6",
                    }}
                  >
                    {finding.evidence}
                  </div>
                </div>

                {/* Expandable Impact */}
                {isOpen && (
                  <div
                    style={{
                      marginTop: "15px",
                      padding: "16px",
                      borderRadius: "12px",
                      background: "rgba(124,58,237,0.08)",
                      border: "1px solid rgba(139,92,246,0.18)",
                    }}
                  >
                    <div
                      style={{
                        color: "#a78bfa",
                        fontSize: "11px",
                        fontWeight: "700",
                        marginBottom: "7px",
                      }}
                    >
                      INVESTIGATION FINDING
                    </div>

                    <div
                      style={{
                        color: "#dbe4f5",
                        fontSize: "13px",
                        lineHeight: "1.6",
                      }}
                    >
                      {finding.impact}
                    </div>
                  </div>
                )}

                <button
                  onClick={() =>
                    setSelectedFinding(
                      isOpen ? null : finding.title
                    )
                  }
                  style={{
                    marginTop: "18px",
                    padding: "11px 18px",
                    border: "none",
                    borderRadius: "10px",
                    color: "#ffffff",
                    fontWeight: "700",
                    cursor: "pointer",
                    background:
                      "linear-gradient(90deg, #2563eb, #7c3aed)",
                    boxShadow:
                      "0 8px 22px rgba(79,70,229,0.28)",
                  }}
                >
                  {isOpen ? "Hide Finding ↑" : "View Evidence & Finding →"}
                </button>
              </div>
            );
          })}
        </div>

        {/* Bottom Insight */}
        <div
          style={{
            marginTop: "25px",
            padding: "22px",
            borderRadius: "18px",
            background: "rgba(59,130,246,0.07)",
            border: "1px solid rgba(59,130,246,0.18)",
          }}
        >
          <div
            style={{
              color: "#60a5fa",
              fontSize: "12px",
              fontWeight: "800",
              letterSpacing: "0.5px",
            }}
          >
            AUREX INVESTIGATION INSIGHT
          </div>

          <div
            style={{
              marginTop: "8px",
              color: "#dbe4f5",
              fontSize: "14px",
              lineHeight: "1.6",
            }}
          >
            Multiple contributing factors have been identified. Review the
            evidence and findings before deciding on the next project
            intervention.
          </div>
        </div>
      </div>
    </div>
  );
}

export default Investigation;