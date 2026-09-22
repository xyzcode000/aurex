import { Link } from "react-router-dom";
import { projectsData } from "../mocks/projectsData";

function ProjectList() {
  const savedProjects = JSON.parse(
    localStorage.getItem("aurex_projects") || "[]"
  );

  const defaultProjects = projectsData.map((project) => ({
    id: project.project_id,
    name: project.project_name,
    description: project.description,
    status: project.status,
    progress: project.progress,
  }));

  const createdProjects = savedProjects.map(
    (project: any, index: number) => ({
      id:
        project.project_id ||
        `AUREX-${String(index + 5).padStart(3, "0")}`,

      name: project.project_name,

      description:
        project.description ||
        "New project created through Aurex Project Intelligence.",

      status: project.status || "Monitoring",

      progress: project.progress || 0,
    })
  );

  const allProjects = [...defaultProjects, ...createdProjects];

  const projects = allProjects.filter(
    (project, index, array) =>
      index ===
      array.findIndex(
        (item) =>
          item.name.toLowerCase() === project.name.toLowerCase()
      )
  );

  const getStatusClass = (status: string) => {
    if (status === "At Risk") return "risk";
    if (status === "Delayed") return "delayed";
    if (status === "On Track") return "success";
    return "monitoring";
  };

  return (
    <div className="projects-page">
      <div className="projects-container">

        <div className="projects-header">
          <div>
            <p className="eyebrow">
              AUREX PROJECT INTELLIGENCE
            </p>

            <h1>My Projects</h1>

            <p className="subtitle">
              Manage your projects and monitor their current intelligence.
            </p>
          </div>

          <Link
            to="/create-project"
            className="create-button"
          >
            + Create New Project
          </Link>
        </div>

        <div className="summary-bar">
          <div>
            <span className="summary-number">
              {projects.length}
            </span>

            <span className="summary-label">
              Active Projects
            </span>
          </div>

          <Link
            to="/risk-center"
            className="summary-link"
          >
            Open Risk Center →
          </Link>
        </div>

        <div className="project-grid">

          {projects.map((project) => (
            <div
              className="project-card"
              key={project.id}
            >

              <div className="card-top">

                <span className="project-id">
                  {project.id}
                </span>

                <span
                  className={`status-badge ${getStatusClass(
                    project.status
                  )}`}
                >
                  {project.status}
                </span>

              </div>

              <h2>
                {project.name}
              </h2>

              <p className="project-description">
                {project.description}
              </p>

              <div className="progress-section">

                <div className="progress-heading">

                  <span>
                    Project Progress
                  </span>

                  <strong>
                    {project.progress}%
                  </strong>

                </div>

                <div className="progress-track">

                  <div
                    className="progress-fill"
                    style={{
                      width: `${project.progress}%`,
                    }}
                  />

                </div>

              </div>

              <div className="card-footer">

                <span>
                  Project intelligence available
                </span>

                <Link
  to={`/project-detail?project=${project.id}`}
  className="details-button"
>
  View Details →
</Link>

              </div>

            </div>
          ))}

        </div>

      </div>

      <style>{`

        .projects-page {
          min-height: 100vh;
          box-sizing: border-box;
          padding: 42px;
          color: #f5f7ff;

          background:
            radial-gradient(
              circle at top right,
              rgba(91, 76, 255, 0.16),
              transparent 34%
            ),
            radial-gradient(
              circle at bottom left,
              rgba(0, 212, 255, 0.07),
              transparent 30%
            ),
            #070b17;

          font-family: Inter, system-ui, sans-serif;
        }

        .projects-container {
          max-width: 1200px;
          margin: 0 auto;
        }

        .projects-header {
          display: flex;
          align-items: flex-end;
          justify-content: space-between;
          gap: 25px;
          margin-bottom: 30px;
        }

        .eyebrow {
          margin: 0 0 8px;
          color: #8d9cff;
          font-size: 11px;
          font-weight: 800;
          letter-spacing: 2px;
        }

        .projects-header h1 {
          margin: 0;
          font-size: 34px;
          font-weight: 800;
          letter-spacing: -1px;
        }

        .subtitle {
          margin: 9px 0 0;
          color: #8f9bb5;
          font-size: 14px;
        }

        .create-button {
          padding: 12px 18px;
          border: 1px solid rgba(120, 130, 255, 0.35);
          border-radius: 11px;

          background: rgba(91, 76, 255, 0.14);

          color: #c5caff;
          text-decoration: none;

          font-size: 12px;
          font-weight: 800;

          transition: 0.2s ease;
          white-space: nowrap;
        }

        .create-button:hover {
          background: rgba(91, 76, 255, 0.24);
          border-color: rgba(120, 130, 255, 0.65);
          transform: translateY(-2px);
        }

        .summary-bar {
          display: flex;
          align-items: center;
          justify-content: space-between;

          padding: 18px 22px;
          margin-bottom: 22px;

          border: 1px solid rgba(255,255,255,0.07);
          border-radius: 16px;

          background: rgba(14, 19, 35, 0.72);
        }

        .summary-number {
          margin-right: 10px;
          color: #aab2ff;
          font-size: 20px;
          font-weight: 800;
        }

        .summary-label {
          color: #818ca5;
          font-size: 12px;
        }

        .summary-link {
          color: #9ca7ff;
          text-decoration: none;
          font-size: 12px;
          font-weight: 700;
        }

        .project-grid {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 18px;
        }

        .project-card {
          padding: 23px;

          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 20px;

          background: rgba(14, 19, 35, 0.78);

          backdrop-filter: blur(15px);

          box-shadow:
            0 18px 50px rgba(0,0,0,0.2);

          transition: 0.25s ease;
        }

        .project-card:hover {
          transform: translateY(-4px);

          border-color:
            rgba(120,130,255,0.3);

          box-shadow:
            0 22px 55px rgba(0,0,0,0.3);
        }

        .card-top {
          display: flex;
          justify-content: space-between;
          align-items: center;

          gap: 10px;
          margin-bottom: 20px;
        }

        .project-id {
          color: #626e88;

          font-size: 10px;
          font-weight: 700;

          letter-spacing: 1px;
        }

        .status-badge {
          padding: 6px 10px;

          border-radius: 8px;

          font-size: 10px;
          font-weight: 800;
        }

        .status-badge.risk {
          color: #ff8e9b;

          background:
            rgba(255,70,90,0.11);

          border:
            1px solid rgba(255,70,90,0.2);
        }

        .status-badge.delayed {
          color: #ffd27d;

          background:
            rgba(255,180,60,0.11);

          border:
            1px solid rgba(255,180,60,0.2);
        }

        .status-badge.success {
          color: #6ee7b7;

          background:
            rgba(30,200,130,0.11);

          border:
            1px solid rgba(30,200,130,0.2);
        }

        .status-badge.monitoring {
          color: #9ca7ff;

          background:
            rgba(120,130,255,0.11);

          border:
            1px solid rgba(120,130,255,0.2);
        }

        .project-card h2 {
          margin: 0;

          font-size: 20px;
          font-weight: 800;
        }

        .project-description {
          min-height: 42px;

          margin: 9px 0 23px;

          color: #8f9bb5;

          font-size: 12px;
          line-height: 1.6;
        }

        .progress-section {
          margin-bottom: 22px;
        }

        .progress-heading {
          display: flex;
          justify-content: space-between;

          margin-bottom: 9px;

          color: #78849d;

          font-size: 11px;
        }

        .progress-heading strong {
          color: #dce1ff;
        }

        .progress-track {
          height: 7px;

          overflow: hidden;

          border-radius: 20px;

          background:
            rgba(255,255,255,0.07);
        }

        .progress-fill {
          height: 100%;

          border-radius: inherit;

          background:
            linear-gradient(
              90deg,
              #5b4cff,
              #6d8cff
            );
        }

        .card-footer {
          display: flex;
          align-items: center;
          justify-content: space-between;

          gap: 12px;

          padding-top: 15px;

          border-top:
            1px solid rgba(255,255,255,0.06);
        }

        .card-footer > span {
          color: #606c84;
          font-size: 10px;
        }

        .details-button {
          color: #aab2ff;

          text-decoration: none;

          font-size: 11px;
          font-weight: 800;
        }

        .details-button:hover {
          color: #d5d9ff;
        }

        @media (max-width: 800px) {

          .projects-page {
            padding: 22px;
          }

          .projects-header {
            align-items: flex-start;
            flex-direction: column;
          }

          .project-grid {
            grid-template-columns: 1fr;
          }

        }

      `}</style>
    </div>
  );
}

export default ProjectList;