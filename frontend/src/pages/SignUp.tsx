import { useState } from "react";
import { useNavigate } from "react-router-dom";

function SignUp() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");

  const handleSignUp = (e: React.FormEvent) => {
    e.preventDefault();

    if (!name || !email || !password || !confirmPassword) {
      setError("Please fill in all fields.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    localStorage.setItem("aurex_auth", "true");
localStorage.setItem("aurex_user_name", name);
localStorage.setItem("aurex_user_email", email);

navigate("/welcome");
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

      {/* Glass Sign Up Card */}
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
        {/* Top Shine */}
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

        {/* Header */}
        <div
          style={{
            textAlign: "center",
            marginBottom: "30px",
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
            Create Your Account
          </h1>

          <p
            style={{
              margin: 0,
              color: "rgba(255,255,255,0.62)",
              fontSize: "14px",
            }}
          >
            Join Aurex Project Intelligence
          </p>
        </div>

        <form onSubmit={handleSignUp}>
          {/* Name */}
          <div style={{ marginBottom: "18px" }}>
            <label
              style={{
                display: "block",
                marginBottom: "8px",
                color: "rgba(255,255,255,0.85)",
                fontSize: "14px",
                fontWeight: "600",
              }}
            >
              Full Name
            </label>

            <input
              type="text"
              placeholder="Enter your full name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              style={{
                width: "100%",
                padding: "14px 15px",
                borderRadius: "11px",
                border: "1px solid rgba(255,255,255,0.14)",
                background: "rgba(255,255,255,0.07)",
                color: "#ffffff",
                fontSize: "15px",
                outline: "none",
                boxSizing: "border-box",
              }}
            />
          </div>

          {/* Email */}
          <div style={{ marginBottom: "18px" }}>
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
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{
                width: "100%",
                padding: "14px 15px",
                borderRadius: "11px",
                border: "1px solid rgba(255,255,255,0.14)",
                background: "rgba(255,255,255,0.07)",
                color: "#ffffff",
                fontSize: "15px",
                outline: "none",
                boxSizing: "border-box",
              }}
            />
          </div>

          {/* Password */}
          <div style={{ marginBottom: "18px" }}>
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
              placeholder="Create a password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{
                width: "100%",
                padding: "14px 15px",
                borderRadius: "11px",
                border: "1px solid rgba(255,255,255,0.14)",
                background: "rgba(255,255,255,0.07)",
                color: "#ffffff",
                fontSize: "15px",
                outline: "none",
                boxSizing: "border-box",
              }}
            />
          </div>

          {/* Confirm Password */}
          <div style={{ marginBottom: "18px" }}>
            <label
              style={{
                display: "block",
                marginBottom: "8px",
                color: "rgba(255,255,255,0.85)",
                fontSize: "14px",
                fontWeight: "600",
              }}
            >
              Confirm Password
            </label>

            <input
              type="password"
              placeholder="Confirm your password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              style={{
                width: "100%",
                padding: "14px 15px",
                borderRadius: "11px",
                border: "1px solid rgba(255,255,255,0.14)",
                background: "rgba(255,255,255,0.07)",
                color: "#ffffff",
                fontSize: "15px",
                outline: "none",
                boxSizing: "border-box",
              }}
            />
          </div>

          {/* Error */}
          {error && (
            <p
              style={{
                margin: "0 0 18px",
                color: "#ff6b81",
                fontSize: "13px",
                textAlign: "center",
              }}
            >
              {error}
            </p>
          )}

          {/* Sign Up Button */}
          <button
            type="submit"
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
            }}
          >
            Create Account →
          </button>
        </form>

        {/* Login Link */}
        <p
          style={{
            textAlign: "center",
            marginTop: "22px",
            marginBottom: 0,
            color: "rgba(255,255,255,0.62)",
            fontSize: "14px",
          }}
        >
          Already have an account?{" "}
          <button
            type="button"
            onClick={() => navigate("/")}
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
            Login
          </button>
        </p>
      </div>
    </div>
  );
}

export default SignUp;