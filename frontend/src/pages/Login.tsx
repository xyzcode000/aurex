import { useRef } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();
  const buttonRef = useRef<HTMLButtonElement>(null);

  const handleLogin = () => {
    localStorage.setItem("aurex_auth", "true");
    navigate("/welcome");
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLButtonElement>) => {
    const button = buttonRef.current;

    if (!button) return;

    const rect = button.getBoundingClientRect();

    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;

    button.style.transform = `translate(${x * 0.18}px, ${y * 0.18}px)`;
  };

  const handleMouseLeave = () => {
    const button = buttonRef.current;

    if (!button) return;

    button.style.transform = "translate(0, 0)";
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "24px",
        position: "relative",
        overflow: "hidden",
        background:
          "radial-gradient(circle at 20% 20%, rgba(37, 99, 235, 0.22), transparent 30%), radial-gradient(circle at 80% 80%, rgba(124, 58, 237, 0.25), transparent 30%), #050816",
      }}
    >
      {/* Background Glow 1 */}
      <div
        style={{
          position: "absolute",
          width: "420px",
          height: "420px",
          borderRadius: "50%",
          background: "rgba(37, 99, 235, 0.18)",
          filter: "blur(100px)",
          top: "-150px",
          left: "-120px",
          pointerEvents: "none",
        }}
      />

      {/* Background Glow 2 */}
      <div
        style={{
          position: "absolute",
          width: "420px",
          height: "420px",
          borderRadius: "50%",
          background: "rgba(168, 85, 247, 0.18)",
          filter: "blur(100px)",
          bottom: "-150px",
          right: "-120px",
          pointerEvents: "none",
        }}
      />

      {/* Glass Login Card */}
      <div
        style={{
          width: "100%",
          maxWidth: "420px",
          position: "relative",
          zIndex: 2,
          padding: "42px",
          borderRadius: "24px",

          background:
            "linear-gradient(135deg, rgba(255,255,255,0.13), rgba(255,255,255,0.04))",

          backdropFilter: "blur(24px)",
          WebkitBackdropFilter: "blur(24px)",

          border: "1px solid rgba(255,255,255,0.18)",

          boxShadow:
            "0 30px 80px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.12)",
        }}
      >
        {/* Top shine */}
        <div
          style={{
            position: "absolute",
            top: 0,
            left: "15%",
            right: "15%",
            height: "1px",
            background:
              "linear-gradient(90deg, transparent, rgba(255,255,255,0.7), transparent)",
          }}
        />

        {/* Logo */}
        <div
          style={{
            textAlign: "center",
            marginBottom: "34px",
          }}
        >
          <div
            style={{
              width: "64px",
              height: "64px",
              margin: "0 auto 18px",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              borderRadius: "18px",

              background:
                "linear-gradient(135deg, #2563eb, #7c3aed)",

              color: "white",
              fontSize: "28px",
              fontWeight: "800",

              boxShadow:
                "0 0 30px rgba(99,102,241,0.45)",
            }}
          >
            A
          </div>

          <h1
            style={{
              margin: "0 0 8px",
              color: "#ffffff",
              fontSize: "32px",
              fontWeight: "750",
              letterSpacing: "-1px",
            }}
          >
            Welcome to Aurex
          </h1>

          <p
            style={{
              margin: 0,
              color: "rgba(255,255,255,0.62)",
              fontSize: "14px",
            }}
          >
            Project Intelligence & Risk Management
          </p>
        </div>

        {/* Email */}
        <div style={{ marginBottom: "20px" }}>
          <label
            style={{
              display: "block",
              marginBottom: "8px",
              color: "rgba(255,255,255,0.85)",
              fontSize: "14px",
              fontWeight: "600",
            }}
          >
            Email
          </label>

          <input
            type="email"
            placeholder="Enter your email"
            style={{
              width: "100%",
              padding: "14px 15px",
              borderRadius: "11px",

              border: "1px solid rgba(255,255,255,0.14)",

              background: "rgba(255,255,255,0.07)",

              color: "#ffffff",
              fontSize: "15px",
              outline: "none",

              boxShadow:
                "inset 0 1px 10px rgba(0,0,0,0.08)",

              boxSizing: "border-box",
            }}
          />
        </div>

        {/* Password */}
        <div style={{ marginBottom: "26px" }}>
          <label
            style={{
              display: "block",
              marginBottom: "8px",
              color: "rgba(255,255,255,0.85)",
              fontSize: "14px",
              fontWeight: "600",
            }}
          >
            Password
          </label>

          <input
            type="password"
            placeholder="Enter your password"
            style={{
              width: "100%",
              padding: "14px 15px",
              borderRadius: "11px",

              border: "1px solid rgba(255,255,255,0.14)",

              background: "rgba(255,255,255,0.07)",

              color: "#ffffff",
              fontSize: "15px",
              outline: "none",

              boxShadow:
                "inset 0 1px 10px rgba(0,0,0,0.08)",

              boxSizing: "border-box",
            }}
          />
        </div>

        {/* Magnetic Button */}
        <button
          ref={buttonRef}
          onClick={handleLogin}
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
          style={{
            width: "100%",
            padding: "15px",

            border: "1px solid rgba(255,255,255,0.2)",
            borderRadius: "12px",

            background:
              "linear-gradient(135deg, #2563eb, #7c3aed)",

            color: "#ffffff",
            fontSize: "16px",
            fontWeight: "700",

            cursor: "pointer",

            boxShadow:
              "0 10px 30px rgba(37,99,235,0.35), 0 0 20px rgba(124,58,237,0.2)",

            transition: "transform 0.18s ease-out, box-shadow 0.2s ease",

            willChange: "transform",
          }}
        >
          Login to Aurex →
        </button>

               {/* Sign Up Link */}
        <p
          style={{
            textAlign: "center",
            marginTop: "18px",
            marginBottom: 0,
            color: "rgba(255,255,255,0.62)",
            fontSize: "14px",
          }}
        >
          New to Aurex?{" "}
          <button
            type="button"
            onClick={() => navigate("/signup")}
            style={{
              background: "none",
              border: "none",
              padding: 0,
              color: "#8b5cf6",
              fontWeight: "700",
              cursor: "pointer",
              fontSize: "14px",
            }}
          >
            Sign Up
          </button>
        </p> {/* Footer */}
        <p
          style={{
            textAlign: "center",
            marginTop: "26px",
            marginBottom: 0,
            color: "rgba(255,255,255,0.4)",
            fontSize: "12px",
          }}
        >
          Secure project intelligence dashboard
        </p>
      </div>
    </div>
  );
}

export default Login;