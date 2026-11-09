# Adaptação do front-end para o Censo Agrícola

## Tecnologias

- React 19
- Vite 7
- React Router DOM 6
- Axios

## Instalação e execução local

Dentro desta pasta (`frontend`):

```bash
npm ci
npm run dev
```

Por padrão, o Vite encaminha as chamadas iniciadas por `/api` para `http://127.0.0.1:5000`, removendo o prefixo `/api` antes de enviá-las ao Flask. Para alterar o destino durante o desenvolvimento:

```bash
VITE_DEV_API_TARGET=http://127.0.0.1:5000 npm run dev
```

## Compilação de produção

```bash
npm run build
```

O Vite gera os arquivos estáticos em `dist/`. Essa pasta será disponibilizada pelos contêineres Nginx que compõem os nós do Load Balancer.

## Comunicação com a API

O cliente HTTP utiliza `/api` como endereço-base. Em produção, o Nginx de entrada deverá encaminhar `/api/` ao serviço Flask, removendo o prefixo `/api`. Assim, o navegador acessa front-end e API pela mesma origem, sem depender de `localhost` no computador do usuário.

A tela inicial consulta `GET /produtores` e utiliza o campo `data` da resposta paginada do Flask. Os campos exibidos são `nome`, `cpf` e `data_nascimento`.

## Observação

O front-end precisa da API Flask e do PostgreSQL disponíveis para exibir os produtores. Sem a API, a tela apresenta uma mensagem de erro e permite tentar novamente.
