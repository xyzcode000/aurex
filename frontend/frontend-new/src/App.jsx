import { useEffect, useMemo, useState } from "react";
import "./App.css";

const projects = [
  {
    id: "PRJ-001",
    name: "Metro Infrastructure",
    category: "Infrastructure",
    owner: "Urban Development",
    status: "On Track",
    priority: "High",
    progress: 82,
    budget: "₹48.2 Cr",
    spent: "₹37.6 Cr",
    budgetValue: 48.2,
    spentValue: 37.6,
    schedule: "12 days ahead",
    scheduleDays: 12,
    scheduleDirection: "ahead",
  },
  {
    id: "PRJ-002",
    name: "Digital Citizen Hub",
    category: "Technology",
    owner: "Digital Services",
    status: "Review",
    priority: "Medium",
    progress: 64,
    budget: "₹18.7 Cr",
    spent: "₹13.9 Cr",
    budgetValue: 18.7,
    spentValue: 13.9,
    schedule: "4 days behind",
    scheduleDays: 4,
    scheduleDirection: "behind",
  },
  {
    id: "PRJ-003",
    name: "Green Corridor",
    category: "Environment",
    owner: "Public Works",
    status: "On Track",
    priority: "Medium",
    progress: 91,
    budget: "₹32.4 Cr",
    spent: "₹28.1 Cr",
    budgetValue: 32.4,
    spentValue: 28.1,
    schedule: "8 days ahead",
    scheduleDays: 8,
    scheduleDirection: "ahead",
  },
  {
    id: "PRJ-004",
    name: "Water Network Upgrade",
    category: "Infrastructure",
    owner: "Utilities",
    status: "At Risk",
    priority: "Critical",
    progress: 47,
    budget: "₹26.8 Cr",
    spent: "₹22.9 Cr",
    budgetValue: 26.8,
    spentValue: 22.9,
    schedule: "18 days behind",
    scheduleDays: 18,
    scheduleDirection: "behind",
  },
  {
    id: "PRJ-005",
    name: "Smart Mobility Grid",
    category: "Technology",
    owner: "Transport Authority",
    status: "On Track",
    priority: "Low",
    progress: 76,
    budget: "₹41.3 Cr",
    spent: "₹31.2 Cr",
    budgetValue: 41.3,
    spentValue: 31.2,
    schedule: "6 days ahead",
    scheduleDays: 6,
    scheduleDirection: "ahead",
  },
];

const navigation = [
  { label: "Portfolio", icon: "◈" },
  { label: "Risk Center", icon: "◇" },
  { label: "Predictions", icon: "⌁" },
  { label: "Projects", icon: "▦" },
  { label: "Warnings", icon: "△" },
  { label: "Investigation", icon: "⌖" },
  { label: "Scenarios", icon: "◌" },
  { label: "Reports", icon: "▤" },
];

const statusClass = {
  "On Track": "success",
  Review: "warning",
  "At Risk": "danger",
};

const severityValue = {
  High: 3,
  Moderate: 2,
  Low: 1,
};

function getRiskSignals(project) {
  const budgetUtilization = Math.round(
    (project.spentValue / project.budgetValue) * 100
  );

  const scheduleRisk =
    project.scheduleDirection === "behind" && project.scheduleDays >= 14
      ? "High"
      : project.scheduleDirection === "behind"
        ? "Moderate"
        : "Low";

  const budgetRisk =
    budgetUtilization >= 85
      ? "High"
      : budgetUtilization >= 70
        ? "Moderate"
        : "Low";

  const executionRisk =
    project.status === "At Risk"
      ? "High"
      : project.status === "Review"
        ? "Moderate"
        : project.priority === "High"
          ? "Moderate"
          : "Low";

  const dimensions = [scheduleRisk, budgetRisk, executionRisk];

  const highCount = dimensions.filter((risk) => risk === "High").length;

  const overallRisk =
    highCount >= 2
      ? "High"
      : dimensions.includes("Moderate")
        ? "Moderate"
        : "Low";

  return {
    budgetUtilization,
    scheduleRisk,
    budgetRisk,
    executionRisk,
    overallRisk,
  };
}

function riskClass(value) {
  return value.toLowerCase();
}

function ModulePage({
  eyebrow,
  title,
  description,
  metrics,
  rows,
  onProject,
  actionLabel,
}) {
  return (
    <section className="module-page">
      <div className="module-page-header">
        <div>
          <div className="eyebrow">{eyebrow}</div>
          <h1>{title}</h1>
          <p>{description}</p>
        </div>

        <span className="module-live">LIVE SNAPSHOT</span>
      </div>

      <div className="module-metrics">
        {metrics.map(([label, value, detail]) => (
          <div className="module-metric" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
            <small>{detail}</small>
          </div>
        ))}
      </div>

      <div className="module-register">
        <div className="section-heading">
          <div>
            <span className="eyebrow">OPERATIONAL REGISTER</span>
            <h2>Current project signals</h2>
          </div>

          <span className="record-count">{rows.length} RECORDS</span>
        </div>

        <div className="module-table-head">
          <span>PROJECT</span>
          <span>HEALTH</span>
          <span>RISK</span>
          <span>SCHEDULE</span>
          <span>ACTION</span>
        </div>

        {rows.map((project) => (
          <button
            className="module-project-row"
            key={project.id}
            onClick={() => onProject(project)}
          >
            <div>
              <small>{project.id}</small>
              <strong>{project.name}</strong>
              <span>
                {project.category} / {project.owner}
              </span>
            </div>

            <div>
              <strong>{project.status}</strong>
              <span>{project.progress}% progress</span>
            </div>

            <div>
              <strong className={riskClass(project.risk.overallRisk)}>
                {project.risk.overallRisk}
              </strong>
              <span>{project.risk.budgetUtilization}% budget used</span>
            </div>

            <div>
              <strong
                className={
                  project.scheduleDirection === "behind"
                    ? "negative"
                    : "positive"
                }
              >
                {project.scheduleDirection === "behind" ? "↓" : "↑"}{" "}
                {project.scheduleDays}d
              </strong>

              <span>
                {project.scheduleDirection === "behind" ? "BEHIND" : "AHEAD"}
              </span>
            </div>

            <div>
              <span>{actionLabel}</span>
              <b>↗</b>
            </div>
          </button>
        ))}
      </div>
    </section>
  );
}

