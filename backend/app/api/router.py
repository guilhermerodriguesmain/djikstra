from fastapi import APIRouter
from ..core.graph import Graph
from pydantic import BaseModel

router = APIRouter()
graph = Graph()

@router.post("/core/graph/{node}")  # endpoint para inserir arestas manualmente
def manual_insert_edges(node):
    graph.manual_insert_edges(node) 
    return graph.nodes

@router.get("/core/graph")  # endpoint para inserir arestas aleatoriamente
def insert_random_edges():
    edges = graph.insert_random_edges() 
    return graph.nodes

@router.post("/core/grph/{inicio}/{fim}")  # endpoint para calcular o menor caminho
def shortest_path(inicio: str, fim: str):
    distance, path = graph.dijkstra(inicio, fim)
    return {"distance": distance, "path": path}