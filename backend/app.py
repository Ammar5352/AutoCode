from fastapi import FastAPI
from .AIAgents.app import app as autocode_router
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/serverhealth")
def server_health():
    return {"message": "PONG"}

app.include_router(autocode_router,prefix="/autocodeai")