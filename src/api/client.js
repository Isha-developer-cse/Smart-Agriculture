import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5051/api",
  timeout: 20000
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("smart_agro_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
