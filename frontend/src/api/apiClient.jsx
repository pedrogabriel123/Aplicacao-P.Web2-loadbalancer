import axios from "axios";

// Em produção, /api será encaminhado pelo Nginx ao serviço Flask.
// No desenvolvimento, o Vite fará o proxy conforme vite.config.js.
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  timeout: 10000,
});

export default apiClient;
