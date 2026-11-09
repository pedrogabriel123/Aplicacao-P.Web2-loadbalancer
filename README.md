# Censo Agrícola — Load Balancer

Projeto desenvolvido para a **Atividade 2 — Criação do Load Balancer para recursos da aplicação Front-end**, da disciplina **Gerência e Configuração de Serviços para Internet (GCSI)**.

A aplicação utiliza um **Nginx como Load Balancer**, distribuindo as requisições entre cinco réplicas do frontend React por meio do algoritmo **Round Robin**. O frontend consulta uma API desenvolvida em Flask, que utiliza PostgreSQL para persistência dos dados.

## 1. Arquitetura

A infraestrutura é composta por oito containers Docker:

| Serviço | Container | Tecnologia | Porta interna |
|---|---|---|---:|
| Load Balancer | `censo-agricula-lb` | Nginx | 80 |
| Frontend 1 | `no1` | React + Nginx | 80 |
| Frontend 2 | `no2` | React + Nginx | 80 |
| Frontend 3 | `no3` | React + Nginx | 80 |
| Frontend 4 | `no4` | React + Nginx | 80 |
| Frontend 5 | `no5` | React + Nginx | 80 |
| Backend | `censo-agricula-api` | Flask | 5000 |
| Banco de dados | `censo-agricula-db` | PostgreSQL 15 | 5432 |

O Load Balancer é publicado na máquina hospedeira pela porta **8080**. Portanto, a aplicação pode ser acessada pelo navegador em:

```text
http://localhost:8080
```

Os containers se comunicam pela rede Docker bridge `censo-agricola-network`, que permite a resolução dos serviços pelos nomes dos próprios containers.

### Fluxo das requisições

```text
                         Navegador
                             |
                             v
                    localhost:8080
                             |
                             v
                 Nginx — Load Balancer
                             |
                  Round Robin (HTTP)
                 /    /    |    \    \
                v    v     v     v    v
              no1  no2   no3   no4  no5
                 \    \    |    /    /
                     React + Nginx
                           |
                    Requisições /api/
                           |
                           v
                       Flask API
                           |
                           v
                       PostgreSQL
```

O caminho `/api/` é encaminhado pelo Load Balancer ao backend. A configuração atual remove o prefixo `/api/` antes de encaminhar a requisição. Por exemplo, `/api/produtores` chega ao Flask como `/produtores`.

## 2. Estrutura do projeto

A estrutura relevante para a infraestrutura é:

```text
Censo-Agricula/
├── backend/
│   ├── app/
│   ├── .env
│   ├── .env.example
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   ├── dist/
│   ├── src/
│   ├── default.conf
│   └── Dockerfile
├── loadbalancer/
│   ├── Dockerfile
│   └── nginx.conf
├── monitorar.sh
└── README.md
```

> A pasta `frontend/dist` contém a versão compilada do React, que é copiada para a imagem Nginx do frontend.

## 3. Pré-requisitos

- Linux ou outro sistema compatível com Docker.
- Docker Engine instalado e em execução.
- Node.js e npm para compilar o frontend.
- Arquivo de variáveis de ambiente do backend configurado.
- Banco PostgreSQL disponível em um container conectado à rede da aplicação.

Os comandos abaixo usam `docker run` diretamente. Caso seja utilizado Docker Compose em outro ambiente, os serviços podem ser adaptados para um arquivo Compose.

## 4. Configuração da rede Docker

Crie a rede bridge utilizada pelos containers:

```bash
docker network create \
  --driver bridge \
  censo-agricola-network
```

Se a rede já existir, não é necessário criá-la novamente.

O banco de dados precisa estar conectado a essa rede. Para conectar um container PostgreSQL já existente:

```bash
docker network connect censo-agricola-network censo-agricula-db
```

Se ele já estiver conectado, o Docker informará que a conexão já existe. **Não remova o container nem o volume do banco para executar essa etapa**, pois eles podem conter dados persistentes.