function PendingPage({ eyebrow, title, description }) {
  return (
    <section className="module-page pending-page">
      <div className="module-page-header">
        <div>
          <div className="eyebrow">{eyebrow}</div>
          <h1>{title}</h1>
          <p>{description}</p>
        </div>

        <span className="module-live pending">BACKEND PENDING</span>
      </div>

      <div className="pending-workspace">
        <span className="eyebrow">INTEGRATION STATE</span>

        <strong>READY FOR INTELLIGENCE SERVICE</strong>

        <p>
          Frontend workspace is available. This surface will display
          backend-driven values when the corresponding API contract is
          connected.
        </p>
      </div>
    </section>
  );
}

function App() {
  const [activePage, setActivePage] = useState("Portfolio");
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");
  const [selectedProject, setSelectedProject] = useState(null);
  const [commandOpen, setCommandOpen] = useState(false);

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (
        (event.ctrlKey || event.metaKey) &&
        event.key.toLowerCase() === "k"
      ) {
        event.preventDefault();
        setCommandOpen((open) => !open);
      }

      if (event.key === "Escape") {
        setCommandOpen(false);
        setSelectedProject(null);
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const projectsWithRisk = useMemo(
    () =>
      projects.map((project) => ({
        ...project,
        risk: getRiskSignals(project),
      })),
    []
  );

  const portfolioRisk = useMemo(() => {
    const totalBudget = projectsWithRisk.reduce(
      (sum, project) => sum + project.budgetValue,
      0
    );

    const totalSpent = projectsWithRisk.reduce(
      (sum, project) => sum + project.spentValue,
      0
    );

    const budgetUtilization = Math.round((totalSpent / totalBudget) * 100);

    const schedulePenalty = projectsWithRisk.reduce(
      (sum, project) =>
        sum +
        (project.scheduleDirection === "behind"
          ? project.scheduleDays
          : 0),
      0
    );

    const scheduleHealth = Math.max(0, 100 - schedulePenalty * 1.5);

    const executionConfidence = Math.round(
      projectsWithRisk.reduce((sum, project) => {
        if (project.risk.executionRisk === "High") return sum + 55;
        if (project.risk.executionRisk === "Moderate") return sum + 78;
        return sum + 94;
      }, 0) / projectsWithRisk.length
    );

    const portfolioScore = Math.max(
      0,
      Math.min(
        100,
        Math.round(
          scheduleHealth * 0.35 +
            (100 - budgetUtilization * 0.18) * 0.25 +
            executionConfidence * 0.4
        )
      )
    );

    const getExposure = (key) => {
      const values = projectsWithRisk.map((project) => project.risk[key]);

      if (values.includes("High")) return "High";
      if (values.includes("Moderate")) return "Moderate";

      return "Low";
    };

    const highRiskCount = projectsWithRisk.filter(
      (project) => project.risk.overallRisk === "High"
    ).length;

    const attentionCount = projectsWithRisk.filter(
      (project) => project.risk.overallRisk !== "Low"
    ).length;

    return {
      totalBudget,
      totalSpent,
      budgetUtilization,
      scheduleHealth: Math.round(scheduleHealth),
      executionConfidence,
      portfolioScore,
      highRiskCount,
      attentionCount,
      scheduleExposure: getExposure("scheduleRisk"),
      budgetExposure: getExposure("budgetRisk"),
      executionExposure: getExposure("executionRisk"),
      onScheduleCount: projectsWithRisk.filter(
        (project) => project.scheduleDirection === "ahead"
      ).length,
    };
  }, [projectsWithRisk]);

  const portfolioIntelligence = useMemo(() => {
    const signals = [
      {
        name: "Schedule Exposure",
        value: portfolioRisk.scheduleExposure,
        detail: `${
          projectsWithRisk.filter(
            (project) => project.risk.scheduleRisk !== "Low"
          ).length
        } project(s) with schedule variance`,
      },
      {
        name: "Budget Exposure",
        value: portfolioRisk.budgetExposure,
        detail: `${portfolioRisk.budgetUtilization}% of analyzed budget deployed`,
      },
      {
        name: "Execution Risk",
        value: portfolioRisk.executionExposure,
        detail: `${portfolioRisk.executionConfidence}% derived execution confidence`,
      },
    ];

    const primarySignal = signals.reduce((strongest, signal) => {
      if (!strongest) return signal;

      return severityValue[signal.value] > severityValue[strongest.value]
        ? signal
        : strongest;
    }, null);

    const projectScore = (project) => {
      const signalScore = [
        project.risk.scheduleRisk,
        project.risk.budgetRisk,
        project.risk.executionRisk,
      ].reduce((score, risk) => score + severityValue[risk], 0);

      const schedulePenalty =
        project.scheduleDirection === "behind" ? project.scheduleDays : 0;

      const priorityPenalty =
        project.priority === "Critical"
          ? 4
          : project.priority === "High"
            ? 2
            : 0;

      return signalScore + schedulePenalty + priorityPenalty;
    };

    const priorityProject = [...projectsWithRisk].sort(
      (a, b) => projectScore(b) - projectScore(a)
    )[0];

    return {
      primarySignal,
      priorityProject,
    };
  }, [portfolioRisk, projectsWithRisk]);

  const filteredProjects = useMemo(() => {
    const query = search.trim().toLowerCase();

    return projectsWithRisk.filter((project) => {
      const matchesSearch = [
        project.name,
        project.category,
        project.owner,
        project.id,
      ].some((value) => value.toLowerCase().includes(query));

      const matchesStatus =
        statusFilter === "All" || project.status === statusFilter;

      return matchesSearch && matchesStatus;
    });
  }, [search, statusFilter, projectsWithRisk]);

  /*
   * IMPORTANT:
   * warningRows is intentionally defined ONCE.
   * The previous App.jsx contained a duplicated warningRows declaration
   * followed by an extra closing brace, which caused the syntax error.
   */
  const warningRows = useMemo(
    () =>
      projectsWithRisk.flatMap((project) => {
        const rows = [];

        if (project.risk.scheduleRisk !== "Low") {
          rows.push({
            id: `${project.id}-schedule`,
            project,
            signal: "Schedule Exposure",
            severity: project.risk.scheduleRisk,
            impact:
              project.scheduleDirection === "behind"
                ? `${project.scheduleDays}d behind`
                : `${project.scheduleDays}d ahead`,
            state: project.status,
            detail:
              project.scheduleDirection === "behind"
                ? "Schedule variance requires review"
                : "Schedule variance detected",
          });
        }

        if (project.risk.budgetRisk !== "Low") {
          rows.push({
            id: `${project.id}-budget`,
            project,
            signal: "Budget Exposure",
            severity: project.risk.budgetRisk,
            impact: `${project.risk.budgetUtilization}% used`,
            state: `${project.priority} priority`,
            detail: "Budget utilization above low-risk threshold",
          });
        }

        if (project.risk.executionRisk !== "Low") {
          rows.push({
            id: `${project.id}-execution`,
            project,
            signal: "Execution Risk",
            severity: project.risk.executionRisk,
            impact: project.status,
            state: `${project.priority} priority`,
            detail: "Execution signal requires review",
          });
        }

        return rows;
      }),
    [projectsWithRisk]
  );

  const highWarningCount = useMemo(
    () =>
      warningRows.filter((warning) => warning.severity === "High").length,
    [warningRows]
  );

  const scheduleWarningCount = useMemo(
    () =>
      warningRows.filter(
        (warning) => warning.signal === "Schedule Exposure"
      ).length,
    [warningRows]
  );

  const budgetWarningCount = useMemo(
    () =>
      warningRows.filter(
        (warning) => warning.signal === "Budget Exposure"
      ).length,
    [warningRows]
  );

  const handleNavigation = (label) => {
    setActivePage(label);
    setCommandOpen(false);

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  return (
    <div className="aurex-app">
      <aside className="side-rail">
        <div className="rail-brand">
          <div className="rail-mark">A</div>

          <div className="rail-brand-copy">
            <strong>AUREX</strong>
            <span>INTELLIGENCE ENGINE</span>
          </div>
        </div>

        <div className="rail-section-label">COMMAND</div>

        <nav className="rail-nav" aria-label="Aurex navigation">
          {navigation.map((item) => (
            <button
              key={item.label}
              className={`rail-item ${
                activePage === item.label ? "active" : ""
              }`}
              onClick={() => handleNavigation(item.label)}
              title={item.label}
            >
              <span className="rail-icon">{item.icon}</span>
              <span className="rail-label">{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="rail-bottom">
          <div className="system-health">
            <span className="online-dot" />

            <div>
              <strong>SYSTEM ONLINE</strong>
              <span>Portfolio workspace ready</span>
            </div>
          </div>

          <div className="rail-user">
            <div className="user-avatar">SA</div>

            <div className="rail-user-copy">
              <strong>System Admin</strong>
              <span>Administrator</span>
            </div>
          </div>
        </div>
      </aside>

      <main className="main-canvas">
        <header className="command-bar">
          <div className="command-brand">
            <span>AUREX</span>
            <i>/</i>
            <strong>{activePage}</strong>
          </div>

          <button
            className="command-search"
            onClick={() => setCommandOpen(true)}
          >
            <span className="search-icon">⌕</span>
            <span>Search projects, intelligence or actions</span>
            <kbd>Ctrl K</kbd>
          </button>

          <div className="command-actions">
            <span className="live-state">
              <i /> LIVE
            </span>

            <button className="command-icon" aria-label="Notifications">
              △
            </button>

            <div className="command-profile">
              <div className="user-avatar small">SA</div>
              <span>ADMIN</span>
            </div>
          </div>
        </header>

        <div className="page-content">
          {activePage === "Portfolio" ? (
            <>
              <section className="page-intro">
                <div>
                  <div className="eyebrow">
                    PORTFOLIO INTELLIGENCE / LIVE SCOPE
                  </div>

                  <h1>See what is happening across the portfolio.</h1>

                  <p>
                    A dense operational view of project health, financial
                    exposure, schedule position and the signals currently
                    requiring attention.
                  </p>
                </div>

                <div className="scope-readout">
                  <span>ANALYZED SCOPE</span>
                  <strong>{projects.length} PROJECTS</strong>
                  <small>
                    Mock portfolio snapshot · backend-ready adapter
                  </small>
                </div>
              </section>

              <section
                className="metric-strip"
                aria-label="Portfolio metrics"
              >
                <div className="metric-block primary">
                  <span>ANALYZED PROJECTS</span>
                  <strong>{projects.length}</strong>
                  <small>Current portfolio snapshot</small>
                </div>

                <div className="metric-block">
                  <span>TOTAL EXPOSURE</span>
                  <strong>
                    ₹{portfolioRisk.totalBudget.toFixed(1)} Cr
                  </strong>
                  <small>Approved / analyzed budget</small>
                </div>

                <div className="metric-block">
                  <span>HIGH-RISK PROJECTS</span>
                  <strong>{portfolioRisk.highRiskCount}</strong>
                  <small>Immediate attention</small>
                </div>

                <div className="metric-block">
                  <span>REQUIRING ACTION</span>
                  <strong>{portfolioRisk.attentionCount}</strong>
                  <small>Non-low risk signals</small>
                </div>
              </section>

              <section className="workspace-grid">
                <div className="portfolio-workspace">
                  <div className="section-heading">
                    <div>
                      <span className="eyebrow">PROJECT PORTFOLIO</span>
                      <h2>Operational project register</h2>
                    </div>

                    <span className="record-count">
                      {filteredProjects.length} / {projects.length}
                    </span>
                  </div>

                  <div className="table-toolbar">
                    <label className="table-search">
                      <span>⌕</span>

                      <input
                        value={search}
                        onChange={(event) => setSearch(event.target.value)}
                        placeholder="Search project, owner or ID"
                      />
                    </label>

                    <select
                      value={statusFilter}
                      onChange={(event) =>
                        setStatusFilter(event.target.value)
                      }
                    >
                      <option value="All">All status</option>
                      <option value="On Track">On Track</option>
                      <option value="Review">Review</option>
                      <option value="At Risk">At Risk</option>
                    </select>
                  </div>

                  <div className="project-table">
                    <div className="table-head">
                      <span>PROJECT</span>
                      <span>HEALTH</span>
                      <span>PROGRESS</span>
                      <span>FINANCIAL</span>
                      <span>SCHEDULE</span>
                      <span>ACTION</span>
                    </div>

                    {filteredProjects.length ? (
                      filteredProjects.map((project) => (
                        <button
                          className="project-row"
                          key={project.id}
                          onClick={() => setSelectedProject(project)}
                        >
                          <div className="project-cell">
                            <span className="project-id">{project.id}</span>

                            <div>
                              <strong>{project.name}</strong>
                              <small>
                                {project.category} / {project.owner}
                              </small>
                            </div>
                          </div>

                          <div className="health-cell">
                            <span
                              className={`status-marker ${
                                statusClass[project.status]
                              }`}
                            />

                            <div>
                              <strong>{project.status}</strong>

                              <small
                                className={riskClass(
                                  project.risk.overallRisk
                                )}
                              >
                                {project.risk.overallRisk} risk
                              </small>
                            </div>
                          </div>

                          <div className="progress-cell">
                            <div className="progress-value">
                              <strong>{project.progress}%</strong>
                              <span>
                                {project.progress >= 70
                                  ? "ADVANCING"
                                  : "WATCH"}
                              </span>
                            </div>

                            <div className="progress-track">
                              <span
                                style={{
                                  width: `${project.progress}%`,
                                }}
                              />
                            </div>
                          </div>

                          <div className="financial-cell">
                            <strong>{project.spent}</strong>
                            <small>of {project.budget}</small>

                            <em
                              className={riskClass(
                                project.risk.budgetRisk
                              )}
                            >
                              {project.risk.budgetUtilization}% used
                            </em>
                          </div>

                          <div
                            className={`schedule-cell ${project.scheduleDirection}`}
                          >
                            <strong>
                              {project.scheduleDirection === "behind"
                                ? "↓"
                                : "↑"}{" "}
                              {project.scheduleDays}d
                            </strong>

                            <small>
                              {project.scheduleDirection === "behind"
                                ? "BEHIND"
                                : "AHEAD"}
                            </small>
                          </div>

                          <div className="investigate-cell">
                            <span>INVESTIGATE</span>
                            <b>↗</b>
                          </div>
                        </button>
                      ))
                    ) : (
                      <div className="empty-state">
                        No projects match the current query.
                      </div>
                    )}
                  </div>
                </div>

                <aside className="intelligence-column">
                  <div className="intelligence-heading">
                    <div>
                      <span className="eyebrow">AUREX INTELLIGENCE</span>
                      <h2>Portfolio signal</h2>
                    </div>

                    <span className="signal-live">LIVE</span>
                  </div>

                  <div className="score-block">
                    <div className="score-kicker">
                      AUREX INTELLIGENCE SCORE
                    </div>

                    <div className="score-number">
                      {portfolioRisk.portfolioScore}
                      <span>/100</span>
                    </div>

                    <div className="score-state">
                      <span className="score-line" />

                      <strong>
                        {portfolioRisk.portfolioScore >= 85
                          ? "STABLE"
                          : portfolioRisk.portfolioScore >= 70
                            ? "UNDER WATCH"
                            : "ELEVATED RISK"}
                      </strong>
                    </div>

                    <p>
                      Aggregate signal derived from the current project
                      snapshot. Inspect the dimensions below before acting.
                    </p>
                  </div>

                  <div className="signal-list">
                    {[
                      ["SCHEDULE", portfolioRisk.scheduleExposure],
                      ["BUDGET", portfolioRisk.budgetExposure],
                      ["EXECUTION", portfolioRisk.executionExposure],
                    ].map(([label, value]) => (
                      <div className="signal-row" key={label}>
                        <div>
                          <span>{label}</span>
                          <i className={riskClass(value)} />
                        </div>

                        <strong className={riskClass(value)}>
                          {value}
                        </strong>
                      </div>
                    ))}
                  </div>

                  <div className="signal-evidence">
                    <div>
                      <span>SCHEDULE HEALTH</span>
                      <strong>{portfolioRisk.scheduleHealth}%</strong>
                    </div>

                    <div>
                      <span>BUDGET UTILIZATION</span>
                      <strong>{portfolioRisk.budgetUtilization}%</strong>
                    </div>

                    <div>
                      <span>EXECUTION CONFIDENCE</span>
                      <strong>
                        {portfolioRisk.executionConfidence}%
                      </strong>
                    </div>
                  </div>

                  <div className="executive-signal">
                    <span className="eyebrow">KEY INTELLIGENCE</span>

                    <h3>
                      {portfolioIntelligence.priorityProject.name}
                    </h3>

                    <div className="signal-meta">
                      <span>PRIMARY SIGNAL</span>

                      <strong
                        className={riskClass(
                          portfolioIntelligence.primarySignal.value
                        )}
                      >
                        {portfolioIntelligence.primarySignal.name} /{" "}
                        {portfolioIntelligence.primarySignal.value}
                      </strong>
                    </div>

                    <p>
                      {portfolioIntelligence.primarySignal.detail}.
                    </p>

                    <button
                      onClick={() =>
                        setSelectedProject(
                          portfolioIntelligence.priorityProject
                        )
                      }
                    >
                      INVESTIGATE PRIORITY <b>↗</b>
                    </button>
                  </div>
                </aside>
              </section>

              <section className="summary-strip">
                <div>
                  <span>ON SCHEDULE</span>

                  <strong>
                    {portfolioRisk.onScheduleCount}
                    <small> / {projects.length}</small>
                  </strong>

                  <em>projects ahead of schedule</em>
                </div>

                <div>
                  <span>CAPITAL DEPLOYED</span>

                  <strong>
                    ₹{portfolioRisk.totalSpent.toFixed(1)}
                    <small> Cr</small>
                  </strong>

                  <em>
                    {portfolioRisk.budgetUtilization}% of analyzed budget
                  </em>
                </div>

                <div>
                  <span>ACTIVE SIGNALS</span>

                  <strong>
                    {portfolioRisk.attentionCount}
                    <small> projects</small>
                  </strong>

                  <em>requiring review or action</em>
                </div>

                <div>
                  <span>PRIMARY SIGNAL</span>

                  <strong>
                    {portfolioIntelligence.primarySignal.name}
                  </strong>

                  <em
                    className={riskClass(
                      portfolioIntelligence.primarySignal.value
                    )}
                  >
                    {portfolioIntelligence.primarySignal.value} exposure
                  </em>
                </div>
              </section>
            </>
          ) : activePage === "Risk Center" ? (
            <section className="risk-center-page">
              <section className="risk-center-header">
                <div>
                  <div className="eyebrow">
                    RISK CENTER / PORTFOLIO EXPOSURE
                  </div>

                  <h1>Risk Center</h1>

                  <p>
                    Detect where portfolio exposure is concentrated across
                    schedule, budget and execution signals.
                  </p>
                </div>

                <div className="risk-center-state">
                  <span className="signal-live">LIVE SNAPSHOT</span>

                  <strong>
                    {portfolioRisk.highRiskCount} HIGH-RISK PROJECT
                  </strong>

                  <small>
                    {portfolioRisk.attentionCount} projects requiring
                    attention
                  </small>
                </div>
              </section>

              <section className="risk-overview-strip">
                <div className="risk-overview-block critical">
                  <span>HIGH-RISK PROJECTS</span>
                  <strong>{portfolioRisk.highRiskCount}</strong>
                  <small>Immediate portfolio attention</small>
                </div>

                <div className="risk-overview-block">
                  <span>SCHEDULE EXPOSURE</span>

                  <strong
                    className={riskClass(
                      portfolioRisk.scheduleExposure
                    )}
                  >
                    {portfolioRisk.scheduleExposure}
                  </strong>

                  <small>
                    {
                      projectsWithRisk.filter(
                        (project) =>
                          project.risk.scheduleRisk !== "Low"
                      ).length
                    }{" "}
                    affected project(s)
                  </small>
                </div>

                <div className="risk-overview-block">
                  <span>BUDGET EXPOSURE</span>

                  <strong
                    className={riskClass(portfolioRisk.budgetExposure)}
                  >
                    {portfolioRisk.budgetExposure}
                  </strong>

                  <small>
                    {portfolioRisk.budgetUtilization}% analyzed budget
                    used
                  </small>
                </div>

                <div className="risk-overview-block">
                  <span>EXECUTION EXPOSURE</span>

                  <strong
                    className={riskClass(
                      portfolioRisk.executionExposure
                    )}
                  >
                    {portfolioRisk.executionExposure}
                  </strong>

                  <small>
                    {portfolioRisk.executionConfidence}% derived
                    confidence
                  </small>
                </div>
              </section>

              <section className="risk-center-grid">
                <div className="risk-register-panel">
                  <div className="section-heading">
                    <div>
                      <span className="eyebrow">
                        ACTIVE RISK REGISTER
                      </span>

                      <h2>Portfolio exposure by project</h2>
                    </div>

                    <span className="record-count">
                      {
                        projectsWithRisk.filter(
                          (project) =>
                            project.risk.overallRisk !== "Low"
                        ).length
                      }{" "}
                      ACTIVE
                    </span>
                  </div>

                  <div className="risk-table">
                    <div className="risk-table-head">
                      <span>PROJECT</span>
                      <span>OVERALL</span>
                      <span>SCHEDULE</span>
                      <span>BUDGET</span>
                      <span>EXECUTION</span>
                      <span>ACTION</span>
                    </div>

                    {projectsWithRisk
                      .filter(
                        (project) =>
                          project.risk.overallRisk !== "Low"
                      )
                      .sort(
                        (a, b) =>
                          severityValue[b.risk.overallRisk] -
                          severityValue[a.risk.overallRisk]
                      )
                      .map((project) => {
                        const signalEntries = [
                          {
                            name: "Schedule Exposure",
                            value: project.risk.scheduleRisk,
                          },
                          {
                            name: "Budget Exposure",
                            value: project.risk.budgetRisk,
                          },
                          {
                            name: "Execution Risk",
                            value: project.risk.executionRisk,
                          },
                        ];

                        const primarySignal = signalEntries.reduce(
                          (strongest, signal) =>
                            severityValue[signal.value] >
                            severityValue[strongest.value]
                              ? signal
                              : strongest
                        );

                        return (
                          <button
                            className="risk-project-row"
                            key={project.id}
                            onClick={() =>
                              setSelectedProject(project)
                            }
                          >
                            <div className="risk-project-cell">
                              <span className="project-id">
                                {project.id}
                              </span>

                              <div>
                                <strong>{project.name}</strong>

                                <small>
                                  {project.category} /{" "}
                                  {project.owner}
                                </small>

                                <em
                                  className={riskClass(
                                    primarySignal.value
                                  )}
                                >
                                  {primarySignal.name}
                                </em>
                              </div>
                            </div>

                            <div className="risk-value-cell">
                              <strong
                                className={riskClass(
                                  project.risk.overallRisk
                                )}
                              >
                                {project.risk.overallRisk}
                              </strong>

                              <small>
                                {project.priority} priority
                              </small>
                            </div>

                            <div className="risk-dimension-cell">
                              <i
                                className={riskClass(
                                  project.risk.scheduleRisk
                                )}
                              />

                              <strong>
                                {project.risk.scheduleRisk}
                              </strong>

                              <small>
                                {project.scheduleDirection === "behind"
                                  ? `${project.scheduleDays}d behind`
                                  : `${project.scheduleDays}d ahead`}
                              </small>
                            </div>

                            <div className="risk-dimension-cell">
                              <i
                                className={riskClass(
                                  project.risk.budgetRisk
                                )}
                              />

                              <strong>
                                {project.risk.budgetRisk}
                              </strong>

                              <small>
                                {project.risk.budgetUtilization}% used
                              </small>
                            </div>

                            <div className="risk-dimension-cell">
                              <i
                                className={riskClass(
                                  project.risk.executionRisk
                                )}
                              />

                              <strong>
                                {project.risk.executionRisk}
                              </strong>

                              <small>{project.status}</small>
                            </div>

                            <div className="risk-investigate-cell">
                              <span>INVESTIGATE</span>
                              <b>↗</b>
                            </div>
                          </button>
                        );
                      })}
                  </div>
                </div>

                <aside className="risk-landscape-panel">
                  <div className="section-heading">
                    <div>
                      <span className="eyebrow">
                        RISK LANDSCAPE
                      </span>

                      <h2>Signal concentration</h2>
                    </div>
                  </div>

                  <div className="risk-landscape-score">
                    <span>PORTFOLIO INTELLIGENCE</span>

                    <strong>
                      {portfolioRisk.portfolioScore}
                      <small>/100</small>
                    </strong>

                    <div className="risk-score-bar">
                      <span
                        style={{
                          width: `${portfolioRisk.portfolioScore}%`,
                        }}
                      />
                    </div>

                    <p>
                      Current aggregate signal across the analyzed
                      project snapshot.
                    </p>
                  </div>

                  <div className="risk-landscape-list">
                    {[
                      [
                        "SCHEDULE",
                        portfolioRisk.scheduleExposure,
                        projectsWithRisk.filter(
                          (project) =>
                            project.risk.scheduleRisk !== "Low"
                        ).length,
                      ],
                      [
                        "BUDGET",
                        portfolioRisk.budgetExposure,
                        projectsWithRisk.filter(
                          (project) =>
                            project.risk.budgetRisk !== "Low"
                        ).length,
                      ],
                      [
                        "EXECUTION",
                        portfolioRisk.executionExposure,
                        projectsWithRisk.filter(
                          (project) =>
                            project.risk.executionRisk !== "Low"
                        ).length,
                      ],
                    ].map(([label, value, count]) => (
                      <div
                        className="risk-landscape-row"
                        key={label}
                      >
                        <div>
                          <span>{label}</span>

                          <strong className={riskClass(value)}>
                            {value}
                          </strong>
                        </div>

                        <div className="risk-landscape-track">
                          <span
                            className={riskClass(value)}
                            style={{
                              width:
                                value === "High"
                                  ? "100%"
                                  : value === "Moderate"
                                    ? "66%"
                                    : "32%",
                            }}
                          />
                        </div>

                        <small>{count} affected</small>
                      </div>
                    ))}
                  </div>

                  <div className="risk-center-focus">
                    <span className="eyebrow">PRIMARY FOCUS</span>

                    <strong>
                      {portfolioIntelligence.priorityProject.name}
                    </strong>

                    <small>
                      {portfolioIntelligence.primarySignal.name} /{" "}
                      {portfolioIntelligence.primarySignal.value}
                    </small>

                    <button
                      onClick={() =>
                        setSelectedProject(
                          portfolioIntelligence.priorityProject
                        )
                      }
                    >
                      OPEN INVESTIGATION <b>↗</b>
                    </button>
                  </div>
                </aside>
              </section>
            </section>
          ) : activePage === "Projects" ? (
            <ModulePage
              eyebrow="PROJECTS / OPERATIONAL REGISTER"
              title="Projects"
              description="Search, inspect and investigate the current project snapshot from one operational register."
              metrics={[
                [
                  "PROJECTS",
                  projects.length,
                  "Analyzed project snapshot",
                ],
                [
                  "ON TRACK",
                  projectsWithRisk.filter(
                    (p) => p.status === "On Track"
                  ).length,
                  "Currently on track",
                ],
                [
                  "REVIEW",
                  projectsWithRisk.filter(
                    (p) => p.status === "Review"
                  ).length,
                  "Requires review",
                ],
                [
                  "AT RISK",
                  projectsWithRisk.filter(
                    (p) => p.status === "At Risk"
                  ).length,
                  "Requires action",
                ],
              ]}
              rows={projectsWithRisk}
              onProject={setSelectedProject}
              actionLabel="OPEN PROJECT"
            />
          ) : activePage === "Warnings" ? (
            <section className="warnings-page">
              <section className="warnings-header">
                <div>
                  <div className="eyebrow">
                    EARLY WARNING / SIGNAL REGISTER
                  </div>

                  <h1>Warnings</h1>

                  <p>
                    Active non-low signals requiring attention across
                    the analyzed portfolio.
                  </p>
                </div>

                <div className="warnings-state">
                  <span className="signal-live">LIVE SNAPSHOT</span>

                  <strong>
                    {warningRows.length} ACTIVE SIGNALS
                  </strong>

                  <small>
                    {highWarningCount} high-severity signal
                    {highWarningCount === 1 ? "" : "s"}
                  </small>
                </div>
              </section>

              <section className="warning-overview-strip">
                <div className="warning-overview-block critical">
                  <span>ACTIVE WARNINGS</span>
                  <strong>{warningRows.length}</strong>
                  <small>Non-low project signals</small>
                </div>

                <div className="warning-overview-block">
                  <span>HIGH</span>

                  <strong className="warning-high-value">
                    {highWarningCount}
                  </strong>

                  <small>High-severity signals</small>
                </div>

                <div className="warning-overview-block">
                  <span>SCHEDULE</span>
                  <strong>{scheduleWarningCount}</strong>
                  <small>Schedule signals detected</small>
                </div>

                <div className="warning-overview-block">
                  <span>BUDGET</span>
                  <strong>{budgetWarningCount}</strong>
                  <small>Budget signals detected</small>
                </div>
              </section>

              <section className="warning-register-panel">
                <div className="section-heading">
                  <div>
                    <span className="eyebrow">
                      WARNING REGISTER
                    </span>

                    <h2>Signals requiring review</h2>
                  </div>

                  <span className="record-count">
                    {warningRows.length} ACTIVE
                  </span>
                </div>

                <div className="warning-table">
                  <div className="warning-table-head">
                    <span>PROJECT</span>
                    <span>SIGNAL</span>
                    <span>SEVERITY</span>
                    <span>IMPACT</span>
                    <span>CURRENT STATE</span>
                    <span>ACTION</span>
                  </div>

                  {[...warningRows]
                    .sort(
                      (a, b) =>
                        severityValue[b.severity] -
                        severityValue[a.severity]
                    )
                    .map((warning) => (
                      <button
                        className="warning-row"
                        key={warning.id}
                        onClick={() =>
                          setSelectedProject(warning.project)
                        }
                      >
                        <div className="warning-project-cell">
                          <span className="project-id">
                            {warning.project.id}
                          </span>

                          <div>
                            <strong>{warning.project.name}</strong>

                            <small>
                              {warning.project.category} /{" "}
                              {warning.project.owner}
                            </small>
                          </div>
                        </div>

                        <div className="warning-signal-cell">
                          <span className="warning-signal-mark">
                            △
                          </span>

                          <div>
                            <strong>{warning.signal}</strong>
                            <small>{warning.detail}</small>
                          </div>
                        </div>

                        <div className="warning-severity-cell">
                          <i
                            className={riskClass(
                              warning.severity
                            )}
                          />

                          <strong
                            className={riskClass(
                              warning.severity
                            )}
                          >
                            {warning.severity}
                          </strong>
                        </div>

                        <div className="warning-impact-cell">
                          <strong>{warning.impact}</strong>
                        </div>

                        <div className="warning-state-cell">
                          <span>{warning.state}</span>
                        </div>

                        <div className="warning-action-cell">
                          <span>INVESTIGATE</span>
                          <b>↗</b>
                        </div>
                      </button>
                    ))}
                </div>
              </section>

              <section className="warning-focus-panel">
                <div>
                  <span className="eyebrow">
                    INVESTIGATION HANDOFF
                  </span>

                  <h2>
                    Warnings connect directly to project investigation.
                  </h2>

                  <p>
                    Select any signal to open the existing project
                    investigation workspace. Backend evidence and
                    recommendations remain pending until connected.
                  </p>
                </div>

                <div className="warning-focus-meta">
                  <span>PROJECT SNAPSHOT</span>
                  <strong>AVAILABLE</strong>

                  <span>BACKEND EVIDENCE</span>
                  <strong className="pending">PENDING</strong>
                </div>
              </section>
            </section>
          ) : activePage === "Investigation" ? (
            <ModulePage
              eyebrow="INVESTIGATION / TRACEABLE WORKSPACE"
              title="Investigation"
              description="Start from a project signal and move into the evidence chain. Backend evidence and recommendations remain pending until supplied by the intelligence service."
              metrics={[
                [
                  "PROJECTS",
                  projects.length,
                  "Available for investigation",
                ],
                [
                  "SIGNALS",
                  portfolioRisk.attentionCount,
                  "Non-low signals",
                ],
                ["EVIDENCE", "PENDING", "Backend evidence state"],
                [
                  "ACTIONS",
                  "PENDING",
                  "Backend recommendation state",
                ],
              ]}
              rows={projectsWithRisk}
              onProject={setSelectedProject}
              actionLabel="INVESTIGATE"
            />
          ) : activePage === "Predictions" ? (
            <PendingPage
              eyebrow="PREDICTIONS / FORECASTING"
              title="Predictions"
              description="Prediction outputs are not connected to the current frontend data contract yet. The workspace is ready for backend forecast values."
            />
          ) : activePage === "Scenarios" ? (
            <PendingPage
              eyebrow="SCENARIO SIMULATION / WHAT-IF"
              title="Scenarios"
              description="Scenario simulation controls are reserved for the intelligence integration layer. No simulated values are fabricated in this frontend."
            />
          ) : (
            <PendingPage
              eyebrow="REPORTS / PROJECT DOSSIER"
              title="Reports"
              description="Report generation is ready as an application surface. Backend report data and export contracts can be connected here."
            />
          )}
        </div>
      </main>

      {selectedProject && (
        <div
          className="drawer-backdrop"
          onClick={() => setSelectedProject(null)}
        >
          <section
            className="project-drawer investigation-drawer"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="drawer-topline">
              <div>
                <span className="eyebrow">
                  AUREX / PROJECT INVESTIGATION
                </span>

                <span className="drawer-scope">
                  ANALYZED PROJECT
                </span>
              </div>

              <button
                className="close-button"
                onClick={() => setSelectedProject(null)}
                aria-label="Close project investigation"
              >
                ×
              </button>
            </div>

            <div className="investigation-header">
              <div className="investigation-id">
                {selectedProject.id}
              </div>

              <h2>{selectedProject.name}</h2>

              <p>
                {selectedProject.category} /{" "}
                {selectedProject.owner}
              </p>
            </div>

            <div className="investigation-health">
              <div>
                <span>PROJECT HEALTH</span>

                <strong
                  className={riskClass(
                    selectedProject.risk.overallRisk
                  )}
                >
                  {selectedProject.status}
                </strong>
              </div>

              <div>
                <span>OVERALL RISK</span>

                <strong
                  className={riskClass(
                    selectedProject.risk.overallRisk
                  )}
                >
                  {selectedProject.risk.overallRisk}
                </strong>
              </div>

              <div>
                <span>PRIORITY</span>
                <strong>{selectedProject.priority}</strong>
              </div>
            </div>

            <section className="investigation-section intelligence-section">
              <div className="section-heading">
                <div>
                  <span className="eyebrow">
                    AUREX INTELLIGENCE
                  </span>

                  <h3>Primary project signal</h3>
                </div>

                <span className="signal-live">LIVE</span>
              </div>

              <div className="primary-signal">
                <div className="primary-signal-marker" />

                <div>
                  <span>DOMINANT RISK DIMENSION</span>

                  <strong>
                    {[
                      [
                        "Schedule Exposure",
                        selectedProject.risk.scheduleRisk,
                      ],
                      [
                        "Budget Exposure",
                        selectedProject.risk.budgetRisk,
                      ],
                      [
                        "Execution Risk",
                        selectedProject.risk.executionRisk,
                      ],
                    ].sort(
                      (a, b) =>
                        severityValue[b[1]] -
                        severityValue[a[1]]
                    )[0][0]}
                  </strong>

                  <small>
                    {
                      [
                        selectedProject.risk.scheduleRisk,
                        selectedProject.risk.budgetRisk,
                        selectedProject.risk.executionRisk,
                      ].sort(
                        (a, b) =>
                          severityValue[b] -
                          severityValue[a]
                      )[0]
                    }{" "}
                    exposure
                  </small>
                </div>
              </div>
            </section>

            <section className="investigation-section">
              <div className="section-heading">
                <div>
                  <span className="eyebrow">PROJECT STATE</span>
                  <h3>Operational snapshot</h3>
                </div>
              </div>

              <div className="investigation-metrics">
                <div className="investigation-metric">
                  <span>PHYSICAL PROGRESS</span>

                  <strong>{selectedProject.progress}%</strong>

                  <div className="investigation-progress">
                    <span
                      style={{
                        width: `${selectedProject.progress}%`,
                      }}
                    />
                  </div>
                </div>

                <div className="investigation-metric">
                  <span>FINANCIAL</span>

                  <strong>{selectedProject.spent}</strong>

                  <small>of {selectedProject.budget}</small>

                  <em
                    className={riskClass(
                      selectedProject.risk.budgetRisk
                    )}
                  >
                    {selectedProject.risk.budgetUtilization}% used
                  </em>
                </div>

                <div className="investigation-metric">
                  <span>SCHEDULE</span>

                  <strong
                    className={
                      selectedProject.scheduleDirection === "behind"
                        ? "negative"
                        : "positive"
                    }
                  >
                    {selectedProject.scheduleDirection === "behind"
                      ? "↓"
                      : "↑"}{" "}
                    {selectedProject.scheduleDays}d
                  </strong>

                  <small>
                    {selectedProject.scheduleDirection === "behind"
                      ? "behind schedule"
                      : "ahead of schedule"}
                  </small>
                </div>
              </div>
            </section>

            <section className="investigation-section">
              <div className="section-heading">
                <div>
                  <span className="eyebrow">RISK SIGNALS</span>
                  <h3>Supporting dimensions</h3>
                </div>
              </div>

              <div className="risk-signal-list">
                {[
                  [
                    "01",
                    "Schedule Risk",
                    selectedProject.risk.scheduleRisk,
                    "Derived from current schedule position",
                  ],
                  [
                    "02",
                    "Budget Risk",
                    selectedProject.risk.budgetRisk,
                    "Based on current budget utilization",
                  ],
                  [
                    "03",
                    "Execution Risk",
                    selectedProject.risk.executionRisk,
                    "Based on current project status",
                  ],
                ].map(([index, label, value, detail]) => (
                  <div
                    className="investigation-signal-row"
                    key={label}
                  >
                    <div>
                      <span>{index}</span>
                      <strong>{label}</strong>
                      <small>{detail}</small>
                    </div>

                    <strong className={riskClass(value)}>
                      {value}
                    </strong>
                  </div>
                ))}
              </div>
            </section>

            <section className="investigation-section evidence-section">
              <div className="section-heading">
                <div>
                  <span className="eyebrow">
                    INVESTIGATION ENGINE
                  </span>

                  <h3>Evidence status</h3>
                </div>

                <span className="pending-label">PENDING</span>
              </div>

              <div className="evidence-chain">
                {[
                  [
                    "01",
                    "PROJECT",
                    "Current project snapshot available",
                    true,
                  ],
                  [
                    "02",
                    "SIGNAL",
                    "Portfolio risk dimensions available",
                    true,
                  ],
                  [
                    "03",
                    "EVIDENCE",
                    "Backend investigation data pending",
                    false,
                  ],
                  [
                    "04",
                    "ACTION",
                    "Recommendation unavailable",
                    false,
                  ],
                ].map(([index, label, detail, active], position) => (
                  <div className="evidence-group" key={label}>
                    <div
                      className={`evidence-node ${
                        active ? "active" : "pending"
                      }`}
                    >
                      <span className="evidence-node-index">
                        {index}
                      </span>

                      <div>
                        <strong>{label}</strong>
                        <small>{detail}</small>
                      </div>
                    </div>

                    {position < 3 && (
                      <div className="evidence-line" />
                    )}
                  </div>
                ))}
              </div>
            </section>

            <div className="investigation-footer">
              <span>
                AUREX / BACKEND-READY INVESTIGATION WORKSPACE
              </span>

              <span>{selectedProject.id}</span>
            </div>
          </section>
        </div>
      )}

      {commandOpen && (
        <div
          className="command-backdrop"
          onClick={() => setCommandOpen(false)}
        >
          <section
            className="command-palette"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="palette-search">
              <span>⌕</span>

              <input
                autoFocus
                placeholder="Search projects, routes or actions"
              />

              <kbd>ESC</kbd>
            </div>

            <div className="palette-group">
              <span>PROJECTS</span>

              {projects.slice(0, 4).map((project) => (
                <button
                  key={project.id}
                  onClick={() => {
                    setSelectedProject(
                      projectsWithRisk.find(
                        (item) => item.id === project.id
                      )
                    );

                    setCommandOpen(false);
                  }}
                >
                  <b>{project.id}</b>
                  <strong>{project.name}</strong>
                  <small>Open project detail ↗</small>
                </button>
              ))}
            </div>

            <div className="palette-group routes">
              <span>COMMANDS</span>

              {navigation.slice(0, 4).map((item) => (
                <button
                  key={item.label}
                  onClick={() =>
                    handleNavigation(item.label)
                  }
                >
                  <b>{item.icon}</b>
                  <strong>{item.label}</strong>
                  <small>
                    {[
                      "Portfolio",
                      "Projects",
                      "Risk Center",
                      "Warnings",
                      "Investigation",
                    ].includes(item.label)
                      ? "Open"
                      : "Workspace"}
                  </small>
                </button>
              ))}
            </div>
          </section>
        </div>
      )}
    </div>
  );
}

export default App;