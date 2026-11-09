import { useProdutores } from "../hooks/useProdutores";
import ProdutorCard from "../components/ProdutorCard";

export default function Produtores() {
  const { produtores, loading, error, recarregar } = useProdutores();

  return (
    <main className="page-shell">
      <header className="page-header">
        <div>
          <p className="eyebrow">CENSO AGRÍCOLA</p>
          <h1>Produtores rurais</h1>
          <p className="page-description">
            Consulte os produtores cadastrados no sistema.
          </p>
        </div>
        <span className="producer-count">
          {produtores.length} {produtores.length === 1 ? "produtor" : "produtores"}
        </span>
      </header>

      {loading && <p className="feedback">Carregando produtores...</p>}

      {!loading && error && (
        <section className="feedback feedback--error" role="alert">
          <p>{error}</p>
          <button type="button" onClick={recarregar}>
            Tentar novamente
          </button>
        </section>
      )}

      {!loading && !error && produtores.length === 0 && (
        <p className="feedback">Nenhum produtor cadastrado.</p>
      )}

      {!loading && !error && produtores.length > 0 && (
        <section className="producer-list" aria-label="Lista de produtores">
          {produtores.map((produtor) => (
            <ProdutorCard key={produtor.id} produtor={produtor} />
          ))}
        </section>
      )}
    </main>
  );
}
