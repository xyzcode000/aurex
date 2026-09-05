import RiskCard from "../components/RiskCard";
import { riskData } from "../mocks/riskData";

function RiskCenter() {
  return (
    <div>
      <h1>Aurex Risk Center</h1>

      <p>Project ID: {riskData.project_id}</p>

      <div>
        <RiskCard title="Cost Risk" value={riskData.cost_risk} />
        <RiskCard title="Schedule Risk" value={riskData.schedule_risk} />
        <RiskCard title="Progress Risk" value={riskData.progress_risk} />
        <RiskCard title="Anomaly Score" value={riskData.anomaly_score} />
        <RiskCard title="Overall Risk" value={riskData.overall_risk} />
      </div>

      <h2>Risk Level: {riskData.risk_level}</h2>
    </div>
  );
}

export default RiskCenter;