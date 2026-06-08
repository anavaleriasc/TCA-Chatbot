# Chatbot Multiusuário com LLM

Projeto desenvolvido para a disciplina de Tópicos em Computação Aplicada.

## Visão Geral

O sistema consiste em uma aplicação web multiusuário que permite a interação com um modelo de linguagem (LLM) por meio de uma interface de chat.

A solução foi projetada para suportar autenticação de usuários, gerenciamento de sessões de conversa e persistência do histórico de mensagens. A arquitetura é composta por um frontend desenvolvido em Next.js e um backend desenvolvido em FastAPI, responsável pela integração com o modelo de linguagem e pelo acesso ao banco de dados.

## Tecnologias Utilizadas

### Frontend

* Next.js
* React
* TypeScript
* CSS

### Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic
* Pydantic

### Inteligência Artificial

* LangChain
* Google Gemini

### Banco de Dados

* PostgreSQL

### Infraestrutura

* Docker
* Docker Compose
* AWS

---

## Fluxo de Uso

1. O usuário acessa a aplicação web.
2. O usuário realiza autenticação no sistema.
3. O frontend envia requisições HTTP para a API.
4. A API valida o usuário e a sessão ativa.
5. A mensagem enviada é encaminhada para a camada de negócios.
6. O LangChain processa a solicitação e consulta o modelo Gemini.
7. A resposta gerada é retornada para a API.
8. O histórico da conversa é persistido no PostgreSQL.
9. A resposta é enviada ao frontend em formato JSON.
10. O usuário visualiza a resposta na interface do chat.

---

## Estrutura do Projeto

### Backend

```text
app/
├── auth/
├── chatbot/
├── core/
├── db/
├── users/
├── alembic/
├── main.py
└── requirements.txt
```

### Frontend

```text
interface_project/
├── src/
│   ├── app/
│   ├── components/
│   ├── services/
│   ├── data/
│   └── context/
├── public/
└── package.json
```

---

## Configuração do Ambiente

### Pré-requisitos

* Python 3.12+
* Node.js
* Docker Desktop
* Git

É necessário que o Docker esteja em execução antes da inicialização do banco de dados.

---

## Instalação das Dependências

Na raiz do projeto:

```bash
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Inicialização do Banco de Dados

Executar:

```bash
docker compose -f app/docker/docker-compose.yml up db -d
```

Caso ocorra algum problema com os volumes:

```bash
docker compose -f app/docker/docker-compose.yml down -v

docker compose -f app/docker/docker-compose.yml up -d

alembic upgrade head
```

---

## Variáveis de Ambiente

O arquivo `.env` deve estar localizado na raiz do projeto.

Exemplo:

```env
GOOGLE_API_KEY=...
JWS_SECRET_KEY=...

DB_HOST=db
DB_NAME=tca_chatbot
DB_USER=admin
DB_PASSWORD=admin_tca
```

---

## Execução do Backend

Em um terminal:

```bash
cd app

uvicorn main:app --reload
```

A API ficará disponível em:

```text
http://localhost:8000
```

Documentação automática:

```text
http://localhost:8000/docs
```

---

## Execução do Frontend

Em outro terminal:

```bash
cd interface_project

npm install

npm run dev
```

A aplicação ficará disponível em:

```text
http://localhost:3000
```

---

## Fluxo de Comunicação

```text
Usuário
   │
   ▼
Next.js (Frontend)
   │ HTTP/HTTPS + JSON
   ▼
FastAPI (API)
   │
   ▼
LangChain
   │
   ▼
Google Gemini
   │
   ▼
PostgreSQL
   │
   ▼
Resposta ao Usuário
```

---

## Equipe

Projeto desenvolvido no âmbito da disciplina de Tópicos em Computação Aplicada.
