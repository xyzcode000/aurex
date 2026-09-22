import { useState } from "react";
import { useNavigate } from "react-router-dom";

function ProjectCreate() {
  const navigate = useNavigate();

  const [projectName, setProjectName] = useState("");
  const [projectBudget, setProjectBudget] = useState("");
  const [projectTimeline, setProjectTimeline] = useState("");

  const handleCreateProject = () => {
    if (!projectName || !projectBudget || !projectTimeline) {
      alert("Please fill all project details.");
      return;
    }

    const existingProjects = JSON.parse(
      localStorage.getItem("aurex_projects") || "[]"
    );

    const usedIds = existingProjects
      .map((project: any) => project.project_id)
      .filter(Boolean);

    let nextNumber = 5;

    while (
      usedIds.includes(
        `AUREX-${String(nextNumber).padStart(3, "0")}`
      )
    ) {
      nextNumber++;
    }

    const newProject = {
      project_id: `AUREX-${String(nextNumber).padStart(3, "0")}`,

      project_name: projectName,

      description:
        "New project created through Aurex Project Intelligence.",

      planned_budget: Number(projectBudget),

      actual_budget: Number(projectBudget),

      planned_timeline: Number(projectTimeline),

      actual_timeline: Number(projectTimeline),

      progress: 0,

      status: "Monitoring",

      risk_level: "MEDIUM",
    };

    const updatedProjects = [
      ...existingProjects,
      newProject,
    ];

    localStorage.setItem(
      "aurex_projects",
      JSON.stringify(updatedProjects)
    );

    alert(
      `${projectName} created successfully as ${newProject.project_id}!`
    );

    setProjectName("");
    setProjectBudget("");
    setProjectTimeline("");

    navigate("/projects");
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        padding: "40px 5%",
        color: "#f8fafc",
        background:
          "radial-gradient(circle at 10% 10%, rgba(37,99,235,0.25), transparent 30%), radial-gradient(circle at 90% 20%, rgba(124,58,237,0.25), transparent 30%), linear-gradient(135deg, #07163f 0%, #090c2c 65%, #18075a 100%)",
        boxSizing: "border-box",
        fontFamily: "Inter, system-ui, sans-serif",
      }}
    >

      {/* Header */}

      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "14px",
          marginBottom: "45px",
        }}
      >

        <div
          style={{
            width: "42px",
            height: "42px",
            borderRadius: "12px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "20px",
            fontWeight: "800",
            background:
              "linear-gradient(135deg, #2563eb, #7c3aed)",
            boxShadow:
              "0 0 25px rgba(79,70,229,0.45)",
          }}
        >
          A
        </div>

        <div>

          <div
            style={{
              fontSize: "22px",
              fontWeight: "800",
              color: "#ffffff",
            }}
          >
            AUREX
          </div>

          <div
            style={{
              fontSize: "12px",
              color: "#8f9dbb",
              letterSpacing: "1px",
            }}
          >
            PROJECT INTELLIGENCE PLATFORM
          </div>

        </div>

      </div>


      {/* Main Content */}

      <div
        style={{
          maxWidth: "900px",
          margin: "0 auto",
        }}
      >

        {/* Heading */}

        <div
          style={{
            textAlign: "center",
            marginBottom: "30px",
          }}
        >

          <div
            style={{
              display: "inline-block",
              padding: "8px 15px",
              borderRadius: "20px",
              fontSize: "12px",
              fontWeight: "700",
              color: "#c4b5fd",
              background:
                "rgba(124,58,237,0.16)",
              border:
                "1px solid rgba(139,92,246,0.35)",
              marginBottom: "16px",
            }}
          >
            PROJECT SETUP
          </div>

          <h1
            style={{
              margin: "0",
              fontSize: "clamp(36px, 5vw, 52px)",
              fontWeight: "800",
              letterSpacing: "-1.5px",
            }}
          >
            Create{" "}

            <span
              style={{
                background:
                  "linear-gradient(90deg, #38bdf8, #8b5cf6, #d946ef)",
                WebkitBackgroundClip: "text",
                backgroundClip: "text",
                color: "transparent",
              }}
            >
              New Project
            </span>

          </h1>

          <p
            style={{
              marginTop: "12px",
              color: "#aeb9d5",
              fontSize: "15px",
            }}
          >
            Enter your project information to start
            intelligent risk monitoring.
          </p>

        </div>


        {/* Form Card */}

        <div
          style={{
            maxWidth: "620px",
            margin: "0 auto",
            padding: "30px",
            borderRadius: "22px",
            background:
              "linear-gradient(145deg, rgba(255,255,255,0.09), rgba(255,255,255,0.035))",
            border:
              "1px solid rgba(110,140,255,0.28)",
            boxShadow:
              "0 25px 60px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.05)",
            backdropFilter: "blur(20px)",
          }}
        >

          {/* Project Name */}

          <div
            style={{
              marginBottom: "22px",
            }}
          >

            <label
              style={{
                display: "block",
                marginBottom: "9px",
                color: "#e2e8f0",
                fontSize: "14px",
                fontWeight: "600",
              }}
            >
              Project Name
            </label>

            <input
              type="text"
              value={projectName}
              onChange={(e) =>
                setProjectName(e.target.value)
              }
              placeholder="Enter project name"
              style={{
                width: "100%",
                padding: "14px 16px",
                borderRadius: "12px",
                border:
                  "1px solid rgba(139,92,246,0.28)",
                outline: "none",
                color: "#ffffff",
                background:
                  "rgba(5,8,22,0.55)",
                boxSizing: "border-box",
                fontSize: "14px",
              }}
            />

          </div>


          {/* Budget */}

          <div
            style={{
              marginBottom: "22px",
            }}
          >

            <label
              style={{
                display: "block",
                marginBottom: "9px",
                color: "#e2e8f0",
                fontSize: "14px",
                fontWeight: "600",
              }}
            >
              Planned Project Budget
            </label>

            <input
              type="number"
              min="0"
              value={projectBudget}
              onChange={(e) =>
                setProjectBudget(e.target.value)
              }
              placeholder="Example: 2500000"
              style={{
                width: "100%",
                padding: "14px 16px",
                borderRadius: "12px",
                border:
                  "1px solid rgba(139,92,246,0.28)",
                outline: "none",
                color: "#ffffff",
                background:
                  "rgba(5,8,22,0.55)",
                boxSizing: "border-box",
                fontSize: "14px",
              }}
            />

            <div
              style={{
                marginTop: "7px",
                color: "#7180a3",
                fontSize: "11px",
              }}
            >
              Enter planned budget in ₹
            </div>

          </div>


          {/* Timeline */}

          <div
            style={{
              marginBottom: "28px",
            }}
          >

            <label
              style={{
                display: "block",
                marginBottom: "9px",
                color: "#e2e8f0",
                fontSize: "14px",
                fontWeight: "600",
              }}
            >
              Planned Project Timeline
            </label>

            <input
              type="number"
              min="1"
              value={projectTimeline}
              onChange={(e) =>
                setProjectTimeline(e.target.value)
              }
              placeholder="Example: 12"
              style={{
                width: "100%",
                padding: "14px 16px",
                borderRadius: "12px",
                border:
                  "1px solid rgba(139,92,246,0.28)",
                outline: "none",
                color: "#ffffff",
                background:
                  "rgba(5,8,22,0.55)",
                boxSizing: "border-box",
                fontSize: "14px",
              }}
            />

            <div
              style={{
                marginTop: "7px",
                color: "#7180a3",
                fontSize: "11px",
              }}
            >
              Enter planned timeline in months
            </div>

          </div>


          {/* Create Button */}

          <button
            onClick={handleCreateProject}
            style={{
              width: "100%",
              padding: "15px",
              border: "none",
              borderRadius: "13px",
              color: "#ffffff",
              fontSize: "15px",
              fontWeight: "700",
              cursor: "pointer",
              background:
                "linear-gradient(90deg, #3b82f6, #7c3aed)",
              boxShadow:
                "0 10px 30px rgba(79,70,229,0.35)",
            }}
          >
            Create Project →
          </button>

        </div>


        {/* Bottom Info */}

        <div
          style={{
            textAlign: "center",
            marginTop: "20px",
            color: "#7180a3",
            fontSize: "12px",
          }}
        >
          Your project can be monitored through Aurex Risk Intelligence.
        </div>

      </div>

    </div>
  );
}

export default ProjectCreate;