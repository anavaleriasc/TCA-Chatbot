from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware
from api.router import api_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Inicializa o FastAPI
app = FastAPI(title="Chatbot Multiusuário com Gemini")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"], # Isso permite o OPTIONS, POST, GET, etc.
    allow_headers=["*"],
)

# Registra os roteadores definidos no arquivo routes.py
#app.include_router(router)
app.include_router(api_router)

# Garantindo que a pasta static exista caso seja rodado num local vazio
os.makedirs(STATIC_DIR, exist_ok=True)

# Monta a pasta 'static' para servir o Frontend web (HTML, CSS, JS) na raiz ("/")
# A opção html=True faz com que ao acessar a raiz ele busque automaticamente o index.html
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # Na AWS EC2, host='0.0.0.0' é necessário para expor publicamente na rede
    # reload=False para produção. Deixei True para facilitar o desenvolvimento local
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
