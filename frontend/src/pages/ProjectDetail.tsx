import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { projectsData } from "../mocks/projectsData";

interface Project {
  project_id: string;
  project_name: string;
  description: string;
  planned_budget: number;
  actual_budget: number;
  planned_timeline: number;
  actual_timeline: number;
  progress: number;
  status: string;
  risk_level: string;
}

function ProjectDetail() {
  const [searchParams] = useSearchParams();
  

  const savedProjects: Project[] = JSON.parse(
    localStorage.getItem("aurex_projects") || "[]"
  );

  const defaultProjects: Project[] = projectsData;

  const createdProjects: Project[] = savedProjects.map(
    (project: any, index: number) => ({
      project_id:
        project.project_id ||
        `AUREX-${String(index + 5).padStart(3, "0")}`,

      project_name:
        project.project_name || "Untitled Project",

      description:
        project.description ||
        "New project created through Aurex Project Intelligence.",

      planned_budget:
        Number(project.planned_budget || project.budget || 0),

      actual_budget:
        Number(
          project.actual_budget ||
            project.planned_budget ||
            project.budget ||
            0
        ),

      planned_timeline:
        Number(project.planned_timeline || project.timeline || 0),

      actual_timeline:
        Number(
          project.actual_timeline ||
            project.planned_timeline ||
            project.timeline ||
            0
        ),

      progress:
        Number(project.progress || 0),

      status:
        project.status || "Monitoring",

      risk_level:
        project.risk_level || "MEDIUM",
    })
  );

  const allProjects = [...defaultProjects, ...createdProjects];

  const uniqueProjects = allProjects.filter(
    (project, index, array) =>
      index ===
      array.findIndex(
        (item) =>
          item.project_id === project.project_id
      )
  );

  const requestedProjectId = searchParams.get("project");

  const initialProject =
    uniqueProjects.find(
      (project) =>
        project.project_id === requestedProjectId
    ) || uniqueProjects[0];

  const [selectedProject, setSelectedProject] =
    useState<Project>(initialProject);
    useEffect(() => {
  localStorage.setItem(
    "aurex_active_project",
    JSON.stringify(selectedProject)
  );
}, [selectedProject]);

  const budgetChartData = [
    {
      name: "Budget",
      planned: selectedProject.planned_budget,
      actual: selectedProject.actual_budget,
    },
  ];

  const timelineChartData = [
    {
      name: "Timeline",
      planned: selectedProject.planned_timeline,
      actual: selectedProject.actual_timeline,
    },
  ];

  const getRiskClass = (risk: string) => {
    if (risk === "HIGH") return "high";
    if (risk === "LOW") return "low";
    return "medium";
  };

  return (
    <div className="detail-page">

      <div className="detail-container">

        {/* Header */}

        <div className="page-header">

          <div>

            <p className="eyebrow">
              AUREX PROJECT INTELLIGENCE
            </p>

            <h1>
              Project Detail
            </h1>

            <p className="subtitle">
              Explore project performance, budget, timeline and risk intelligence.
            </p>

          </div>

        </div>


        {/* Project Selector */}

        <div className="project-selector">

          <div className="selector-heading">

            <div>

              <h2>
                Select Project
              </h2>

              <p>
                Choose a project to inspect its details.
              </p>

            </div>

            <span>
              {uniqueProjects.length} Projects
            </span>

          </div>


          <div className="selector-list">

            {uniqueProjects.map((project) => (

              <button
                key={project.project_id}
                className={`selector-card ${
                  selectedProject.project_id ===
                  project.project_id
                    ? "active"
                    : ""
                }`}
              onClick={() => {
  setSelectedProject(project);
  localStorage.setItem(
    "aurex_active_project",
    JSON.stringify(project)
  );
}}
              >

                <strong>
                  {project.project_name}
                </strong>

                <small>
                  {project.project_id}
                </small>

              </button>

            ))}

          </div>

        </div>


        {/* Project Overview */}

        <div className="project-overview">

          <div className="overview-header">

            <div>

              <p className="project-id">
                {selectedProject.project_id}
              </p>

              <h2>
                {selectedProject.project_name}
              </h2>

              <p className="description">
                {selectedProject.description}
              </p>

            </div>


            <div
              className={`risk-badge ${getRiskClass(
                selectedProject.risk_level
              )}`}
            >
              {selectedProject.risk_level} RISK
            </div>

          </div>


          <div className="overview-grid">

            <div className="info-card">

              <span>
                Project Status
              </span>

              <strong>
                {selectedProject.status}
              </strong>

            </div>


            <div className="info-card">

              <span>
                Progress
              </span>

              <strong>
                {selectedProject.progress}%
              </strong>

              <div className="progress-track">

                <div
                  className="progress-fill"
                  style={{
                    width: `${selectedProject.progress}%`,
                  }}
                />

              </div>

            </div>


            <div className="info-card">

              <span>
                Planned Budget
              </span>

              <strong>
                ₹{selectedProject.planned_budget}L
              </strong>

            </div>


            <div className="info-card">

              <span>
                Planned Timeline
              </span>

              <strong>
                {selectedProject.planned_timeline} Months
              </strong>

            </div>

          </div>

        </div>


        {/* Performance */}

        <div className="performance-grid">


          {/* Budget */}

          <div className="visualization-card">

            <div className="section-title">

              <div>

                <p className="eyebrow">
                  PERFORMANCE
                </p>

                <h2>
                  Budget Performance
                </h2>

              </div>

              <span>
                Planned vs Actual
              </span>

            </div>


            <div className="chart-wrapper">

              <ResponsiveContainer
                width="100%"
                height={280}
              >

                <BarChart
                  data={budgetChartData}
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="rgba(255,255,255,0.07)"
                  />

                  <XAxis
                    dataKey="name"
                    stroke="#78849d"
                  />

                  <YAxis
                    stroke="#78849d"
                  />

                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#101629",
                      border:
                        "1px solid rgba(255,255,255,0.1)",
                      borderRadius: "10px",
                      color: "#fff",
                    }}
                  />

                  <Bar
                    dataKey="planned"
                    name="Planned Budget (₹ Lakhs)"
                    fill="#6d7cff"
                    radius={[6, 6, 0, 0]}
                  />

                  <Bar
                    dataKey="actual"
                    name="Actual Budget (₹ Lakhs)"
                    fill="#ff6b81"
                    radius={[6, 6, 0, 0]}
                  />

                </BarChart>

              </ResponsiveContainer>

            </div>


            <div className="metric-summary">

              <div>

                <span>
                  Planned Budget
                </span>

                <strong>
                  ₹{selectedProject.planned_budget}L
                </strong>

              </div>


              <div>

                <span>
                  Actual Budget
                </span>

                <strong>
                  ₹{selectedProject.actual_budget}L
                </strong>

              </div>

            </div>

          </div>


          {/* Timeline */}

          <div className="visualization-card">

            <div className="section-title">

              <div>

                <p className="eyebrow">
                  PERFORMANCE
                </p>

                <h2>
                  Timeline Performance
                </h2>

              </div>

              <span>
                Planned vs Actual
              </span>

            </div>


            <div className="chart-wrapper">

              <ResponsiveContainer
                width="100%"
                height={280}
              >

                <BarChart
                  data={timelineChartData}
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="rgba(255,255,255,0.07)"
                  />

                  <XAxis
                    dataKey="name"
                    stroke="#78849d"
                  />

                  <YAxis
                    stroke="#78849d"
                  />

                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#101629",
                      border:
                        "1px solid rgba(255,255,255,0.1)",
                      borderRadius: "10px",
                      color: "#fff",
                    }}
                  />

                  <Bar
                    dataKey="planned"
                    name="Planned Timeline (Months)"
                    fill="#6d7cff"
                    radius={[6, 6, 0, 0]}
                  />

                  <Bar
                    dataKey="actual"
                    name="Actual Timeline (Months)"
                    fill="#ff6b81"
                    radius={[6, 6, 0, 0]}
                  />

                </BarChart>

              </ResponsiveContainer>

            </div>


            <div className="metric-summary">

              <div>

                <span>
                  Planned Timeline
                </span>

                <strong>
                  {selectedProject.planned_timeline} Months
                </strong>

              </div>


              <div>

                <span>
                  Actual Timeline
                </span>

                <strong>
                  {selectedProject.actual_timeline} Months
                </strong>

              </div>

            </div>

          </div>

        </div>


        {/* Intelligence */}

        <div className="intelligence-card">

          <div className="intelligence-icon">
            AI
          </div>


          <div>

            <p className="eyebrow">
              PROJECT INTELLIGENCE
            </p>

            <h2>
              Current Project Assessment
            </h2>

            <p>

              {selectedProject.project_name} is currently
              showing{" "}

              <strong>
                {selectedProject.risk_level}
              </strong>{" "}

              risk with{" "}

              <strong>
                {selectedProject.progress}%
              </strong>{" "}

              project progress. Budget and timeline
              performance are being monitored through
              the AUREX intelligence system.

            </p>

          </div>

        </div>

      </div>


      <style>{`

        .detail-page {
          min-height: 100vh;
          padding: 42px;
          box-sizing: border-box;
          color: #f5f7ff;

          background:
            radial-gradient(
              circle at top right,
              rgba(91,76,255,0.16),
              transparent 35%
            ),
            radial-gradient(
              circle at bottom left,
              rgba(0,212,255,0.07),
              transparent 30%
            ),
            #070b17;

          font-family: Inter, system-ui, sans-serif;
        }


        .detail-container {
          max-width: 1200px;
          margin: 0 auto;
        }


        .page-header {
          margin-bottom: 30px;
        }


        .eyebrow {
          margin: 0 0 8px;
          color: #8d9cff;
          font-size: 10px;
          font-weight: 800;
          letter-spacing: 2px;
        }


        .page-header h1 {
          margin: 0;
          font-size: 34px;
          font-weight: 800;
        }


        .subtitle {
          margin: 9px 0 0;
          color: #8f9bb5;
          font-size: 14px;
        }


        .project-selector,
        .project-overview,
        .visualization-card,
        .intelligence-card {

          border:
            1px solid rgba(255,255,255,0.08);

          border-radius: 21px;

          background:
            rgba(14,19,35,0.78);

          backdrop-filter: blur(15px);

          box-shadow:
            0 18px 50px rgba(0,0,0,0.2);

        }


        .project-selector {
          padding: 23px;
          margin-bottom: 20px;
        }


        .selector-heading {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 18px;
        }


        .selector-heading h2 {
          margin: 0;
          font-size: 17px;
        }


        .selector-heading p {
          margin: 5px 0 0;
          color: #78849d;
          font-size: 11px;
        }


        .selector-heading > span {
          color: #9ca7ff;
          font-size: 11px;
          font-weight: 700;
        }


        .selector-list {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 12px;
        }


        .selector-card {
          padding: 15px;

          text-align: left;

          border:
            1px solid rgba(255,255,255,0.07);

          border-radius: 13px;

          background:
            rgba(255,255,255,0.025);

          color: white;

          cursor: pointer;

          transition: 0.2s ease;
        }


        .selector-card:hover {
          transform: translateY(-2px);

          border-color:
            rgba(120,130,255,0.4);
        }


        .selector-card.active {
          border-color:
            rgba(120,130,255,0.7);

          background:
            rgba(91,76,255,0.12);
        }


        .selector-card strong {
          display: block;
          font-size: 12px;
          margin-bottom: 6px;
        }


        .selector-card small {
          color: #68748d;
          font-size: 9px;
        }


        .project-overview {
          padding: 27px;
          margin-bottom: 20px;
        }


        .overview-header {
          display: flex;
          justify-content: space-between;
          gap: 20px;
        }


        .project-id {
          margin: 0 0 6px;
          color: #68748d;
          font-size: 10px;
          font-weight: 700;
          letter-spacing: 1px;
        }


        .overview-header h2 {
          margin: 0;
          font-size: 26px;
        }


        .description {
          max-width: 650px;
          margin: 8px 0 0;
          color: #8f9bb5;
          font-size: 12px;
          line-height: 1.6;
        }


        .risk-badge {
          height: fit-content;

          padding: 9px 15px;

          border-radius: 10px;

          font-size: 10px;
          font-weight: 900;

          letter-spacing: 1px;

          white-space: nowrap;
        }


        .risk-badge.high {
          color: #ff8e9b;

          background:
            rgba(255,70,90,0.11);

          border:
            1px solid rgba(255,70,90,0.22);
        }


        .risk-badge.medium {
          color: #ffd27d;

          background:
            rgba(255,180,60,0.11);

          border:
            1px solid rgba(255,180,60,0.22);
        }


        .risk-badge.low {
          color: #6ee7b7;

          background:
            rgba(30,200,130,0.11);

          border:
            1px solid rgba(30,200,130,0.22);
        }


        .overview-grid {
          display: grid;

          grid-template-columns:
            repeat(4, 1fr);

          gap: 13px;

          margin-top: 25px;
        }


        .info-card {
          padding: 18px;

          border-radius: 14px;

          background:
            rgba(255,255,255,0.035);

          border:
            1px solid rgba(255,255,255,0.06);
        }


        .info-card span {
          display: block;
          color: #727e97;
          font-size: 10px;
          margin-bottom: 9px;
        }


        .info-card strong {
          font-size: 17px;
        }


        .progress-track {
          height: 5px;

          margin-top: 12px;

          border-radius: 10px;

          background:
            rgba(255,255,255,0.07);

          overflow: hidden;
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


        .performance-grid {
          display: grid;

          grid-template-columns:
            repeat(2, minmax(0, 1fr));

          gap: 20px;

          margin-bottom: 20px;
        }


        .visualization-card {
          padding: 25px;
        }


        .section-title {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }


        .section-title h2 {
          margin: 0;
          font-size: 18px;
        }


        .section-title > span {
          color: #68748d;
          font-size: 10px;
        }


        .chart-wrapper {
          margin-top: 20px;
          width: 100%;
        }


        .metric-summary {
          display: flex;
          gap: 12px;
          margin-top: 10px;
        }


        .metric-summary > div {
          flex: 1;

          padding: 14px;

          border-radius: 12px;

          background:
            rgba(255,255,255,0.03);

          border:
            1px solid rgba(255,255,255,0.06);
        }


        .metric-summary span {
          display: block;

          color: #727e97;

          font-size: 10px;

          margin-bottom: 7px;
        }


        .metric-summary strong {
          font-size: 14px;
        }


        .intelligence-card {
          display: flex;

          gap: 16px;

          padding: 22px;
        }


        .intelligence-icon {
          width: 38px;
          height: 38px;

          flex-shrink: 0;

          display: grid;
          place-items: center;

          border-radius: 10px;

          color: #aab2ff;

          background:
            rgba(120,130,255,0.12);

          font-size: 10px;
          font-weight: 900;
        }


        .intelligence-card h2 {
          margin: 0;
          font-size: 15px;
        }


        .intelligence-card p:last-child {
          max-width: 850px;

          margin: 7px 0 0;

          color: #8f9bb5;

          font-size: 12px;

          line-height: 1.65;
        }


        .intelligence-card strong {
          color: #dce1ff;
        }


        @media (max-width: 900px) {

          .detail-page {
            padding: 22px;
          }

          .selector-list {
            grid-template-columns:
              repeat(2, 1fr);
          }

          .overview-grid {
            grid-template-columns:
              repeat(2, 1fr);
          }

          .performance-grid {
            grid-template-columns: 1fr;
          }

          .overview-header {
            flex-direction: column;
          }

        }


        @media (max-width: 550px) {

          .selector-list,
          .overview-grid {
            grid-template-columns: 1fr;
          }

          .metric-summary {
            flex-direction: column;
          }

        }

      `}</style>

    </div>
  );
}

export default ProjectDetail;