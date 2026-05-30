# Chatbot Multiusuário com Gemini AI 🤖

Repositório destinado ao protótipo do chatbot desenvolvido para a disciplina **Tópicos em Computação Aplicada**.

## 📌 Sobre o Projeto
O projeto consiste em uma aplicação web multiusuário onde os clientes podem interagir com um modelo LLM (Large Language Model) - neste caso, o mais recente **Google Gemini 2.5 Flash**. A aplicação gerencia sessões independentes, garantindo que o histórico de conversa de um usuário não interfira no de outro.

## 🚀 Tecnologias Utilizadas
* **Backend:** Python 3, FastAPI, Uvicorn, Pydantic.
* **Inteligência Artificial:** Novo SDK `google-genai` (Modelo Gemini 2.5 Flash).
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (Interface assíncrona com `fetch` e gerenciamento de estado via `sessionStorage`).
* **Infraestrutura:** Planejado para AWS EC2.

## 🏗️ Arquitetura do Sistema
O código foi desenhado aplicando *Separation of Concerns* (Separação de Responsabilidades), distribuído nos seguintes módulos:
* `main.py`: Inicialização e montagem da aplicação FastAPI e dos recursos estáticos (frontend).
* `routes.py`: Definição de endpoints REST, como o `POST /chat`.
* `session_manager.py`: Lógica para criação e gerenciamento de UUIDs únicos por sessão e isolamento em memória do histórico de cada usuário.
* `llm_service.py`: Lógica isolada de comunicação e integração com a API do Google Generative AI.
* `static/index.html`: Toda a parte visual (UI moderna do chatbot).
* `.env`: Arquivo de variáveis de ambiente (contendo a chave secreta da API).

## ⚙️ Como rodar o projeto localmente

Siga o passo a passo abaixo para rodar o projeto na sua máquina:

**1. Clone o repositório (ou baixe os arquivos)**
```bash
git clone <URL_DE_STE_REPOSITORIO>
cd chatbot_project
```

**2. Crie um Ambiente Virtual (Opcional, mas recomendado)**
```bash
python -m venv venv

# Para ativar no Windows:
venv\Scripts\activate

# Para ativar no Linux/Mac:
source venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Configure sua chave da API do Google**
Crie um arquivo chamado `.env` na raiz do projeto (se ainda não existir) e insira sua chave do [Google AI Studio](https://aistudio.google.com/):
```env
GOOGLE_API_KEY=sua_chave_secreta_aqui
```

**5. Execute o servidor**
```bash
uvicorn main:app --reload
```

**6. Acesse no Navegador**
Abra o seu navegador e acesse: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## ☁️ Implantação na AWS (Entrega Final)
Para instruções sobre como publicar essa aplicação em um servidor público EC2 na AWS para a apresentação, consulte o arquivo interno `instrucoes_ec2.md`.
