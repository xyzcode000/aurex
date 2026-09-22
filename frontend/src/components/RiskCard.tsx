import { useState } from "react";
import type { MouseEvent } from "react";

interface RiskCardProps {
  title: string;
  value: number;
  icon: string;
  accent: string;
}

function RiskCard({ title, value, icon, accent }: RiskCardProps) {
  const [showDetails, setShowDetails] = useState(false);

  const handleMouseMove = (e: MouseEvent<HTMLDivElement>) => {
    const card = e.currentTarget;
    const rect = card.getBoundingClientRect();

    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const rotateX = (y / rect.height - 0.5) * -6;
    const rotateY = (x / rect.width - 0.5) * 6;

    card.style.transform = `
      perspective(900px)
      rotateX(${rotateX}deg)
      rotateY(${rotateY}deg)
      translateY(-6px)
      scale(1.02)
    `;
  };

  const handleMouseLeave = (e: MouseEvent<HTMLDivElement>) => {
    e.currentTarget.style.transform =
      "perspective(900px) rotateX(0deg) rotateY(0deg) translateY(0) scale(1)";
  };

  const getRiskDetails = () => {
  if (title === "Cost Risk") {
    return {
      problem:
        "Project expenditure is currently above the planned budget.",
      impact:
        "If the current spending pattern continues, the final project cost may exceed the approved budget and put additional pressure on available funds.",
      detection:
        "Aurex detected a high cost-risk score of 82% from the project risk data.",
      action:
        "Review current expenditure, identify high-cost activities, compare actual spending with the planned budget, and apply cost-control measures.",
    };
  }

  if (title === "Schedule Risk") {
    return {
      problem:
        "The project schedule is showing signs of delay against the expected timeline.",
      impact:
        "Continued delays may affect milestone completion and the overall project delivery date.",
      detection:
        "Aurex detected a schedule-risk score of 74% from the project risk data.",
      action:
        "Review delayed activities, identify the reason for the delay, and prioritize critical milestones.",
    };
  }

  if (title === "Progress Risk") {
    return {
      problem:
        "Current project progress is below the expected level.",
      impact:
        "Lower-than-expected progress can increase schedule pressure and may affect successful project delivery.",
      detection:
        "Aurex detected a high progress-risk score of 91% from the project risk data.",
      action:
        "Review current project progress, identify blocked activities, and focus resources on critical tasks.",
    };
  }

  if (title === "Anomaly Score") {
    return {
      problem:
        "Aurex has detected unusual activity in the recent project data.",
      impact:
        "Unexpected patterns may indicate an emerging project issue that requires further investigation.",
      detection:
        "Aurex detected an anomaly score of 63% in the project risk data.",
      action:
        "Investigate the unusual activity and compare recent project data with expected project patterns.",
    };
  }

  return {
    problem:
      "The combined project risk level is currently high.",
    impact:
      "Multiple risk signals may affect project cost, schedule, progress, and overall delivery performance.",
    detection:
      "Aurex calculated an overall risk score of 84% for this project.",
    action:
      "Review the major contributing risk areas and investigate the highest-priority signals first.",
  };
};

  return (
    <>
      {/* Risk Card */}
      <div
        onClick={() => setShowDetails(true)}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        style={{
          position: "relative",
          padding: "22px",
          minHeight: "175px",
          borderRadius: "18px",
          background:
            "linear-gradient(145deg, rgba(255,255,255,0.09), rgba(255,255,255,0.035))",
          border: `1px solid ${accent}66`,
          boxShadow: `0 15px 40px rgba(0,0,0,0.25), 0 0 25px ${accent}18`,
          backdropFilter: "blur(18px)",
          WebkitBackdropFilter: "blur(18px)",
          overflow: "hidden",
          cursor: "pointer",
          transition:
            "transform 0.18s ease, box-shadow 0.25s ease, border-color 0.25s ease",
          transformStyle: "preserve-3d",
        }}
      >
        {/* Glow */}
        <div
          style={{
            position: "absolute",
            width: "130px",
            height: "130px",
            borderRadius: "50%",
            background: accent,
            opacity: 0.1,
            filter: "blur(35px)",
            top: "-55px",
            right: "-45px",
            pointerEvents: "none",
          }}
        />

        {/* Top row */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            position: "relative",
            zIndex: 2,
          }}
        >
          <div
            style={{
              width: "44px",
              height: "44px",
              borderRadius: "50%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              background: `${accent}25`,
              border: `1px solid ${accent}66`,
              boxShadow: `0 0 20px ${accent}35`,
              fontSize: "20px",
            }}
          >
            {icon}
          </div>

          <div
            style={{
              width: "32px",
              height: "32px",
              borderRadius: "50%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              background: "rgba(255,255,255,0.06)",
              color: "#cbd5e1",
              fontSize: "18px",
              border: "1px solid rgba(255,255,255,0.08)",
            }}
          >
            →
          </div>
        </div>

        {/* Title */}
        <p
          style={{
            margin: "18px 0 5px",
            color: "#cbd5e1",
            fontSize: "15px",
            fontWeight: 600,
            letterSpacing: "0.2px",
          }}
        >
          {title}
        </p>

        {/* Value */}
        <div
          style={{
            fontSize: "34px",
            fontWeight: 750,
            color: "#f8fafc",
            lineHeight: 1.1,
          }}
        >
          {value}%
        </div>

        {/* Progress */}
        <div
          style={{
            marginTop: "18px",
            height: "6px",
            width: "100%",
            borderRadius: "20px",
            background: "rgba(255,255,255,0.09)",
            overflow: "hidden",
          }}
        >
          <div
            style={{
              width: `${value}%`,
              height: "100%",
              borderRadius: "20px",
              background: accent,
              boxShadow: `0 0 12px ${accent}`,
              transition: "width 0.5s ease",
            }}
          />
        </div>

        {/* Click hint */}
        <div
          style={{
            marginTop: "12px",
            color: "#71809f",
            fontSize: "10px",
            textAlign: "right",
          }}
        >
          Click for details
        </div>
      </div>

      {/* Detail Modal */}
      {showDetails && (
        <div
          onClick={() => setShowDetails(false)}
          style={{
            position: "fixed",
            inset: 0,
            zIndex: 99999,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "20px",
            background: "rgba(2, 6, 23, 0.72)",
            backdropFilter: "blur(12px)",
            WebkitBackdropFilter: "blur(12px)",
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              width: "min(480px, 100%)",
              maxHeight: "90vh",
overflowY: "auto",
              padding: "30px",
              borderRadius: "24px",
              background:
                "linear-gradient(145deg, rgba(24,32,65,0.98), rgba(12,17,43,0.98))",
              border: `1px solid ${accent}77`,
              boxShadow: `0 25px 80px rgba(0,0,0,0.55), 0 0 40px ${accent}25`,
            }}
          >
            {/* Modal top */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
              }}
            >
              <div
                style={{
                  width: "54px",
                  height: "54px",
                  borderRadius: "50%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  background: `${accent}25`,
                  border: `1px solid ${accent}66`,
                  boxShadow: `0 0 25px ${accent}35`,
                  fontSize: "24px",
                }}
              >
                {icon}
              </div>

              <button
                onClick={() => setShowDetails(false)}
                style={{
                  width: "34px",
                  height: "34px",
                  borderRadius: "50%",
                  border: "1px solid rgba(255,255,255,0.1)",
                  background: "rgba(255,255,255,0.06)",
                  color: "#cbd5e1",
                  fontSize: "18px",
                }}
              >
                ×
              </button>
            </div>

            <p
              style={{
                marginTop: "22px",
                marginBottom: "5px",
                color: "#94a3b8",
                fontSize: "14px",
              }}
            >
              Risk Analysis
            </p>

            <h2
              style={{
                margin: "0",
                color: "#ffffff",
                fontSize: "28px",
              }}
            >
              {title}
            </h2>

            {/* Score */}
            <div
              style={{
                marginTop: "25px",
                display: "flex",
                alignItems: "baseline",
                gap: "5px",
              }}
            >
              <span
                style={{
                  fontSize: "58px",
                  fontWeight: 800,
                  color: accent,
                  textShadow: `0 0 25px ${accent}55`,
                }}
              >
                {value}
              </span>

              <span
                style={{
                  color: "#94a3b8",
                  fontSize: "20px",
                }}
              >
                %
              </span>
            </div>

            {/* Progress */}
            <div
              style={{
                marginTop: "12px",
                height: "9px",
                borderRadius: "20px",
                background: "rgba(255,255,255,0.08)",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: `${value}%`,
                  height: "100%",
                  borderRadius: "20px",
                  background: accent,
                  boxShadow: `0 0 18px ${accent}`,
                }}
              />
            </div>

            {/* Status */}
            <div
              style={{
                marginTop: "24px",
                padding: "16px",
                borderRadius: "14px",
                background: `${accent}12`,
                border: `1px solid ${accent}30`,
              }}
            >
              <p
                style={{
                  margin: 0,
                  color: "#dbe4f5",
                  fontSize: "14px",
                  lineHeight: 1.6,
                }}
              >
                <div
  style={{
    display: "grid",
    gap: "14px",
    marginTop: "24px",
  }}
>
  {/* Problem */}
  <div
    style={{
      padding: "16px",
      borderRadius: "14px",
      background: "rgba(255,255,255,0.045)",
      border: "1px solid rgba(255,255,255,0.08)",
    }}
  >
    <div
      style={{
        color: accent,
        fontSize: "13px",
        fontWeight: 700,
        marginBottom: "7px",
      }}
    >
      🔴 Problem
    </div>

    <p
      style={{
        margin: 0,
        color: "#dbe4f5",
        fontSize: "13px",
        lineHeight: 1.6,
      }}
    >
      {getRiskDetails().problem}
    </p>
  </div>

  {/* Impact */}
  <div
    style={{
      padding: "16px",
      borderRadius: "14px",
      background: "rgba(255,255,255,0.045)",
      border: "1px solid rgba(255,255,255,0.08)",
    }}
  >
    <div
      style={{
        color: "#f59e0b",
        fontSize: "13px",
        fontWeight: 700,
        marginBottom: "7px",
      }}
    >
      ⚠️ Potential Impact
    </div>

    <p
      style={{
        margin: 0,
        color: "#dbe4f5",
        fontSize: "13px",
        lineHeight: 1.6,
      }}
    >
      {getRiskDetails().impact}
    </p>
  </div>

  {/* Aurex Detection */}
  <div
    style={{
      padding: "16px",
      borderRadius: "14px",
      background: "rgba(139,92,246,0.08)",
      border: "1px solid rgba(139,92,246,0.22)",
    }}
  >
    <div
      style={{
        color: "#a78bfa",
        fontSize: "13px",
        fontWeight: 700,
        marginBottom: "7px",
      }}
    >
      🔍 Aurex Detection
    </div>

    <p
      style={{
        margin: 0,
        color: "#dbe4f5",
        fontSize: "13px",
        lineHeight: 1.6,
      }}
    >
      {getRiskDetails().detection}
    </p>
  </div>

  {/* Recommended Action */}
  <div
    style={{
      padding: "16px",
      borderRadius: "14px",
      background: "rgba(34,197,94,0.07)",
      border: "1px solid rgba(34,197,94,0.2)",
    }}
  >
    <div
      style={{
        color: "#4ade80",
        fontSize: "13px",
        fontWeight: 700,
        marginBottom: "7px",
      }}
    >
      💡 Recommended Action
    </div>

    <p
      style={{
        margin: 0,
        color: "#dbe4f5",
        fontSize: "13px",
        lineHeight: 1.6,
      }}
    >
      {getRiskDetails().action}
    </p>
  </div>
</div>
              </p>
            </div>

            <button
              onClick={() => setShowDetails(false)}
              style={{
                width: "100%",
                marginTop: "22px",
                padding: "13px",
                border: "none",
                borderRadius: "12px",
                color: "white",
                fontWeight: 700,
                background: `linear-gradient(90deg, ${accent}, #7c3aed)`,
                boxShadow: `0 8px 25px ${accent}35`,
              }}
            >
              Close Details
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default RiskCard;