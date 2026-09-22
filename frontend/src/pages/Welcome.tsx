import { useNavigate } from "react-router-dom";

function Welcome() {
  const navigate = useNavigate();

  const userName = localStorage.getItem("aurex_user_name") || "User";

  const modules = [
    {
      icon: "🛡️",
      title: "Risk Center",
      description: "Monitor project risks and overall project health.",
      path: "/risk-center",
    },
    {
      icon: "➕",
      title: "Create New Project",
      description: "Create and start monitoring a new project.",
      path: "/create-project",
    },
    {
      icon: "📁",
      title: "My Projects",
      description: "View and manage your existing projects.",
      path: "/projects",
    },
    {
      icon: "🔮",
      title: "Prediction",
      description: "Explore project risk predictions and forecasts.",
      path: "/prediction",
    },
    {
      icon: "⚠️",
      title: "Early Warning",
      description: "Identify early signs of potential project problems.",
      path: "/early-warning",
    },
    {
      icon: "🔎",
      title: "Investigation",
      description: "Investigate risks and understand project issues.",
      path: "/investigation",
    },
    {
      icon: "🎯",
      title: "Scenario Simulation",
      description: "Explore possible project scenarios and outcomes.",
      path: "/scenario-simulation",
    },
    {
  icon: "📊",
  title: "Project Report",
  description: "View a complete project intelligence and risk report.",
  path: "/project-report",
},
  ];

  return (
    <div
      style={{
        minHeight: "100vh",
        padding: "40px",
        boxSizing: "border-box",
        color: "white",
        background:
          "radial-gradient(circle at 15% 15%, rgba(37,99,235,0.22), transparent 28%), radial-gradient(circle at 85% 80%, rgba(124,58,237,0.25), transparent 30%), #050816",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Background Glow */}
      <div
        style={{
          position: "absolute",
          width: "400px",
          height: "400px",
          borderRadius: "50%",
          background: "rgba(37,99,235,0.14)",
          filter: "blur(110px)",
          top: "-160px",
          left: "-120px",
          pointerEvents: "none",
        }}
      />

      <div
        style={{
          position: "absolute",
          width: "400px",
          height: "400px",
          borderRadius: "50%",
          background: "rgba(168,85,247,0.14)",
          filter: "blur(110px)",
          bottom: "-160px",
          right: "-120px",
          pointerEvents: "none",
        }}
      />

      {/* Main Content */}
      <div
        style={{
          maxWidth: "1200px",
          margin: "0 auto",
          position: "relative",
          zIndex: 2,
        }}
      >
        {/* Header */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "55px",
          }}
        >
          <div>
            <div
              style={{
                fontSize: "24px",
                fontWeight: "800",
                letterSpacing: "-0.5px",
              }}
            >
              AUREX
            </div>

            <div
              style={{
                marginTop: "4px",
                color: "rgba(255,255,255,0.45)",
                fontSize: "12px",
                letterSpacing: "1px",
              }}
            >
              PROJECT INTELLIGENCE
            </div>
          </div>

          <button
            onClick={() => navigate("/")}
            style={{
              padding: "9px 18px",
              borderRadius: "10px",
              border: "1px solid rgba(255,255,255,0.14)",
              background: "rgba(255,255,255,0.06)",
              color: "rgba(255,255,255,0.75)",
              cursor: "pointer",
              fontSize: "13px",
            }}
          >
            Login Page
          </button>
        </div>

        {/* Welcome Section */}
        <div
          style={{
            textAlign: "center",
            marginBottom: "55px",
          }}
        >
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              justifyContent: "center",
              width: "70px",
              height: "70px",
              borderRadius: "20px",
              marginBottom: "22px",
              background:
                "linear-gradient(135deg, #2563eb, #7c3aed)",
              fontSize: "30px",
              fontWeight: "800",
              boxShadow: "0 0 40px rgba(99,102,241,0.4)",
            }}
          >
            A
          </div>

          <h1
            style={{
              margin: "0 0 12px",
              fontSize: "42px",
              fontWeight: "800",
              letterSpacing: "-1.5px",
            }}
          >
            Welcome to Aurex, {userName} 👋
          </h1>

          <p
            style={{
              margin: "0 auto",
              maxWidth: "650px",
              color: "rgba(255,255,255,0.58)",
              fontSize: "16px",
              lineHeight: 1.7,
            }}
          >
            Your intelligent project management and risk intelligence
            platform. Monitor projects, detect risks early, and make
            smarter project decisions.
          </p>
        </div>

        {/* Aurex Overview */}
        <div
          style={{
            padding: "28px",
            marginBottom: "38px",
            borderRadius: "20px",
            background:
              "linear-gradient(135deg, rgba(255,255,255,0.11), rgba(255,255,255,0.035))",
            backdropFilter: "blur(20px)",
            WebkitBackdropFilter: "blur(20px)",
            border: "1px solid rgba(255,255,255,0.13)",
            boxShadow: "0 20px 60px rgba(0,0,0,0.22)",
          }}
        >
          <h2
            style={{
              margin: "0 0 10px",
              fontSize: "21px",
            }}
          >
            About Aurex
          </h2>

          <p
            style={{
              margin: 0,
              color: "rgba(255,255,255,0.58)",
              lineHeight: 1.7,
              fontSize: "14px",
            }}
          >
            Aurex brings project monitoring, risk intelligence, prediction,
            investigation, and scenario analysis together in one place.
            Use the modules below to explore your project and take action
            before risks become major problems.
          </p>
        </div>

        {/* Module Heading */}
        <div style={{ marginBottom: "20px" }}>
          <h2
            style={{
              margin: 0,
              fontSize: "24px",
            }}
          >
            Explore Aurex
          </h2>

          <p
            style={{
              margin: "7px 0 0",
              color: "rgba(255,255,255,0.45)",
              fontSize: "13px",
            }}
          >
            Select a module to continue
          </p>
        </div>

        {/* Module Cards */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit, minmax(240px, 1fr))",
            gap: "18px",
          }}
        >
          {modules.map((module) => (
            <button
              key={module.path}
              onClick={() => navigate(module.path)}
              style={{
                textAlign: "left",
                padding: "24px",
                minHeight: "170px",
                borderRadius: "18px",
                border: "1px solid rgba(255,255,255,0.12)",
                background:
                  "linear-gradient(135deg, rgba(255,255,255,0.09), rgba(255,255,255,0.035))",
                backdropFilter: "blur(18px)",
                WebkitBackdropFilter: "blur(18px)",
                color: "white",
                cursor: "pointer",
                transition:
                  "transform 0.2s ease, border-color 0.2s ease, background 0.2s ease",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform =
                  "translateY(-5px)";
                e.currentTarget.style.borderColor =
                  "rgba(139,92,246,0.55)";
                e.currentTarget.style.background =
                  "linear-gradient(135deg, rgba(37,99,235,0.16), rgba(124,58,237,0.12))";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform =
                  "translateY(0)";
                e.currentTarget.style.borderColor =
                  "rgba(255,255,255,0.12)";
                e.currentTarget.style.background =
                  "linear-gradient(135deg, rgba(255,255,255,0.09), rgba(255,255,255,0.035))";
              }}
            >
              <div
                style={{
                  fontSize: "27px",
                  marginBottom: "15px",
                }}
              >
                {module.icon}
              </div>

              <div
                style={{
                  fontSize: "17px",
                  fontWeight: "700",
                  marginBottom: "8px",
                }}
              >
                {module.title}
              </div>

              <div
                style={{
                  color: "rgba(255,255,255,0.48)",
                  fontSize: "13px",
                  lineHeight: 1.5,
                }}
              >
                {module.description}
              </div>

              <div
                style={{
                  marginTop: "17px",
                  color: "#a78bfa",
                  fontSize: "12px",
                  fontWeight: "700",
                }}
              >
                Open Module →
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Welcome;