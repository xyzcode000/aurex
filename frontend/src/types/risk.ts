export interface RiskData {
  project_id: string;
  cost_risk: number;
  schedule_risk: number;
  progress_risk: number;
  anomaly_score: number;
  overall_risk: number;
  risk_level: string;
  evidence: string[];
}