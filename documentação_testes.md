# Documentação de Testes Unitários: Rotas da API

Este documento detalha a suíte de testes unitários desenvolvida para a camada de rotas (`routers`) do backend da aplicação FastAPI. 

## Objetivo
O foco dos testes é validar as **respostas HTTP, validações do Pydantic e a integração com as dependências do FastAPI** (rotas de API), garantindo que os endpoints funcionem conforme o esperado em diversas situações. 

Como a arquitetura isola bem a lógica na camada de `services`, utilizamos a técnica de **Mocking** (através da biblioteca `unittest.mock`) para simular as respostas dos serviços e do banco de dados, o que resulta em testes super rápidos que não dependem do Postgres ou de requisições de rede.

## Estrutura de Diretórios
```text
app/tests/
├── __init__.py
├── conftest.py                # Configurações globais do pytest (Fixtures e Overrides)
├── test_auth_router.py        # Testes de autenticação e login
├── test_chat_router.py        # Testes de invocação do Chatbot
├── test_messages_router.py    # Testes de consulta de mensagens
├── test_session_router.py     # Testes de consulta de sessões
└── test_user_router.py        # Testes do CRUD de usuários
```

## Ferramentas e Bibliotecas Utilizadas
- **`pytest`**: Framework de testes em Python.
- **`pytest-asyncio`**: Plugin para permitir o teste de funções assíncronas (async/await).
- **`httpx`**: Utilizado para fornecer um `AsyncClient`, criando um ambiente de cliente HTTP em memória para interagir com o FastAPI durante os testes.
- **`pytest-mock` e `unittest.mock`**: Para realizar o `patch` e criar `AsyncMocks` das funções injetadas.

---

## Configurações Essenciais (`conftest.py`)
O arquivo base da suíte de testes implementa:
1. **Bypass de Chaves de API**: A injeção inicial de variáveis de ambiente simuladas (como `GOOGLE_API_KEY`) para evitar problemas de importação durante o carregamento dos pacotes da Google / LangChain.
2. **Database Override**: A dependência `get_db` global do FastAPI é substituída para retornar um `AsyncMock()` invés de uma sessão de banco real.
3. **Fixture do AsyncClient**: Disponibiliza o `async_client` como argumento para qualquer teste, já conectando ao módulo principal `app.main:app`.

---

## Casos de Teste (Routers)

### 1. `test_user_router.py` (5 Testes)
Testa o CRUD de Usuários através da rota `/usuarios`.
- **`test_create_user`**: Valida a resposta do endpoint `POST /usuarios` verificando se devolve status `201` e um token simulado de sucesso.
- **`test_list_users`**: Valida o retorno do `GET /usuarios` com uma lista contendo múltiplos objetos `UserPublic`.
- **`test_get_user`**: Valida o retorno específico via ID (`GET /usuarios/{id}`).
- **`test_update_user`**: Garante que o retorno do `PATCH /usuarios/{id}` devolve um JSON correspondente aos campos atualizados.
- **`test_delete_user`**: Valida a exclusão retornando o usuário apagado via `DELETE /usuarios/{id}`.

### 2. `test_auth_router.py` (3 Testes)
Testa o sistema de login via `POST /auth/login`.
- **`test_login_success`**: Garante o status `200` ao prover credenciais válidas e verifica se a resposta traz o token do usuário.
- **`test_login_wrong_email`**: Simula quando o repositório não encontra o e-mail informado (status `401`).
- **`test_login_wrong_password`**: Simula um erro na validação de hash e garante o status `401`.

### 3. `test_chat_router.py` (1 Teste)
Testa a rota de conversação do Chatbot via `POST /chat/invoke`.
- **`test_invoke_chat`**: Envia o payload no formato `ChatRequest` (com `user_id`, `message` e `thread_id`) e verifica se a resposta em Mock contém os dados aguardados (`interaction_type`, `model`, etc).

### 4. `test_session_router.py` (2 Testes)
Testa as rotas de histórico de seções do usuário.
- **`test_list_sessions`**: Valida que uma coleção de `SessionPublic` simulada reflete corretamente um JSON listado em `GET /seções`.
- **`test_get_sessions_by_thread`**: Checa o retorno de uma sessão específica baseada no UUID da Thread (`GET /seções/{thread_id}`).

### 5. `test_messages_router.py` (2 Testes)
Testa as rotas de recuperação de mensagens (`MessagePublic`).
- **`test_list_messages`**: Valida se as roles ("user" e "bot") e o conteúdo da conversa inteira são parseados corretamente ao invocar `GET /mensagens`.
- **`test_list_message_by_thread`**: Testa a busca das mensagens filtradas para uma única Thread simulando o `GET /mensagens/{thread_id}`.

---

## Como Rodar os Testes

Para garantir que a aplicação segue íntegra após futuras alterações no código, basta executar o seguinte comando a partir da **raiz do projeto** (`TCA-Chatbot-ana-task008`):

```bash
pytest app/tests
```

**Saída Esperada:**
```text
============================= test session starts =============================
collected 13 items

app\tests\test_auth_router.py ...                                        [ 23%]
app\tests\test_chat_router.py .                                          [ 30%]
app\tests\test_messages_router.py ..                                     [ 46%]
app\tests\test_session_router.py ..                                      [ 61%]
app\tests\test_user_router.py .....                                      [100%]

============================== 13 passed in 0.5s ==============================
```
