import axios, { AxiosError } from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("access_token");
    const orgId = localStorage.getItem("active_org_id");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    if (orgId) {
      config.headers["X-Organization-Id"] = orgId;
    }
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // TODO: centralize notification, auth refresh, and route fallback handling.
    return Promise.reject(error);
  },
);

export { api };
