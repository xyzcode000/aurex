import { useNavigate } from "react-router-dom";

function EarlyWarning() {
  const navigate = useNavigate();
  const activeProject = JSON.parse(
  localStorage.getItem("aurex_active_project") ||
    '{"project_id":"AUREX-001"}'
);

  const warnings = [
    {
      title: "Budget Overrun Warning",
      severity: "HIGH",
      project: "Metro Construction",
      projectId: "AUREX-001",
      message: "Project spending is above the planned budget.",
      evidence: "Current spending is exceeding the planned budget baseline.",
    },
    {
      title: "Schedule Delay Warning",
      severity: "MEDIUM",
      project: "Smart City Project",
      projectId: "AUREX-002",
      message: "Recent activities indicate a possible project delay.",
      evidence: "Recent project activities indicate schedule slippage.",
    },
    {
      title: "Progress Warning",
      severity: "HIGH",
      project: "Highway Development",
      projectId: "AUREX-003",
      message: "Project progress is below the expected level.",
      evidence: "Reported progress is below the expected project trajectory.",
    },
  ];
  const selectedWarning = warnings.find(
  (warning) => warning.projectId === activeProject.project_id
);

  const getSeverityStyle = (severity: string) => {
    if (severity === "HIGH") {
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
              color: "#ffffff",
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

      {/* Heading */}
      <div style={{ maxWidth: "1050px", margin: "0 auto" }}>
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
            EARLY WARNING CENTER
          </div>

          <h1
            style={{
              margin: 0,
              fontSize: "clamp(34px, 5vw, 50px)",
              fontWeight: "800",
              letterSpacing: "-1.5px",
            }}
          >
            Detect Problems{" "}
            <span
              style={{
                background: "linear-gradient(90deg, #38bdf8, #8b5cf6, #d946ef)",
                WebkitBackgroundClip: "text",
                backgroundClip: "text",
                color: "transparent",
              }}
            >
              Early
            </span>
          </h1>

          <p
            style={{
              marginTop: "12px",
              color: "#aeb9d5",
              fontSize: "15px",
            }}
          >
            Monitor important project signals before they become critical
            problems.
          </p>
        </div>

        {/* Summary */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: "16px",
            marginBottom: "25px",
          }}
        >
          <div
            style={{
              padding: "20px",
              borderRadius: "16px",
              background: "rgba(255,255,255,0.06)",
              border: "1px solid rgba(255,255,255,0.10)",
            }}
          >
            <div style={{ color: "#8f9dbb", fontSize: "13px" }}>
              Active Warnings
            </div>
            <div
              style={{
                fontSize: "30px",
                fontWeight: "800",
                marginTop: "6px",
              }}
            >
              3
            </div>
          </div>

          <div
            style={{
              padding: "20px",
              borderRadius: "16px",
              background: "rgba(239,68,68,0.07)",
              border: "1px solid rgba(239,68,68,0.18)",
            }}
          >
            <div style={{ color: "#fca5a5", fontSize: "13px" }}>
              High Severity
            </div>
            <div
              style={{
                fontSize: "30px",
                fontWeight: "800",
                marginTop: "6px",
              }}
            >
              2
            </div>
          </div>

          <div
            style={{
              padding: "20px",
              borderRadius: "16px",
              background: "rgba(245,158,11,0.07)",
              border: "1px solid rgba(245,158,11,0.18)",
            }}
          >
            <div style={{ color: "#fcd34d", fontSize: "13px" }}>
              Needs Attention
            </div>
            <div
              style={{
                fontSize: "30px",
                fontWeight: "800",
                marginTop: "6px",
              }}
            >
              3
            </div>
          </div>
        </div>

        {/* Warning Cards */}
        <div
          style={{
            display: "grid",
            gap: "18px",
          }}
        >
          {(selectedWarning ? [selectedWarning] : []).map((warning, index) => {
            const severityStyle = getSeverityStyle(warning.severity);

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
                {/* Top Row */}
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
                        color: "#ffffff",
                      }}
                    >
                      {warning.title}
                    </div>

                    <div
                      style={{
                        marginTop: "6px",
                        color: "#94a3c2",
                        fontSize: "13px",
                      }}
                    >
                      {warning.project} • {warning.projectId}
                    </div>
                  </div>

                  <div
                    style={{
                      ...severityStyle,
                      padding: "7px 13px",
                      borderRadius: "20px",
                      fontSize: "11px",
                      fontWeight: "800",
                      letterSpacing: "0.8px",
                    }}
                  >
                    {warning.severity}
                  </div>
                </div>

                {/* Message */}
                <div
                  style={{
                    marginTop: "20px",
                    padding: "16px",
                    borderRadius: "12px",
                    background: "rgba(5,8,22,0.35)",
                    border: "1px solid rgba(255,255,255,0.06)",
                  }}
                >
                  <div
                    style={{
                      fontSize: "12px",
                      color: "#7180a3",
                      marginBottom: "6px",
                    }}
                  >
                    WARNING
                  </div>

                  <div
                    style={{
                      color: "#dbe4f5",
                      fontSize: "14px",
                    }}
                  >
                    {warning.message}
                  </div>
                </div>

                {/* Evidence */}
                <div style={{ marginTop: "15px" }}>
                  <div
                    style={{
                      fontSize: "12px",
                      color: "#8f9dbb",
                      marginBottom: "5px",
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
                    {warning.evidence}
                  </div>
                </div>

                {/* Action */}
                <button
                  onClick={() => navigate("/investigation")}
                  style={{
                    marginTop: "20px",
                    padding: "11px 18px",
                    border: "none",
                    borderRadius: "10px",
                    color: "#ffffff",
                    fontWeight: "700",
                    cursor: "pointer",
                    background: "linear-gradient(90deg, #2563eb, #7c3aed)",
                    boxShadow: "0 8px 22px rgba(79,70,229,0.28)",
                  }}
                >
                  Investigate Warning →
                </button>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default EarlyWarning;