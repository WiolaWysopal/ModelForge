import type { HealthResponse } from "../types/health";

const API_URL = "http://localhost:8000";

export async function getHealthStatus(): Promise<HealthResponse> {
  const response = await fetch(`${API_URL}/health`);

  if (!response.ok) {
    throw new Error(`Health check failed with status ${response.status}`);
  }

  return response.json() as Promise<HealthResponse>;
}