export interface Project {
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

export const projectsData: Project[] = [
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
  },
];