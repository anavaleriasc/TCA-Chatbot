# Chatbot Multiusuário com Gemini AI 🤖

Repositório destinado ao protótipo do chatbot desenvolvido para a disciplina **Tópicos em Computação Aplicada**.

## 📌 Sobre o Projeto

O projeto consiste em uma aplicação web multiusuário onde os usuários podem interagir com um modelo LLM (Large Language Model), utilizando o **Google Gemini 2.5 Flash** como motor de inteligência artificial.

A aplicação foi projetada para gerenciar sessões independentes de conversa, garantindo o isolamento do histórico entre diferentes usuários. O sistema é composto por um backend responsável pela comunicação com a API do Gemini e um frontend moderno desenvolvido em Next.js.

---

## 🚀 Tecnologias Utilizadas

### Backend

* Python 3
* FastAPI
* Uvicorn
* Pydantic
* Python Dotenv

### Inteligência Artificial

* Google Gemini 2.5 Flash
* SDK oficial `google-genai`

### Frontend

* Next.js 15
* React 19
* TypeScript
* CSS Modules
* Fetch API para comunicação com o backend

### Infraestrutura

* AWS EC2 (implantação planejada)

---

## 🏗️ Arquitetura do Sistema

### Backend

A aplicação backend segue o princípio de **Separation of Concerns (SoC)**, distribuindo responsabilidades entre módulos específicos:

* `main.py` — Inicialização da aplicação FastAPI e configuração dos recursos.
* `routes.py` — Definição dos endpoints REST da API.
* `session_manager.py` — Gerenciamento de sessões e histórico de conversas por usuário.
* `llm_service.py` — Integração com a API do Google Gemini.
* `.env` — Armazenamento seguro das variáveis de ambiente.

### Frontend

O frontend foi desenvolvido utilizando a arquitetura baseada em componentes do Next.js:

* `src/app/` — Rotas e páginas da aplicação.
* `src/components/` — Componentes reutilizáveis da interface.
* `src/mocks/` — Dados simulados utilizados durante o desenvolvimento.
* `src/styles/` — Estilos globais e específicos dos componentes.
* `public/` — Arquivos estáticos da aplicação.

Principais componentes:

* **Sidebar** — Exibição das conversas do usuário.
* **ChatWindow** — Área principal de exibição das mensagens.
* **MessageBubble** — Renderização das mensagens do usuário e do assistente.
* **MessageInput** — Campo de entrada e envio de mensagens.

---

## ⚙️ Como Executar o Projeto

### 1. Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd chatbot-project
```

---

## Backend

### 2. Criar Ambiente Virtual

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```
### 4. Banco de Dados

```
docker compose -f app/docker/
docker-compose.yml up db-d
alembic upgrade head
```


### 5. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do backend:

```env
GOOGLE_API_KEY=sua_chave_aqui
```

### 6. Executar o Backend

```bash
uvicorn main:app --reload
```

O servidor ficará disponível em:

```text
http://127.0.0.1:8000
```

---

## Frontend

### 7. Instalar Dependências

```bash
npm install
```

### 8. Executar o Frontend

```bash
npm run dev
```

O frontend ficará disponível em:

```text
http://localhost:3000
```

---

## 🔄 Fluxo de Funcionamento

1. O usuário envia uma mensagem pela interface web.
2. O frontend realiza uma requisição HTTP para o backend.
3. O backend identifica a sessão do usuário.
4. O histórico da conversa é recuperado.
5. A mensagem é enviada ao Google Gemini.
6. A resposta gerada é retornada ao backend.
7. O backend atualiza o histórico da sessão.
8. A resposta é exibida ao usuário na interface.

---

## ☁️ Implantação na AWS

A entrega final prevê a implantação da aplicação em uma instância EC2 da AWS.

A infraestrutura deverá conter:

* Frontend Next.js em produção;
* Backend FastAPI executando via Uvicorn/Gunicorn;
* Configuração de variáveis de ambiente seguras;
* Acesso público por endereço IP ou domínio.

---

## 👥 Equipe

Projeto desenvolvido para a disciplina **Tópicos em Computação Aplicada**.
