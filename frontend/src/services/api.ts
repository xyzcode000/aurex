export const API_BASE_URL = "http://127.0.0.1:8000";

export async function checkBackendHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error("Backend health check failed");
  }

  return response.json();
}

export async function getProjectRisk(projectId: string) {
  const response = await fetch(`${API_BASE_URL}/api/risk/${projectId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch project risk");
  }

  return response.json();
}