import { useEffect , useState } from "react";
import { predictionData } from "../mocks/predictionData";

function Prediction() {
  const [selectedProject, setSelectedProject] = useState(predictionData[0]);
useEffect(() => {
  const activeProject = JSON.parse(
    localStorage.getItem("aurex_active_project") || '{"project_id":"AUREX-001"}'
  );

  const matchedProject = predictionData.find(
    (project) => project.project_id === activeProject.project_id
  );

  if (matchedProject) {
    setSelectedProject(matchedProject);
  }
}, []);
  const getRiskClass = (level: string) => {
    if (level === "HIGH") return "high";
    if (level === "MEDIUM") return "medium";
    return "low";
  };

  return (
    <div className="prediction-page">
      <div className="prediction-header">
        <div>
          <p className="prediction-label">AUREX INTELLIGENCE</p>
          <h1>Prediction Center</h1>
          <p className="prediction-subtitle">
            Select a project to view its predicted risk and upcoming outlook.
          </p>
        </div>
      </div>

      <div className="project-section">
        <div className="section-heading">
          <h2>Your Projects</h2>
          <span>{predictionData.length} Projects</span>
        </div>

        <div className="project-list">
          {predictionData.map((project) => (
            <button
              key={project.project_id}
              className={`project-badge ${
                selectedProject.project_id === project.project_id
                  ? "selected"
                  : ""
              }`}
              onClick={() => setSelectedProject(project)}
            >
              <div className="project-badge-name">
                {project.project_name}
              </div>

              <div className="project-badge-description">
                {project.description}
              </div>

              <div className="project-badge-footer">
                <span>{project.project_id}</span>
                <span>View Prediction →</span>
              </div>
            </button>
          ))}
        </div>

        <button className="view-more-button">
          View More →
        </button>
      </div>

      <div className="prediction-result">
        <div className="result-header">
          <div>
            <p className="result-label">SELECTED PROJECT</p>
            <h2>{selectedProject.project_name}</h2>
            <p>{selectedProject.description}</p>
          </div>

          <div
            className={`risk-badge ${getRiskClass(
              selectedProject.predicted_risk_level
            )}`}
          >
            {selectedProject.predicted_risk_level} RISK
          </div>
        </div>

        <div className="prediction-grid">
          <div className="prediction-card main-score">
            <span>Predicted Risk Score</span>
            <strong>{selectedProject.predicted_risk_score}%</strong>
            <small>Predicted</small>
          </div>

          <div className="prediction-card">
            <span>Confidence</span>
            <strong>{selectedProject.confidence}%</strong>
            <small>Model confidence</small>
          </div>

          <div className="prediction-card">
            <span>Prediction Period</span>
            <strong>{selectedProject.prediction_period}</strong>
            <small>Expected outlook</small>
          </div>
        </div>

        <div className="prediction-insight">
          <div className="insight-icon">AI</div>

          <div>
            <h3>Prediction Insight</h3>
            <p>
              Based on the current project intelligence,{" "}
              <strong>{selectedProject.project_name}</strong> has a predicted
              risk level of{" "}
              <strong>{selectedProject.predicted_risk_level}</strong> with a
              score of{" "}
              <strong>{selectedProject.predicted_risk_score}%</strong>.
            </p>
          </div>
        </div>
      </div>

      <style>{`
        .prediction-page {
          min-height: 100vh;
          padding: 42px;
          color: #f5f7ff;
          background:
            radial-gradient(circle at top right, rgba(91, 76, 255, 0.16), transparent 35%),
            radial-gradient(circle at bottom left, rgba(0, 212, 255, 0.08), transparent 30%),
            #070b17;
          font-family: Inter, system-ui, sans-serif;
          box-sizing: border-box;
        }

        .prediction-header {
          margin-bottom: 38px;
        }

        .prediction-label,
        .result-label {
          margin: 0 0 8px;
          font-size: 11px;
          font-weight: 800;
          letter-spacing: 2px;
          color: #8d9cff;
        }

        .prediction-header h1 {
          margin: 0;
          font-size: 34px;
          font-weight: 800;
          letter-spacing: -1px;
        }

        .prediction-subtitle {
          margin: 9px 0 0;
          color: #8f9bb5;
          font-size: 14px;
        }

        .project-section {
          padding: 25px;
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 22px;
          background: rgba(14, 19, 35, 0.78);
          backdrop-filter: blur(16px);
          box-shadow: 0 20px 60px rgba(0,0,0,0.25);
        }

        .section-heading {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 20px;
        }

        .section-heading h2 {
          margin: 0;
          font-size: 18px;
        }

        .section-heading span {
          color: #8d9cff;
          font-size: 12px;
          font-weight: 700;
        }

        .project-list {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 14px;
        }

        .project-badge {
          text-align: left;
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 17px;
          padding: 20px;
          background: rgba(255,255,255,0.025);
          color: white;
          cursor: pointer;
          transition: 0.25s ease;
        }

        .project-badge:hover {
          transform: translateY(-3px);
          border-color: rgba(120,130,255,0.45);
          background: rgba(120,130,255,0.07);
        }

        .project-badge.selected {
          border-color: rgba(120,130,255,0.75);
          background: linear-gradient(
            135deg,
            rgba(91,76,255,0.16),
            rgba(0,212,255,0.05)
          );
          box-shadow: 0 0 25px rgba(91,76,255,0.10);
        }

        .project-badge-name {
          font-size: 17px;
          font-weight: 800;
          margin-bottom: 8px;
        }

        .project-badge-description {
          min-height: 38px;
          color: #8f9bb5;
          font-size: 12px;
          line-height: 1.55;
        }

        .project-badge-footer {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-top: 16px;
          padding-top: 12px;
          border-top: 1px solid rgba(255,255,255,0.06);
          color: #78849d;
          font-size: 10px;
          font-weight: 700;
        }

        .project-badge-footer span:last-child {
          color: #9ca7ff;
        }

        .view-more-button {
          display: block;
          margin: 20px auto 0;
          padding: 10px 22px;
          border: 1px solid rgba(120,130,255,0.35);
          border-radius: 10px;
          background: rgba(120,130,255,0.07);
          color: #aab2ff;
          font-size: 12px;
          font-weight: 700;
          cursor: pointer;
          transition: 0.2s ease;
        }

        .view-more-button:hover {
          background: rgba(120,130,255,0.14);
          border-color: rgba(120,130,255,0.6);
        }

        .prediction-result {
          margin-top: 24px;
          padding: 28px;
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 22px;
          background: rgba(14, 19, 35, 0.78);
          backdrop-filter: blur(16px);
        }

        .result-header {
          display: flex;
          align-items: flex-start;
          justify-content: space-between;
          gap: 20px;
        }

        .result-header h2 {
          margin: 0;
          font-size: 25px;
        }

        .result-header p:last-child {
          margin: 7px 0 0;
          color: #8f9bb5;
          font-size: 12px;
        }

        .risk-badge {
          padding: 9px 15px;
          border-radius: 10px;
          font-size: 11px;
          font-weight: 900;
          letter-spacing: 0.7px;
          white-space: nowrap;
        }

        .risk-badge.high {
          color: #ff8e9b;
          background: rgba(255, 70, 90, 0.12);
          border: 1px solid rgba(255, 70, 90, 0.25);
        }

        .risk-badge.medium {
          color: #ffd27d;
          background: rgba(255, 180, 60, 0.12);
          border: 1px solid rgba(255, 180, 60, 0.25);
        }

        .risk-badge.low {
          color: #6ee7b7;
          background: rgba(30, 200, 130, 0.12);
          border: 1px solid rgba(30, 200, 130, 0.25);
        }

        .prediction-grid {
          display: grid;
          grid-template-columns: 1.3fr 1fr 1fr;
          gap: 14px;
          margin-top: 25px;
        }

        .prediction-card {
          padding: 21px;
          border-radius: 16px;
          background: rgba(255,255,255,0.035);
          border: 1px solid rgba(255,255,255,0.07);
        }

        .prediction-card span {
          display: block;
          color: #7f8ba5;
          font-size: 11px;
          margin-bottom: 10px;
        }

        .prediction-card strong {
          display: block;
          font-size: 25px;
          font-weight: 800;
        }

        .prediction-card small {
          display: block;
          margin-top: 7px;
          color: #65718b;
          font-size: 10px;
        }

        .main-score strong {
          color: #9ca7ff;
          font-size: 34px;
        }

        .prediction-insight {
          display: flex;
          gap: 15px;
          align-items: flex-start;
          margin-top: 18px;
          padding: 18px;
          border-radius: 15px;
          background: rgba(91,76,255,0.07);
          border: 1px solid rgba(120,130,255,0.12);
        }

        .insight-icon {
          min-width: 34px;
          height: 34px;
          display: grid;
          place-items: center;
          border-radius: 9px;
          background: rgba(120,130,255,0.15);
          color: #aab2ff;
          font-size: 10px;
          font-weight: 900;
        }

        .prediction-insight h3 {
          margin: 0 0 5px;
          font-size: 13px;
        }

        .prediction-insight p {
          margin: 0;
          color: #8f9bb5;
          font-size: 12px;
          line-height: 1.6;
        }

        .prediction-insight strong {
          color: #dce1ff;
        }

        @media (max-width: 800px) {
          .prediction-page {
            padding: 22px;
          }

          .project-list,
          .prediction-grid {
            grid-template-columns: 1fr;
          }

          .result-header {
            flex-direction: column;
          }
        }
      `}</style>
    </div>
  );
}

export default Prediction;