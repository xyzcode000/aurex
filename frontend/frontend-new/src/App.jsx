import { useMemo, useState } from "react";
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
    schedule: "12 days ahead",
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
    schedule: "4 days behind",
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
    schedule: "8 days ahead",
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
    schedule: "18 days behind",
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
    schedule: "6 days ahead",
  },
];

const statusClass = {
  "On Track": "success",
  Review: "warning",
  "At Risk": "danger",
};

function App() {
  const [activePage, setActivePage] = useState("Overview");
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");
  const [selectedProject, setSelectedProject] = useState(null);

  const filteredProjects = useMemo(() => {
    return projects.filter((project) => {
      const matchesSearch =
        project.name.toLowerCase().includes(search.toLowerCase()) ||
        project.category.toLowerCase().includes(search.toLowerCase());

      const matchesStatus =
        statusFilter === "All" || project.status === statusFilter;

      return matchesSearch && matchesStatus;
    });
  }, [search, statusFilter]);

  return (
    <div className="app">

      {/* SIDEBAR */}
      <aside className="sidebar">

        <div className="brand">
          <div className="brand-symbol">
            <span>A</span>
          </div>

          <div>
            <div className="brand-name">AUREX</div>
            <div className="brand-subtitle">
              PROJECT INTELLIGENCE
            </div>
          </div>
        </div>

        <div className="workspace-label">
          WORKSPACE
        </div>

        <nav className="navigation">

          <button
            className={`nav-item ${
              activePage === "Overview" ? "active" : ""
            }`}
            onClick={() => setActivePage("Overview")}
          >
            <span className="nav-icon">⌂</span>
            <span>Overview</span>
          </button>

          <button
            className={`nav-item ${
              activePage === "Projects" ? "active" : ""
            }`}
            onClick={() => setActivePage("Projects")}
          >
            <span className="nav-icon">▦</span>
            <span>Projects</span>
            <span className="nav-count">24</span>
          </button>

          <button
            className={`nav-item ${
              activePage === "Portfolio" ? "active" : ""
            }`}
            onClick={() => setActivePage("Portfolio")}
          >
            <span className="nav-icon">◫</span>
            <span>Portfolio</span>
          </button>

        </nav>

        <div className="workspace-label system-label">
          SYSTEM
        </div>

        <nav className="navigation">

          <button className="nav-item">
            <span className="nav-icon">◉</span>
            <span>Activity</span>
          </button>

          <button className="nav-item">
            <span className="nav-icon">⚙</span>
            <span>Settings</span>
          </button>

        </nav>

        <div className="sidebar-bottom">

          <div className="system-status">
            <span className="status-light"></span>

            <div>
              <strong>System operational</strong>
              <span>All services connected</span>
            </div>
          </div>

          <div className="profile">
            <div className="profile-avatar">A</div>

            <div>
              <strong>Administrator</strong>
              <span>Portfolio Officer</span>
            </div>

            <span className="profile-more">•••</span>
          </div>

        </div>
      </aside>

      {/* MAIN */}
      <main className="main">

        {/* TOP BAR */}
        <header className="topbar">

          <div className="breadcrumb">
            <span>AUREX</span>
            <b>/</b>
            <span className="current">
              {activePage}
            </span>
          </div>

          <div className="top-actions">

            <div className="live">
              <span></span>
              LIVE
            </div>

            <button className="icon-button">
              ◌
            </button>

            <button className="icon-button notification">
              ◇
              <i></i>
            </button>

            <div className="top-avatar">
              A
            </div>

          </div>

        </header>

        {/* CONTENT */}
        <div className="content">

          {/* HERO */}
          <section className="hero">

            <div className="hero-left">

              <div className="eyebrow">
                PORTFOLIO COMMAND CENTER
              </div>

              <h1>
                See the bigger
                <br />
                <span>picture.</span>
              </h1>

              <p>
                A centralized view of project health, financial
                performance, progress and schedule intelligence.
              </p>

            </div>

            <div className="hero-right">

              <div className="date-label">
                PORTFOLIO STATUS
              </div>

              <div className="date-value">
                September 13, 2026
              </div>

              <div className="updated">
                Last synchronized just now
              </div>

            </div>

          </section>

          {/* KPI CARDS */}
          <section className="kpi-grid">

            <div className="kpi-card">

              <div className="kpi-top">
                <span>Total Projects</span>
                <span className="kpi-symbol">↗</span>
              </div>

              <div className="kpi-value">
                24
              </div>

              <div className="kpi-bottom">
                <span className="positive">+3</span>
                <span>from last quarter</span>
              </div>

            </div>

            <div className="kpi-card">

              <div className="kpi-top">
                <span>On Track</span>
                <span className="kpi-symbol">✓</span>
              </div>

              <div className="kpi-value">
                18
              </div>

              <div className="kpi-bottom">
                <span className="positive">75%</span>
                <span>portfolio coverage</span>
              </div>

            </div>

            <div className="kpi-card">

              <div className="kpi-top">
                <span>Needs Attention</span>
                <span className="kpi-symbol warning-symbol">!</span>
              </div>

              <div className="kpi-value warning-number">
                04
              </div>

              <div className="kpi-bottom">
                <span className="warning-text">2 critical</span>
                <span>requiring review</span>
              </div>

            </div>

            <div className="kpi-card">

              <div className="kpi-top">
                <span>Portfolio Health</span>
                <span className="kpi-symbol">◈</span>
              </div>

              <div className="health-row">
                <div className="kpi-value">
                  87<span className="percentage">%</span>
                </div>

                <div className="health-ring">
                  <div>
                    87
                  </div>
                </div>
              </div>

              <div className="kpi-bottom">
                <span className="positive">+4.2%</span>
                <span>vs previous period</span>
              </div>

            </div>

          </section>

          {/* MAIN GRID */}
          <section className="dashboard-grid">

            {/* PROJECTS */}
            <div className="panel projects-panel">

              <div className="panel-header">

                <div>
                  <div className="panel-label">
                    ACTIVE PORTFOLIO
                  </div>

                  <h2>
                    Projects
                  </h2>
                </div>

                <button className="view-all">
                  View all →
                </button>

              </div>

              {/* FILTER BAR */}
              <div className="filter-bar">

                <div className="search-box">
                  <span>⌕</span>

                  <input
                    type="text"
                    placeholder="Search projects..."
                    value={search}
                    onChange={(e) =>
                      setSearch(e.target.value)
                    }
                  />
                </div>

                <select
                  value={statusFilter}
                  onChange={(e) =>
                    setStatusFilter(e.target.value)
                  }
                >
                  <option value="All">
                    All status
                  </option>

                  <option value="On Track">
                    On Track
                  </option>

                  <option value="Review">
                    Review
                  </option>

                  <option value="At Risk">
                    At Risk
                  </option>
                </select>

              </div>

              {/* TABLE */}
              <div className="project-table">

                <div className="table-head">
                  <span>PROJECT</span>
                  <span>STATUS</span>
                  <span>PROGRESS</span>
                  <span>PRIORITY</span>
                </div>

                {filteredProjects.map((project) => (

                  <button
                    className="project-row"
                    key={project.id}
                    onClick={() =>
                      setSelectedProject(project)
                    }
                  >

                    <div className="project-name-cell">

                      <div className="project-number">
                        {project.id.replace("PRJ-", "")}
                      </div>

                      <div>
                        <strong>
                          {project.name}
                        </strong>

                        <span>
                          {project.category}
                        </span>
                      </div>

                    </div>

                    <div>
                      <span
                        className={`status-pill ${
                          statusClass[project.status]
                        }`}
                      >
                        <i></i>
                        {project.status}
                      </span>
                    </div>

                    <div className="progress-cell">

                      <div className="progress-track">
                        <span
                          style={{
                            width: `${project.progress}%`,
                          }}
                        />
                      </div>

                      <strong>
                        {project.progress}%
                      </strong>

                    </div>

                    <div>
                      <span
                        className={`priority ${
                          project.priority.toLowerCase()
                        }`}
                      >
                        {project.priority}
                      </span>
                    </div>

                  </button>

                ))}

                {filteredProjects.length === 0 && (
                  <div className="empty-state">
                    No projects found.
                  </div>
                )}

              </div>

            </div>

            {/* INTELLIGENCE */}
            <div className="panel intelligence-panel">

              <div className="panel-header">

                <div>
                  <div className="panel-label">
                    PORTFOLIO SIGNAL
                  </div>

                  <h2>
                    Intelligence
                  </h2>
                </div>

                <div className="signal-badge">
                  ● LIVE
                </div>

              </div>

              <div className="health-score">

                <div className="score">
                  87
                  <span>/100</span>
                </div>

                <div className="score-copy">
                  <strong>
                    Healthy portfolio
                  </strong>

                  <p>
                    Overall project performance
                    remains within expected
                    thresholds.
                  </p>
                </div>

              </div>

              <div className="health-line">
                <span></span>
              </div>

              <div className="signal-stats">

                <div>
                  <span>Financial health</span>
                  <strong>Good</strong>
                </div>

                <div>
                  <span>Schedule health</span>
                  <strong>Stable</strong>
                </div>

                <div>
                  <span>Risk exposure</span>
                  <strong className="moderate">
                    Moderate
                  </strong>
                </div>

              </div>

              <div className="insight-box">

                <div className="insight-icon">
                  ✦
                </div>

                <div>
                  <span className="insight-label">
                    SYSTEM INSIGHT
                  </span>

                  <p>
                    3 projects are trending ahead
                    of their current schedule.
                  </p>
                </div>

              </div>

            </div>

          </section>

          {/* BOTTOM STRIP */}
          <section className="bottom-grid">

            <div className="mini-panel">

              <div className="mini-icon">
                ₹
              </div>

              <div>
                <span>Total portfolio value</span>
                <strong>₹167.4 Cr</strong>
              </div>

              <span className="mini-arrow">
                →
              </span>

            </div>

            <div className="mini-panel">

              <div className="mini-icon">
                ◷
              </div>

              <div>
                <span>Schedule variance</span>
                <strong>
                  <em>+6.4 days</em>
                </strong>
              </div>

              <span className="mini-arrow">
                →
              </span>

            </div>

            <div className="mini-panel">

              <div className="mini-icon">
                ⚠
              </div>

              <div>
                <span>Critical attention</span>
                <strong>2 projects</strong>
              </div>

              <span className="mini-arrow">
                →
              </span>

            </div>

          </section>

        </div>
      </main>

      {/* PROJECT DETAIL MODAL */}
      {selectedProject && (
        <div
          className="modal-overlay"
          onClick={() => setSelectedProject(null)}
        >

          <div
            className="project-modal"
            onClick={(e) => e.stopPropagation()}
          >

            <button
              className="modal-close"
              onClick={() => setSelectedProject(null)}
            >
              ×
            </button>

            <div className="modal-label">
              PROJECT DETAILS
            </div>

            <h2>
              {selectedProject.name}
            </h2>

            <p className="modal-category">
              {selectedProject.category}
            </p>

            <div className="modal-status">
              <span
                className={`status-pill ${
                  statusClass[selectedProject.status]
                }`}
              >
                <i></i>
                {selectedProject.status}
              </span>

              <span
                className={`priority ${
                  selectedProject.priority.toLowerCase()
                }`}
              >
                {selectedProject.priority}
              </span>
            </div>

            <div className="modal-metrics">

              <div>
                <span>Progress</span>
                <strong>
                  {selectedProject.progress}%
                </strong>
              </div>

              <div>
                <span>Budget</span>
                <strong>
                  {selectedProject.budget}
                </strong>
              </div>

              <div>
                <span>Spent</span>
                <strong>
                  {selectedProject.spent}
                </strong>
              </div>

              <div>
                <span>Schedule</span>
                <strong>
                  {selectedProject.schedule}
                </strong>
              </div>

            </div>

            <div className="modal-progress">

              <div>
                <span>PROJECT COMPLETION</span>
                <strong>
                  {selectedProject.progress}%
                </strong>
              </div>

              <div className="modal-progress-track">
                <span
                  style={{
                    width: `${selectedProject.progress}%`,
                  }}
                />
              </div>

            </div>

          </div>

        </div>
      )}

    </div>
  );
}

export default App;