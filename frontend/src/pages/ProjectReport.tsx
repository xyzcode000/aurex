import { useEffect, useMemo, useState } from "react";

type Project = {
  project_id: string;
  project_name: string;
  description: string;
  planned_budget: number;
  actual_budget: number;
  planned_timeline: number;
  actual_timeline: number;
  progress: number;
  status: string;
  risk_level: "HIGH" | "MEDIUM" | "LOW";
  predicted_score: number;
  confidence: number;
};

const projects: Project[] = [
  {
    project_id: "AUREX-001",
    project_name: "Metro Construction",
    description:
      "Urban metro construction project focused on infrastructure development and expansion.",
    planned_budget: 25,
    actual_budget: 28,
    planned_timeline: 12,
    actual_timeline: 14,
    progress: 68,
    status: "At Risk",
    risk_level: "HIGH",
    predicted_score: 87,
    confidence: 92,
  },
  {
    project_id: "AUREX-002",
    project_name: "Smart City Development",
    description:
      "Smart infrastructure project focused on technology, connectivity and city development.",
    planned_budget: 40,
    actual_budget: 39,
    planned_timeline: 18,
    actual_timeline: 17,
    progress: 82,
    status: "On Track",
    risk_level: "MEDIUM",
    predicted_score: 64,
    confidence: 88,
  },
  {
    project_id: "AUREX-003",
    project_name: "Highway Expansion",
    description:
      "Highway expansion project focused on improving transportation capacity and connectivity.",
    planned_budget: 32,
    actual_budget: 36,
    planned_timeline: 16,
    actual_timeline: 20,
    progress: 54,
    status: "Delayed",
    risk_level: "HIGH",
    predicted_score: 81,
    confidence: 90,
  },
  {
    project_id: "AUREX-004",
    project_name: "River Bridge Project",
    description:
      "Bridge construction project focused on improving regional transportation and connectivity.",
    planned_budget: 22,
    actual_budget: 23,
    planned_timeline: 10,
    actual_timeline: 11,
    progress: 73,
    status: "Monitoring",
    risk_level: "MEDIUM",
    predicted_score: 58,
    confidence: 90,
  },
];

