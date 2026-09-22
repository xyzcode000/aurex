import type { RiskData } from "../types/risk";

export const riskData: RiskData = {
  project_id: "AUREX-001",
  cost_risk: 82,
  schedule_risk: 74,
  progress_risk: 91,
  anomaly_score: 63,
  overall_risk: 84,
  risk_level: "HIGH", 
   evidence: [
    "Project cost is above the planned budget",
    "Schedule is showing delays",
    "Progress is below expected level",
    "Anomaly detected in recent project data",
  ],
};