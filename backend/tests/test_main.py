from fastapi.testclient import TestClient
from app.main import app
from app.core.graph import Graph

# Cria um cliente simulado para "conversar" com a API
client = TestClient(app)

# --- TESTES UNITÁRIOS (Testam a lógica pura) ---

def test_graph_loading():
    """Testa se o grafo carrega corretamente a partir da string da matriz"""
    graph = Graph()
    # Matriz A->B (peso 10)
    matrix = "0,10; 10,0" 
    graph.load_from_matrix(matrix)
    
    # Verifica se criou 2 nós (A e B)
    assert len(graph.G.nodes) == 2
    # Verifica se existe aresta entre A e B com peso 10
    assert graph.G["A"]["B"]["weight"] == 10

def test_dijkstra_logic_simple():
    """Testa um caminho óbvio A -> B -> C"""
    graph = Graph()
    # A->B(1), B->C(2), A->C(100 - caminho ruim)
    # Matriz: 
    #   A  B  C
    # A 0  1  100
    # B 1  0  2
    # C 100 2 0
    matrix = "0,1,100; 1,0,2; 100,2,0"
    graph.load_from_matrix(matrix)
    
    path, dist = graph.shortest_path("A", "C")
    
    assert path == ["A", "B", "C"] # O caminho deve passar por B
    assert dist == 3               # 1 + 2 = 3

def test_dijkstra_no_path():
    """Testa quando não há caminho possível"""
    graph = Graph()
    # A->B, C (isolado)
    matrix = "0,1,0; 1,0,0; 0,0,0"
    graph.load_from_matrix(matrix)
    
    path, dist = graph.shortest_path("A", "C")
    
    # Se não tem caminho, sua lógica retorna [], -1
    assert path == []
    assert dist == -1

# --- TESTES DE INTEGRAÇÃO (Testam a API completa) ---

def test_api_calculate_route():
    """Testa o endpoint /calculate"""
    # 1. Configura o mapa via API
    client.post("/update-map", json={"matrix_text": "0,1,10; 1,0,1; 10,1,0"})
    
    # 2. Pede para calcular rota
    response = client.post("/calculate", json={"start": "A", "end": "C"})
    
    assert response.status_code == 200
    data = response.json()
    
    # Verifica a resposta
    assert data["result"]["path"] == ["A", "B", "C"]
    assert data["result"]["distance"] == 2
    # Verifica se a imagem foi gerada
    assert "data:image/png;base64" in data["graph"]["image"]

def test_api_random_map():
    """Testa se o endpoint random gera um grafo válido"""
    response = client.post("/random-map")
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "ok"
    assert len(data["graph"]["nodes"]) > 0
    assert len(data["graph"]["matrix"]) > 0