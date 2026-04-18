from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .AIAgents.app import app as autocode_router

app = FastAPI()

# Allow frontend dev server to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/serverhealth")
def server_health():
    return {"message": "PONG"}

app.include_router(autocode_router,prefix="/autocodeai")