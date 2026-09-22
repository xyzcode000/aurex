import { useNavigate } from "react-router-dom";

function EmptyState() {
  const navigate = useNavigate();

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "30px",
        boxSizing: "border-box",
        color: "white",
        background:
          "radial-gradient(circle at 20% 20%, rgba(37,99,235,0.22), transparent 30%), radial-gradient(circle at 80% 80%, rgba(124,58,237,0.25), transparent 30%), #050816",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "500px",
          padding: "45px",
          textAlign: "center",
          borderRadius: "22px",
          background:
            "linear-gradient(135deg, rgba(255,255,255,0.11), rgba(255,255,255,0.035))",
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          border: "1px solid rgba(255,255,255,0.14)",
          boxShadow: "0 25px 70px rgba(0,0,0,0.35)",
        }}
      >
        <div
          style={{
            width: "64px",
            height: "64px",
            margin: "0 auto 22px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            borderRadius: "18px",
            background:
              "linear-gradient(135deg, #2563eb, #7c3aed)",
            fontSize: "28px",
            fontWeight: "800",
            boxShadow: "0 0 30px rgba(99,102,241,0.4)",
          }}
        >
          A
        </div>

        <h1
          style={{
            margin: "0 0 12px",
            fontSize: "28px",
            fontWeight: "800",
          }}
        >
          No Projects Found
        </h1>

        <p
          style={{
            margin: "0 auto",
            maxWidth: "380px",
            color: "rgba(255,255,255,0.55)",
            fontSize: "14px",
            lineHeight: 1.7,
          }}
        >
          There are currently no projects available to display.
          Create a new project to begin monitoring with Aurex.
        </p>

        <button
          onClick={() => navigate("/create-project")}
          style={{
            marginTop: "28px",
            padding: "13px 24px",
            border: "1px solid rgba(255,255,255,0.18)",
            borderRadius: "11px",
            background:
              "linear-gradient(135deg, #2563eb, #7c3aed)",
            color: "white",
            fontSize: "14px",
            fontWeight: "700",
            cursor: "pointer",
            boxShadow: "0 10px 30px rgba(37,99,235,0.3)",
          }}
        >
          Create New Project →
        </button>
      </div>
    </div>
  );
}

export default EmptyState;