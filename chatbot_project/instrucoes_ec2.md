# Instruções de Implantação na AWS EC2

Siga estes passos para colocar o servidor do chatbot online e acessível publicamente via EC2 para a apresentação do seu trabalho (Tópicos em Computação Aplicada).

## Passo 1: Configurar a Instância e Portas (Security Groups)
1. No console da AWS EC2, inicie uma nova instância (ex: **Ubuntu Server** ou **Amazon Linux**).
2. Na aba de **Security Groups** (Configurações de Rede), adicione uma Regra de Entrada (Inbound Rule) permitindo **TCP Personalizado na porta 8000** (porta utilizada pelo FastAPI) para **Qualquer IPv4 (0.0.0.0/0)**.
3. Certifique-se de que a porta SSH (22) está liberada apenas para o seu IP.
4. Faça o download da sua chave `.pem`.

## Passo 2: Conectar ao Servidor e Clonar o Projeto
1. Acesse o servidor via SSH:
   ```bash
   ssh -i sua-chave.pem ubuntu@IP_PUBLICO_DA_EC2
   ```
2. Instale as ferramentas necessárias caso não as possua nativamente:
   ```bash
   sudo apt update
   sudo apt install git python3-pip python3-venv -y
   ```
3. Clone o seu repositório Github (como exigido nas observações do projeto):
   ```bash
   git clone <LINK_DO_SEU_GITHUB> chatbot_project
   cd chatbot_project
   ```

## Passo 3: Configurar as Dependências Python
Para não gerar conflitos, isole as dependências deste projeto:
```bash
# Cria o ambiente virtual
python3 -m venv venv

# Ativa o ambiente virtual
source venv/bin/activate

# Instala o FastAPI, Uvicorn, Google Gemini, Pydantic, etc.
pip install -r requirements.txt
```

## Passo 4: Chave do Google Generative AI
A inteligência artificial depende da sua chave da API. Configure isso nas variáveis de ambiente do Ubuntu antes de inicializar o servidor:
```bash
export GOOGLE_API_KEY="cole_sua_chave_do_google_ai_studio_aqui"
```

## Passo 5: Rodar a Aplicação com Acesso Público
Para ligar o Uvicorn permitindo tráfego da internet, execute:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

> **Dica de Produção:** Se quiser que a aplicação rode em segundo plano (mesmo se você fechar a janela do terminal SSH), utilize:
> ```bash
> nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
> ```

## Acesso Final
Agora basta acessar no seu navegador:
**`http://IP_PUBLICO_DA_EC2:8000/`**

Com isso, o requisito de acessibilidade pública via internet está atendido para a sua avaliação presencial!
