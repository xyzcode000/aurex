function ErrorState() {
  const handleRetry = () => {
    window.location.reload();
  };

  return (
    <div
      style={{
        padding: "30px",
        backgroundColor: "#f5f7fb",
        minHeight: "100vh",
      }}
    >
      <h1>Something Went Wrong</h1>

      <p>
        Aurex could not load the requested project data.
      </p>

      <button
        onClick={handleRetry}
        style={{
          marginTop: "20px",
          padding: "12px 20px",
          backgroundColor: "#dc2626",
          color: "white",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer",
        }}
      >
        Try Again
      </button>
    </div>
  );
}

export default ErrorState;