# cria grafo e implementa algoritmo de Dijkstra

class Graph:
    def __init__(self, size):
        self.size = size # numero de vértices
        self.adj_matrix = [[0]* size for _ in range(size)] # adiciona todas as arestas e seus pesos
        self.vertex_data = ['']*size # nome dos vértices
        
    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight # grafo não direcionado
    
    def set_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data
                    