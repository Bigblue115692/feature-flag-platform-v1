const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api/v1";

export class ApiError extends Error {
  constructor(message, { status, payload } = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.payload = payload;
  }
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      "X-Actor": "dashboard-user",
      ...(options.headers || {}),
    },
    ...options,
  });

  let payload = null;
  const text = await response.text();
  if (text) {
    try {
      payload = JSON.parse(text);
    } catch {
      payload = text;
    }
  }

  if (!response.ok) {
    throw new ApiError("API request failed", {
      status: response.status,
      payload,
    });
  }

  return payload;
}

export const api = {
  listProjects() {
    return request("/projects/");
  },

  listEnvironments() {
    return request("/environments/");
  },

  listFlags() {
    return request("/flags/");
  },

  createFlag(data) {
    return request("/flags/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  updateFlag(id, data) {
    return request(`/flags/${id}/`, {
      method: "PATCH",
      body: JSON.stringify(data),
    });
  },

  deleteFlag(id) {
    return request(`/flags/${id}/`, {
      method: "DELETE",
    });
  },

  evaluate(data) {
    return request("/evaluate/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  listAuditEvents() {
    return request("/audit-events/");
  },
};
