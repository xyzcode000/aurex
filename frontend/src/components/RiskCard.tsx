interface RiskCardProps {
  title: string;
  value: number;
}

function RiskCard({ title, value }: RiskCardProps) {
  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: "12px",
        padding: "20px",
        width: "180px",
        backgroundColor: "#ffffff",
        boxShadow: "0 2px 8px rgba(0, 0, 0, 0.08)",
      }}
    >
      <h3>{title}</h3>

      <p
        style={{
          fontSize: "28px",
          fontWeight: "bold",
          margin: "10px 0",
        }}
      >
        {value}%
      </p>
    </div>
  );
}

export default RiskCard;