function ProjectReport() {
  const [selectedProjectId, setSelectedProjectId] = useState("AUREX-001");
  useEffect(() => {
  const activeProject = JSON.parse(
    localStorage.getItem("aurex_active_project") ||
      '{"project_id":"AUREX-001"}'
  );

  const matchedProject = projects.find(
    (item) => item.project_id === activeProject.project_id
  );

  if (matchedProject) {
    setSelectedProjectId(matchedProject.project_id);
  }
}, []);
const [budgetScenario, setBudgetScenario] = useState(10);
  const [delayScenario, setDelayScenario] = useState(2);
  const [progressScenario, setProgressScenario] = useState(-10);

  const project = projects.find(
    (item) => item.project_id === selectedProjectId
  ) || projects[0];

  const budgetUsage = Math.round(
    (project.actual_budget / project.planned_budget) * 100
  );

  const budgetVariance = project.actual_budget - project.planned_budget;
  const timelineVariance =
    project.actual_timeline - project.planned_timeline;
  const remainingWork = 100 - project.progress;

  const simulatedBudget = Number(
    (project.actual_budget * (1 + budgetScenario / 100)).toFixed(1)
  );

  const simulatedTimeline = project.actual_timeline + delayScenario;

  const simulatedProgress = Math.max(
    0,
    Math.min(100, project.progress + progressScenario)
  );

  const simulatedRisk = useMemo(() => {
    let score = project.predicted_score;

    if (budgetScenario > 0) {
      score += budgetScenario * 0.7;
    }

    if (delayScenario > 0) {
      score += delayScenario * 2;
    }

    if (progressScenario < 0) {
      score += Math.abs(progressScenario) * 0.5;
    }

    return Math.min(99, Math.round(score));
  }, [
    project.predicted_score,
    budgetScenario,
    delayScenario,
    progressScenario,
  ]);

  const simulatedRiskLevel =
    simulatedRisk >= 75
      ? "HIGH"
      : simulatedRisk >= 50
        ? "MEDIUM"
        : "LOW";

  const riskClass = project.risk_level.toLowerCase();

  return (
    <div className="report-page">
      <style>{`
        * {
          box-sizing: border-box;
        }

        .report-page {
          min-height: 100vh;
          background:
            radial-gradient(circle at 15% 10%, rgba(74, 110, 255, 0.16), transparent 28%),
            radial-gradient(circle at 85% 20%, rgba(157, 78, 221, 0.12), transparent 28%),
            #070b16;
          color: #f4f7ff;
          padding: 34px;
          font-family: Inter, Arial, sans-serif;
        }

        .report-container {
          max-width: 1280px;
          margin: 0 auto;
        }

        .report-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          gap: 24px;
          margin-bottom: 28px;
        }

        .eyebrow {
          color: #7f9cff;
          font-size: 12px;
          font-weight: 800;
          letter-spacing: 2px;
          text-transform: uppercase;
          margin-bottom: 8px;
        }

        .report-title {
          margin: 0;
          font-size: 34px;
          line-height: 1.1;
          letter-spacing: -1px;
        }

        .report-subtitle {
          color: #9aa7c2;
          margin: 10px 0 0;
          max-width: 760px;
          line-height: 1.6;
        }

        .project-selector {
          min-width: 270px;
          background: rgba(17, 24, 43, 0.88);
          border: 1px solid #26324f;
          border-radius: 14px;
          padding: 14px;
        }

        .selector-label {
          display: block;
          color: #8490aa;
          font-size: 11px;
          font-weight: 700;
          margin-bottom: 8px;
          text-transform: uppercase;
          letter-spacing: 1px;
        }

        .project-selector select {
          width: 100%;
          background: #0b1020;
          color: #fff;
          border: 1px solid #35415f;
          border-radius: 9px;
          padding: 11px;
          outline: none;
        }

        .identity-card {
          background: linear-gradient(135deg, rgba(20, 29, 52, 0.96), rgba(11, 17, 31, 0.96));
          border: 1px solid #293654;
          border-radius: 20px;
          padding: 24px;
          margin-bottom: 24px;
          box-shadow: 0 18px 60px rgba(0, 0, 0, 0.25);
        }

        .identity-top {
          display: flex;
          justify-content: space-between;
          gap: 20px;
          align-items: center;
        }

        .project-id {
          color: #8290ae;
          font-size: 12px;
          margin-bottom: 7px;
        }

        .project-name {
          font-size: 25px;
          font-weight: 800;
          margin-bottom: 8px;
        }

        .project-description {
          color: #9aa7c2;
          line-height: 1.5;
        }

        .risk-badge {
          padding: 9px 16px;
          border-radius: 999px;
          font-size: 12px;
          font-weight: 900;
          letter-spacing: 1px;
          white-space: nowrap;
        }

        .risk-high {
          background: rgba(255, 77, 92, 0.14);
          border: 1px solid rgba(255, 77, 92, 0.45);
          color: #ff6675;
        }

        .risk-medium {
          background: rgba(255, 184, 77, 0.12);
          border: 1px solid rgba(255, 184, 77, 0.4);
          color: #ffc56d;
        }

        .risk-low {
          background: rgba(65, 220, 155, 0.12);
          border: 1px solid rgba(65, 220, 155, 0.4);
          color: #5ee6a8;
        }

        .intelligence-flow {
          display: grid;
          grid-template-columns: repeat(6, 1fr);
          gap: 10px;
          margin-bottom: 24px;
        }

        .flow-item {
          background: #0e1527;
          border: 1px solid #222e49;
          border-radius: 12px;
          padding: 13px;
        }

        .flow-number {
          color: #7180a0;
          font-size: 11px;
          font-weight: 800;
        }

        .flow-title {
          font-size: 12px;
          font-weight: 800;
          margin-top: 6px;
        }

        .flow-type {
          color: #7485aa;
          font-size: 9px;
          font-weight: 800;
          margin-top: 5px;
          letter-spacing: 0.8px;
        }

        .section {
          background: rgba(12, 18, 33, 0.94);
          border: 1px solid #25314c;
          border-radius: 18px;
          padding: 24px;
          margin-bottom: 22px;
        }

        .section-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 15px;
          margin-bottom: 20px;
        }

        .section-number {
          color: #7180a0;
          font-size: 11px;
          font-weight: 800;
        }

        .section-title {
          margin: 4px 0 0;
          font-size: 20px;
        }

        .type-badge {
          border: 1px solid #34415f;
          border-radius: 999px;
          padding: 6px 10px;
          color: #9aabcf;
          font-size: 10px;
          font-weight: 900;
          letter-spacing: 1px;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 12px;
        }

        .stat {
          background: #0a1020;
          border: 1px solid #202c47;
          border-radius: 13px;
          padding: 16px;
        }

        .stat-label {
          color: #7785a4;
          font-size: 11px;
          margin-bottom: 8px;
        }

        .stat-value {
          font-size: 23px;
          font-weight: 850;
        }

        .stat-note {
          color: #667694;
          font-size: 10px;
          margin-top: 5px;
        }

        .evidence-list {
          display: grid;
          gap: 12px;
          padding: 0;
          margin: 0;
          list-style: none;
        }

        .evidence-item {
          background: #0a1020;
          border: 1px solid #202c47;
          border-radius: 13px;
          padding: 15px 17px;
          color: #b9c4da;
          line-height: 1.65;
        }

        .evidence-item strong {
          color: #f0f4ff;
        }

        .finding-box {
          border: 1px solid rgba(130, 156, 255, 0.28);
          background: linear-gradient(
            135deg,
            rgba(52, 72, 130, 0.2),
            rgba(12, 18, 33, 0.9)
          );
          border-radius: 15px;
          padding: 20px;
          margin-bottom: 14px;
        }

        .finding-label {
          color: #8da4ff;
          font-size: 11px;
          font-weight: 900;
          letter-spacing: 1px;
          text-transform: uppercase;
          margin-bottom: 10px;
        }

        .finding-text {
          color: #d4dcf0;
          line-height: 1.75;
          margin: 0;
        }

        .investigation-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 14px;
        }

        .investigation-card {
          background: #0a1020;
          border: 1px solid #202c47;
          border-radius: 14px;
          padding: 18px;
        }

        .investigation-card h4 {
          margin: 0 0 10px;
          font-size: 14px;
        }

        .investigation-card p {
          margin: 0;
          color: #9faac0;
          line-height: 1.65;
          font-size: 13px;
        }

        .support-list {
          margin: 0;
          padding-left: 20px;
          color: #aeb9cf;
        }

        .support-list li {
          margin-bottom: 12px;
          line-height: 1.65;
        }

        .support-list strong {
          color: #f2f5ff;
        }

        .scenario-warning {
          display: inline-block;
          padding: 7px 11px;
          border-radius: 999px;
          background: rgba(255, 174, 66, 0.1);
          border: 1px solid rgba(255, 174, 66, 0.32);
          color: #ffc66e;
          font-size: 10px;
          font-weight: 900;
          letter-spacing: 1px;
          margin-bottom: 18px;
        }

        .scenario-controls {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 14px;
          margin-bottom: 20px;
        }

        .control-card {
          background: #0a1020;
          border: 1px solid #202c47;
          border-radius: 14px;
          padding: 17px;
        }

        .control-top {
          display: flex;
          justify-content: space-between;
          margin-bottom: 12px;
        }

        .control-title {
          font-size: 12px;
          font-weight: 800;
        }

        .control-value {
          color: #8ea4ff;
          font-weight: 900;
        }

        input[type="range"] {
          width: 100%;
          accent-color: #8098ff;
        }

        .scenario-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 14px;
          margin-bottom: 20px;
        }

        .scenario-box {
          background: #0a1020;
          border: 1px solid #202c47;
          border-radius: 14px;
          padding: 18px;
        }

        .scenario-box h4 {
          margin: 0 0 12px;
          font-size: 13px;
        }

        .scenario-value {
          font-size: 25px;
          font-weight: 900;
        }

        .scenario-note {
          color: #72809d;
          font-size: 10px;
          margin-top: 5px;
        }

        .consequence-chain {
          display: flex;
          align-items: stretch;
          gap: 8px;
          overflow-x: auto;
          padding-bottom: 5px;
        }

        .chain-item {
          min-width: 155px;
          background: #0a1020;
          border: 1px solid #2a3652;
          border-radius: 12px;
          padding: 15px;
        }

        .chain-step {
          color: #70809f;
          font-size: 10px;
          font-weight: 800;
        }

        .chain-item strong {
          display: block;
          margin-top: 6px;
          font-size: 12px;
          line-height: 1.4;
        }

        .chain-arrow {
          display: flex;
          align-items: center;
          color: #647394;
          font-size: 18px;
        }

        .sim-result {
          margin-top: 20px;
          border-radius: 16px;
          border: 1px solid rgba(255, 94, 105, 0.35);
          background: rgba(255, 70, 90, 0.06);
          padding: 20px;
        }

        .sim-result-label {
          color: #ff7a85;
          font-size: 10px;
          font-weight: 900;
          letter-spacing: 1px;
          margin-bottom: 8px;
        }

        .sim-result h3 {
          margin: 0 0 8px;
        }

        .sim-result p {
          color: #aeb9cf;
          line-height: 1.6;
          margin: 0;
        }

        .decision-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 14px;
        }

        .decision-card {
          background: #0a1020;
          border: 1px solid #263452;
          border-radius: 14px;
          padding: 19px;
        }

        .decision-number {
          color: #8198ff;
          font-size: 12px;
          font-weight: 900;
        }

        .decision-card h4 {
          margin: 8px 0;
        }

        .decision-card p {
          color: #9faac0;
          line-height: 1.65;
          font-size: 13px;
          margin: 0;
        }

        .final-summary {
          border: 1px solid rgba(111, 138, 255, 0.3);
          background: linear-gradient(
            135deg,
            rgba(43, 61, 116, 0.24),
            rgba(10, 16, 31, 0.96)
          );
          border-radius: 18px;
          padding: 24px;
        }

        .summary-title {
          margin: 0 0 10px;
          font-size: 20px;
        }

        .summary-text {
          margin: 0;
          color: #b8c3d9;
          line-height: 1.75;
        }

        @media (max-width: 1000px) {
          .intelligence-flow {
            grid-template-columns: repeat(3, 1fr);
          }

          .stats-grid {
            grid-template-columns: repeat(2, 1fr);
          }

          .scenario-controls,
          .scenario-grid {
            grid-template-columns: 1fr;
          }
        }

        @media (max-width: 700px) {
          .report-page {
            padding: 18px;
          }

          .report-header,
          .identity-top {
            flex-direction: column;
          }

          .project-selector {
            width: 100%;
          }

          .intelligence-flow,
          .stats-grid,
          .investigation-grid,
          .decision-grid {
            grid-template-columns: 1fr;
          }

          .report-title {
            font-size: 27px;
          }
        }
      `}</style>

      <div className="report-container">
        {/* HEADER */}
        <div className="report-header">
          <div>
            <div className="eyebrow">Aurex Intelligence Engine</div>
            <h1 className="report-title">Project Intelligence Report</h1>
            <p className="report-subtitle">
              AUREX connects project risk, evidence, prediction, investigation,
              scenario analysis and decision support into one intelligence flow.
            </p>
          </div>

          <div className="project-selector">
            <span className="selector-label">Select Project</span>

            <select
              value={selectedProjectId}
              onChange={(event) => setSelectedProjectId(event.target.value)}
            >
              {projects.map((item) => (
                <option key={item.project_id} value={item.project_id}>
                  {item.project_id} — {item.project_name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* PROJECT IDENTITY */}
        <div className="identity-card">
          <div className="identity-top">
            <div>
              <div className="project-id">{project.project_id}</div>
              <div className="project-name">{project.project_name}</div>
              <div className="project-description">
                {project.description}
              </div>
            </div>

            <div className={`risk-badge risk-${riskClass}`}>
              {project.risk_level} RISK
            </div>
          </div>
        </div>

        {/* INTELLIGENCE FLOW */}
        <div className="intelligence-flow">
          <div className="flow-item">
            <div className="flow-number">01</div>
            <div className="flow-title">Risk Assessment</div>
            <div className="flow-type">OBSERVED</div>
          </div>

          <div className="flow-item">
            <div className="flow-number">02</div>
            <div className="flow-title">Evidence & Signals</div>
            <div className="flow-type">OBSERVED</div>
          </div>

          <div className="flow-item">
            <div className="flow-number">03</div>
            <div className="flow-title">Risk Prediction</div>
            <div className="flow-type">PREDICTED</div>
          </div>

          <div className="flow-item">
            <div className="flow-number">04</div>
            <div className="flow-title">AI Investigation</div>
            <div className="flow-type">FINDING</div>
          </div>

          <div className="flow-item">
            <div className="flow-number">05</div>
            <div className="flow-title">What-if Scenario</div>
            <div className="flow-type">SIMULATED</div>
          </div>

          <div className="flow-item">
            <div className="flow-number">06</div>
            <div className="flow-title">Decision Support</div>
            <div className="flow-type">RECOMMENDED</div>
          </div>
        </div>

        {/* 01 RISK */}
        <section className="section">
          <div className="section-header">
            <div>
              <div className="section-number">01 / RISK ASSESSMENT</div>
              <h2 className="section-title">Current Project Risk</h2>
            </div>

            <div className="type-badge">OBSERVED</div>
          </div>

          <div className="stats-grid">
            <div className="stat">
              <div className="stat-label">Planned Budget</div>
              <div className="stat-value">₹{project.planned_budget}L</div>
              <div className="stat-note">Original baseline</div>
            </div>

            <div className="stat">
              <div className="stat-label">Actual Budget</div>
              <div className="stat-value">₹{project.actual_budget}L</div>
              <div className="stat-note">
                +₹{budgetVariance}L variance
              </div>
            </div>

            <div className="stat">
              <div className="stat-label">Progress</div>
              <div className="stat-value">{project.progress}%</div>
              <div className="stat-note">
                {remainingWork}% work remaining
              </div>
            </div>

            <div className="stat">
              <div className="stat-label">Timeline Variance</div>
              <div className="stat-value">+{timelineVariance} mo</div>
              <div className="stat-note">
                {project.actual_timeline} vs {project.planned_timeline} months
              </div>
            </div>
          </div>
        </section>

        {/* 02 EVIDENCE */}
        <section className="section">
          <div className="section-header">
            <div>
              <div className="section-number">02 / EVIDENCE & SIGNALS</div>
              <h2 className="section-title">What AUREX Observed</h2>
            </div>

            <div className="type-badge">OBSERVED</div>
          </div>

          <ul className="evidence-list">
            <li className="evidence-item">
              <strong>Budget-progress mismatch:</strong> The project has
              reached only {project.progress}% completion, while spending has
              already reached {budgetUsage}% of the planned budget.
            </li>

            <li className="evidence-item">
              <strong>Schedule exposure:</strong> The planned timeline was{" "}
              {project.planned_timeline} months, but the project has extended
              to {project.actual_timeline} months —{" "}
              {timelineVariance} month(s) beyond plan.
            </li>

            <li className="evidence-item">
              <strong>Cost is growing faster than physical completion:</strong>{" "}
              Budget usage has crossed the original baseline while a
              significant portion of the work remains incomplete.
            </li>

            <li className="evidence-item">
              <strong>Multiple signals are aligned:</strong> Cost variance,
              schedule extension and incomplete progress are pointing in the
              same direction rather than appearing as an isolated metric.
            </li>

            <li className="evidence-item">
              <strong>Attention signal:</strong> The remaining {remainingWork}%
              of work must be completed after the project has already crossed
              its planned budget and timeline.
            </li>
          </ul>
        </section>

        {/* 03 PREDICTION */}
        <section className="section">
          <div className="section-header">
            <div>
              <div className="section-number">03 / RISK PREDICTION</div>
              <h2 className="section-title">Forward Risk Signal</h2>
            </div>

            <div className="type-badge">PREDICTED</div>
          </div>

          <div className="stats-grid">
            <div className="stat">
              <div className="stat-label">Predicted Risk Score</div>
              <div className="stat-value">{project.predicted_score}%</div>
              <div className="stat-note">Forward-looking signal</div>
            </div>

            <div className="stat">
              <div className="stat-label">Predicted Level</div>
              <div className="stat-value">{project.risk_level}</div>
              <div className="stat-note">Prediction output</div>
            </div>

            <div className="stat">
              <div className="stat-label">Confidence</div>
              <div className="stat-value">{project.confidence}%</div>
              <div className="stat-note">Model confidence</div>
            </div>

            <div className="stat">
              <div className="stat-label">Signal Horizon</div>
              <div className="stat-value">Next</div>
              <div className="stat-note">Monitoring period</div>
            </div>
          </div>
        </section>

        {/* 04 AI INVESTIGATION */}
        <section className="section">
          <div className="section-header">
            <div>
              <div className="section-number">04 / AI INVESTIGATION</div>
              <h2 className="section-title">Why Is This Project At Risk?</h2>
            </div>

            <div className="type-badge">FINDING</div>
          </div>

          <div className="finding-box">
            <div className="finding-label">Hidden Pattern Detected</div>

            <p className="finding-text">
              AUREX detected a widening gap between money spent and physical
              work completed. The project has consumed more budget than its
              current completion level would normally suggest, while the
              timeline has already extended beyond the original plan.
            </p>
          </div>

          <div className="investigation-grid">
            <div className="investigation-card">
              <h4>What AUREX Connected</h4>

              <p>
                Spending has crossed the original baseline before physical
                completion, while the project has also moved beyond its planned
                timeline.
              </p>
            </div>

            <div className="investigation-card">
              <h4>Why This Matters</h4>

              <p>
                The concern is not simply that the project is over budget. The
                remaining work is being carried forward after the original
                budget baseline has already been exceeded.
              </p>
            </div>

            <div className="investigation-card">
              <h4>Investigation Conclusion</h4>

              <p>
                The project may be entering a higher-cost completion phase,
                where finishing the remaining work could require additional
                resources or time.
              </p>
            </div>

            <div className="investigation-card">
              <h4>What Should Be Investigated</h4>

              <p>
                Identify which work packages are consuming disproportionate
                budget or time instead of treating the entire project as one
                uniform risk.
              </p>
            </div>
          </div>

          <div style={{ marginTop: 16 }}>
            <ul className="evidence-list">
              <li className="evidence-item">
                <strong>Supporting evidence:</strong> Planned budget ₹
                {project.planned_budget}L → Actual budget ₹
                {project.actual_budget}L
              </li>

              <li className="evidence-item">
                <strong>Physical completion:</strong> {project.progress}% —
                remaining work {remainingWork}%
              </li>

              <li className="evidence-item">
                <strong>Timeline:</strong> {project.planned_timeline} months
                planned → {project.actual_timeline} months actual
              </li>
            </ul>
          </div>
        </section>

        {/* 05 WHAT IF */}
        <section className="section">
          <div className="section-header">
            <div>
              <div className="section-number">05 / WHAT-IF SIMULATION</div>
              <h2 className="section-title">AUREX What-if Engine</h2>
            </div>

            <div className="type-badge">SIMULATED</div>
          </div>

          <div className="scenario-warning">
            SIMULATED — NOT AN ACTUAL PROJECT OUTCOME
          </div>

          <div className="scenario-controls">
            <div className="control-card">
              <div className="control-top">
                <span className="control-title">Budget Change</span>
                <span className="control-value">+{budgetScenario}%</span>
              </div>

              <input
                type="range"
                min="0"
                max="30"
                step="5"
                value={budgetScenario}
                onChange={(event) =>
                  setBudgetScenario(Number(event.target.value))
                }
              />
            </div>

            <div className="control-card">
              <div className="control-top">
                <span className="control-title">Additional Delay</span>
                <span className="control-value">
                  +{delayScenario} months
                </span>
              </div>

              <input
                type="range"
                min="0"
                max="6"
                step="1"
                value={delayScenario}
                onChange={(event) =>
                  setDelayScenario(Number(event.target.value))
                }
              />
            </div>

            <div className="control-card">
              <div className="control-top">
                <span className="control-title">Progress Change</span>
                <span className="control-value">
                  {progressScenario}%
                </span>
              </div>

              <input
                type="range"
                min="-20"
                max="10"
                step="5"
                value={progressScenario}
                onChange={(event) =>
                  setProgressScenario(Number(event.target.value))
                }
              />
            </div>
          </div>

          <div className="scenario-grid">
            <div className="scenario-box">
              <h4>Baseline Budget</h4>
              <div className="scenario-value">
                ₹{project.actual_budget}L
              </div>
              <div className="scenario-note">Current observed value</div>
            </div>

            <div className="scenario-box">
              <h4>Scenario Budget</h4>
              <div className="scenario-value">
                ₹{simulatedBudget}L
              </div>
              <div className="scenario-note">
                If spending changes by +{budgetScenario}%
              </div>
            </div>

            <div className="scenario-box">
              <h4>Scenario Timeline</h4>
              <div className="scenario-value">
                {simulatedTimeline} mo
              </div>
              <div className="scenario-note">
                If delay increases by {delayScenario} month(s)
              </div>
            </div>

            <div className="scenario-box">
              <h4>Baseline Progress</h4>
              <div className="scenario-value">{project.progress}%</div>
              <div className="scenario-note">Current observed progress</div>
            </div>

            <div className="scenario-box">
              <h4>Scenario Progress</h4>
              <div className="scenario-value">{simulatedProgress}%</div>
              <div className="scenario-note">Simulated progress level</div>
            </div>

            <div className="scenario-box">
              <h4>Simulated Risk</h4>
              <div className="scenario-value">{simulatedRisk}%</div>
              <div className="scenario-note">
                Simulated level: {simulatedRiskLevel}
              </div>
            </div>
          </div>

          <h3 style={{ marginBottom: 14 }}>Potential Consequence Chain</h3>

          <div className="consequence-chain">
            <div className="chain-item">
              <div className="chain-step">01</div>
              <strong>Delay increases</strong>
            </div>

            <div className="chain-arrow">→</div>

            <div className="chain-item">
              <div className="chain-step">02</div>
              <strong>Project duration may extend</strong>
            </div>

            <div className="chain-arrow">→</div>

            <div className="chain-item">
              <div className="chain-step">03</div>
              <strong>Additional resource / operating exposure</strong>
            </div>

            <div className="chain-arrow">→</div>

            <div className="chain-item">
              <div className="chain-step">04</div>
              <strong>Final expenditure may increase</strong>
            </div>

            <div className="chain-arrow">→</div>

            <div className="chain-item">
              <div className="chain-step">05</div>
              <strong>Further budget pressure</strong>
            </div>
          </div>

          <div className="sim-result">
            <div className="sim-result-label">
              SIMULATED RESULT — NOT ACTUAL
            </div>

            <h3>Potential Scenario Impact</h3>

            <p>
              Under this scenario, additional delay combined with increased
              spending may extend project exposure and create further pressure
              on the remaining budget. This is a what-if analysis only and
              should not be interpreted as an actual project outcome.
            </p>
          </div>
        </section>

        {/* 06 DECISION SUPPORT */}
        <section className="section">
          <div className="section-header">
            <div>
              <div className="section-number">06 / DECISION SUPPORT</div>
              <h2 className="section-title">What Should Be Investigated Next?</h2>
            </div>

            <div className="type-badge">RECOMMENDED</div>
          </div>

          <div className="decision-grid">
            <div className="decision-card">
              <div className="decision-number">01</div>

              <h4>Investigate the cost-progress gap</h4>

              <p>
                Review the work packages contributing to the budget increase
                and compare expenditure against completed work before approving
                further spending.
              </p>
            </div>

            <div className="decision-card">
              <div className="decision-number">02</div>

              <h4>Protect the remaining schedule</h4>

              <p>
                Prioritize delayed or critical activities and evaluate recovery
                actions before schedule variance expands further.
              </p>
            </div>
          </div>

          <div className="finding-box" style={{ marginTop: 16, marginBottom: 0 }}>
            <div className="finding-label">AUREX Decision Signal</div>

            <p className="finding-text">
              Do not treat the current risk as a single-metric problem. Cost,
              schedule and progress signals are interacting. Decisions should
              address both spending efficiency and schedule recovery.
            </p>
          </div>
        </section>

        {/* EXECUTIVE SUMMARY */}
        <section className="final-summary">
          <h2 className="summary-title">Executive Intelligence Summary</h2>

          <p className="summary-text">
            AUREX has connected the project's observed risk signals with
            supporting evidence, a forward-looking prediction, an AI-detected
            investigation pattern, and a clearly labelled what-if simulation.
            The key concern is the relationship between spending, physical
            completion and schedule exposure. The recommended next step is to
            investigate the work packages driving the cost-progress gap while
            protecting critical activities from further schedule expansion.
          </p>
        </section>
      </div>
    </div>
  );
}

export default ProjectReport;