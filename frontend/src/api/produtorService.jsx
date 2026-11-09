import apiClient from "./apiClient";

export const produtorService = {
  async listar() {
    const response = await apiClient.get("/produtores");
    return response.data.data ?? [];
  },
};
