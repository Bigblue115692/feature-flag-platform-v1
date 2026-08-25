import type { Environment, EvaluationResponse, FeatureFlag, Project } from "./types";

const BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
const ADMIN = import.meta.env.VITE_ADMIN_API_KEY ?? "dev-admin-key";
const SDK = import.meta.env.VITE_SDK_API_KEY ?? "dev-sdk-key";

async function call<T>(path: string, options: RequestInit = {}, sdk = false): Promise<T> {
  const response = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": sdk ? SDK : ADMIN,
      ...(options.headers ?? {}),
    },
  });

  if (!response.ok) throw new Error(`${response.status}: ${await response.text()}`);
  if (response.status === 204) return undefined as T;
  return response.json();
}

export const api = {
  projects: () => call<Project[]>("/api/projects"),
  environments: (projectId: number) => call<Environment[]>(`/api/projects/${projectId}/environments`),
  flags: (environmentId: number) => call<FeatureFlag[]>(`/api/environments/${environmentId}/flags`),

  createFlag: (environmentId: number, payload: object) =>
    call<FeatureFlag>(`/api/environments/${environmentId}/flags`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  updateFlag: (flagId: number, payload: object) =>
    call<FeatureFlag>(`/api/flags/${flagId}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    }),

  evaluate: (payload: object) =>
    call<EvaluationResponse>(
      "/api/evaluate",
      { method: "POST", body: JSON.stringify(payload) },
      true,
    ),
};
