from fastapi import APIRouter
from app.core.graph import Graph
from app.core.schemas import MatrixInput, RouteInput
import random

router = APIRouter()

#----------------------------------instância global do Grafo
graph_instance = Graph()

#------------------------------------------------mapa inicial padrão
default_matrix = "0,5,0,0; 0,0,2,0; 0,0,0,3; 1,0,0,0"

graph_instance.load_from_matrix(default_matrix)

#----------------------------------------------------endpoints
@router.get("/graph")
def get_graph():
    return graph_instance.to_dict()

@router.post("/update-map")
def update_map(data: MatrixInput):
    try:
        graph_instance.load_from_matrix(data.matrix_text)
        return {"status": "ok", "graph": graph_instance.to_dict()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@router.post("/calculate")
def calculate_route(data: RouteInput):
    return graph_instance.get_shortest_path(data.start, data.end)

@router.post("/random-map")
def generate_random_map():
    size = random.randint(3, 6)
    matrix_rows = []

    for r in range(size):
        row = []
        for c in range(size):
            if r == c:
                row.append(0)
            else:
                weight = 0 if random.random() < 0.5 else random.randint(1, 9)
                row.append(weight)
        matrix_rows.append(",".join(map(str, row)))

    matrix_text = ";".join(matrix_rows)
    graph_instance.load_from_matrix(matrix_text)

    return {"status": "ok", "graph": graph_instance.to_dict()}