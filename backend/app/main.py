# backend/app/main.py
from fastapi import FastAPI
from .api.router import router
from .core.graph import Graph
from contextlib import asynccontextmanager

app = FastAPI(title="Dijkstra API")
app.include_router(router)

@app.on_event("startup")
def startup_event():
    app.state.graph = Graph()

@app.get("/")
def root():
    return {"ok": True, "msg": "API online. Vá em /docs para ver os endpoints."}

