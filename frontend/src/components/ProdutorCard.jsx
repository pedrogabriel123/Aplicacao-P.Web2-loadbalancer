function formatarData(data) {
  if (!data) return "Não informada";

  // O Flask serializa datas no formato ISO: AAAA-MM-DD.
  const [ano, mes, dia] = data.split("-");
  if (!ano || !mes || !dia) return data;
  return `${dia}/${mes}/${ano}`;
}

export default function ProdutorCard({ produtor }) {
  return (
    <article className="producer-card">
      <div className="producer-card__avatar" aria-hidden="true">
        {produtor.nome?.trim().charAt(0).toUpperCase() || "P"}
      </div>

      <div className="producer-card__details">
        <h2>{produtor.nome || "Nome não informado"}</h2>
        <p>
          <span>CPF:</span> {produtor.cpf || "Não informado"}
        </p>
        <p>
          <span>Data de nascimento:</span> {formatarData(produtor.data_nascimento)}
        </p>
      </div>
    </article>
  );
}