## 5. Configuração e execução

Execute os comandos a partir da raiz do repositório.

### 5.1. Compilar o frontend

Entre na pasta do frontend, instale as dependências e gere a versão de produção:

```bash
cd frontend
npm install
npm run build
cd ..
```

A compilação deve gerar a pasta `frontend/dist`, utilizada na construção da imagem Docker.

### 5.2. Construir a imagem do frontend

```bash
docker build \
  -t censo-agricula-frontend:1.0.0 \
  ./frontend
```

### 5.3. Iniciar as cinco réplicas do frontend

```bash
docker run -d --name no1 --network censo-agricola-network censo-agricula-frontend:1.0.0
docker run -d --name no2 --network censo-agricola-network censo-agricula-frontend:1.0.0
docker run -d --name no3 --network censo-agricola-network censo-agricula-frontend:1.0.0
docker run -d --name no4 --network censo-agricola-network censo-agricula-frontend:1.0.0
docker run -d --name no5 --network censo-agricola-network censo-agricula-frontend:1.0.0
```

Cada réplica executa o Nginx na porta interna 80. Não é necessário publicar individualmente essas portas no host, pois o acesso externo é realizado pelo Load Balancer.

### 5.4. Configurar o backend

Configure `backend/.env` com as credenciais e os dados de conexão do PostgreSQL. Os valores de referência para os campos não secretos são:

```dotenv
DB_USER=user
DB_HOST=censo-agricula-db
DB_PORT=5432
DB_NAME=app_db
```

A senha deve ser definida localmente no arquivo `.env`, de acordo com a configuração do PostgreSQL. **Não publique esse arquivo no GitHub.** O repositório deve conter apenas um arquivo de exemplo sem credenciais reais.

Construa a imagem:

```bash
docker build \
  -t censo-agricula-backend:1.0.0 \
  ./backend
```

Inicie o backend:

```bash
docker run -d \
  --name censo-agricula-api \
  --network censo-agricola-network \
  --env-file backend/.env \
  censo-agricula-backend:1.0.0
```

O backend escuta na porta interna 5000 e se conecta ao banco pelo nome do container `censo-agricula-db`.

### 5.5. Construir a imagem do Load Balancer

```bash
docker build \
  -t censo-agricula-loadbalancer:1.0.0 \
  ./loadbalancer
```

### 5.6. Iniciar o Load Balancer

```bash
docker run -d \
  --name censo-agricula-lb \
  --network censo-agricola-network \
  -p 8080:80 \
  censo-agricula-loadbalancer:1.0.0
```

O serviço ficará disponível em `http://localhost:8080`.

> **Ordem de inicialização:** banco de dados, backend, cinco frontends e, por último, Load Balancer. O Nginx precisa conseguir resolver os nomes dos cinco nós e do backend ao iniciar.

## 6. Configurações do Nginx

### 6.1. Load Balancer — `loadbalancer/nginx.conf`

O bloco `upstream` define os cinco servidores que recebem as requisições:

```nginx
upstream frontend_nodes {
    server no1:80;
    server no2:80;
    server no3:80;
    server no4:80;
    server no5:80;
}
```

O Nginx utiliza Round Robin como algoritmo padrão quando não é especificado outro método no bloco `upstream`. Assim, as requisições são distribuídas sequencialmente entre os servidores disponíveis.

O caminho `/api/` é encaminhado ao backend Flask:

```nginx
location /api/ {
    proxy_pass http://censo-agricula-api:5000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

As demais requisições são encaminhadas ao grupo de frontends:

```nginx
location / {
    proxy_pass http://frontend_nodes;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### 6.2. Frontend — `frontend/default.conf`

O Nginx de cada réplica entrega os arquivos estáticos compilados do React e utiliza `index.html` como fallback para as rotas da aplicação:

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    add_header X-Backend-Server $hostname always;
}
```

O cabeçalho `X-Backend-Server` permite identificar a réplica que respondeu à requisição.

## 7. Verificação e testes

### 7.1. Verificar os containers

```bash
docker ps
```

Devem estar em execução o Load Balancer, as cinco réplicas do frontend, o backend e o banco de dados.

### 7.2. Validar a configuração do Load Balancer

```bash
docker exec censo-agricula-lb nginx -t
```

O resultado esperado indica que a sintaxe está correta e que o teste da configuração foi bem-sucedido.

### 7.3. Testar o frontend

Acesse:

```text
http://localhost:8080
```

### 7.4. Testar a API pelo Load Balancer

```bash
curl -i http://localhost:8080/api/produtores
```

Uma resposta HTTP 200 indica que o encaminhamento ao backend está funcionando. A API pode retornar uma lista vazia caso ainda não existam produtores cadastrados.

### 7.5. Verificar a distribuição Round Robin

```bash
for i in {1..10}; do
  curl -s -I http://localhost:8080/ | grep -i X-Backend-Server
done
```

O cabeçalho `X-Backend-Server` permite observar as respostas das diferentes réplicas.

### 7.6. Testar tolerância a falhas

Interrompa uma réplica:

```bash
docker stop no1
```

Faça novas requisições ao frontend e verifique se as demais réplicas continuam respondendo.

Depois, restaure a réplica:

```bash
docker start no1
```

Faça novas requisições e verifique se ela volta a participar da distribuição.

**Resultado observado nos testes do projeto:** a aplicação continuou acessível quando `no1` foi interrompido, e a réplica voltou a receber requisições após ser iniciada novamente.

## 8. Monitoramento em tempo real

O script `monitorar.sh` acompanha os logs de acesso dos cinco frontends e do backend.

Para executá-lo:

```bash
chmod +x monitorar.sh
./monitorar.sh
```

O painel apresenta:

- Quantidade de requisições recebidas por frontend.
- Percentual de distribuição entre as cinco réplicas.
- Quantidade de requisições recebidas pelo backend.
- Histórico de requisições, métodos HTTP, rotas e códigos de status.
- Contagem de respostas HTTP com status 400 ou superior.

Para encerrar o monitoramento, pressione `Ctrl + C`.

## 9. Comandos úteis do Docker

| Objetivo | Comando |
|---|---|
| Listar containers ativos | `docker ps` |
| Listar todos os containers | `docker ps -a` |
| Consultar logs do Load Balancer | `docker logs censo-agricula-lb` |
| Consultar logs do backend | `docker logs censo-agricula-api` |
| Consultar logs de uma réplica | `docker logs no1` |
| Parar os serviços principais | `docker stop censo-agricula-lb censo-agricula-api no1 no2 no3 no4 no5` |
| Iniciar os serviços principais | `docker start no1 no2 no3 no4 no5 censo-agricula-api censo-agricula-lb` |

O banco de dados é mantido separadamente para preservar sua persistência. Evite remover seu container ou volume sem antes verificar a necessidade e realizar backup.

## 10. Segurança e publicação

Antes de publicar o projeto no GitHub:

- Não envie `backend/.env` nem senhas ou credenciais reais.
- Mantenha um `.env.example` com valores fictícios ou campos sem segredos.
- Confirme que arquivos de ambiente estão protegidos pelo `.gitignore`.
- Não remova volumes persistentes do PostgreSQL durante a manutenção da infraestrutura.

## 11. Tecnologias utilizadas

- **Docker:** conteinerização e execução isolada dos serviços.
- **Nginx:** servidor web e Load Balancer.
- **Round Robin:** algoritmo de distribuição de requisições.
- **React:** interface frontend.
- **Flask:** API backend.
- **PostgreSQL 15:** banco de dados relacional.
- **Linux:** ambiente de execução e administração dos containers.

---

**Projeto:** Censo Agrícola  
**Atividade:** Atividade 2 — Criação do Load Balancer para recursos da aplicação Front-end  
**Disciplina:** Gerência e Configuração de Serviços para Internet (GCSI)
