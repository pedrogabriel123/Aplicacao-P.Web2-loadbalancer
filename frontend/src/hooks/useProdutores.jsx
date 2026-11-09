import { useCallback, useEffect, useState } from "react";
import { produtorService } from "../api/produtorService";

export function useProdutores() {
  const [produtores, setProdutores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const carregarProdutores = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const data = await produtorService.listar();
      setProdutores(data);
    } catch (err) {
      console.error("Erro ao buscar produtores:", err);
      setError(
        err.response?.data?.message ||
          "Não foi possível carregar os produtores. Verifique se a API está em execução."
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    carregarProdutores();
  }, [carregarProdutores]);

  return { produtores, loading, error, recarregar: carregarProdutores };
}
