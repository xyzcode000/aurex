function LoadingState() {
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
          maxWidth: "460px",
          padding: "42px",
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
            width: "58px",
            height: "58px",
            margin: "0 auto 22px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            borderRadius: "16px",
            background: "linear-gradient(135deg, #2563eb, #7c3aed)",
            fontSize: "25px",
            fontWeight: "800",
            boxShadow: "0 0 30px rgba(99,102,241,0.4)",
          }}
        >
          A
        </div>

        <h1
          style={{
            margin: "0 0 10px",
            fontSize: "28px",
            fontWeight: "800",
          }}
        >
          Loading Aurex...
        </h1>

        <p
          style={{
            margin: 0,
            color: "rgba(255,255,255,0.55)",
            fontSize: "14px",
            lineHeight: 1.6,
          }}
        >
          Please wait while Aurex loads the project intelligence data.
        </p>

        <div
          style={{
            width: "100%",
            height: "5px",
            marginTop: "28px",
            borderRadius: "10px",
            background: "rgba(255,255,255,0.08)",
            overflow: "hidden",
          }}
        >
          <div
            style={{
              width: "45%",
              height: "100%",
              borderRadius: "10px",
              background: "linear-gradient(90deg, #2563eb, #7c3aed)",
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default LoadingState;