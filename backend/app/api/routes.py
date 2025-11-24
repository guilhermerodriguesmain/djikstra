from fastapi import APIRouter
from app.core.graph import Graph
from app.core.schemas import MatrixInput, RouteInput

router = APIRouter()

#---------------------------------- Instância Global do Grafo
graph_instance = Graph()

#------------------------------------------------- Inicializa com um mapa simples para não começar vazio
try:
    graph_instance.load_from_matrix("0,5,0; 5,0,2; 0,2,0")
except:
    pass # Se der erro na inicialização, começa vazio sem quebrar

@router.get("/graph")
def get_graph():
    # Retorna o grafo atual e a imagem (sem destaque de rota)
    return graph_instance.to_dict(path=None)

@router.post("/update-map")
def update_map(data: MatrixInput):
    try:
        # Lê a matriz de texto e recria o grafo NetworkX
        graph_instance.load_from_matrix(data.matrix_text)
        return {"status": "ok", "graph": graph_instance.to_dict(path=None)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/calculate")
def calculate_route(data: RouteInput):
    # O método do seu colega retorna uma TUPLA: ([lista_nos], distancia)
    path, distance = graph_instance.shortest_path(data.start, data.end)
    
    # Prepara o objeto de resultado para o frontend
    result = {
        "path": path,
        "distance": distance
    }
    
    # Define o que será pintado de vermelho na imagem
    # Se a distância for -1 (sem caminho), não destaca nada
    path_to_highlight = path if distance != -1 else None
    
    # Retorna o resultado numérico E o grafo atualizado com a nova imagem pintada
    return {
        "result": result,
        "graph": graph_instance.to_dict(path=path_to_highlight)
    }

@router.post("/random-map")
def generate_random_map():
    # Gerar arestas aleatórias
    graph_instance.random_edges()
    return {"status": "ok", "graph": graph_instance.to_dict(path=None)}