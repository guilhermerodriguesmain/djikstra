import random as rnd
import string
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64

# Configura Matplotlib para rodar sem interface gráfica (Server mode)
plt.switch_backend('Agg')

class Graph:
    def __init__(self):
        self.G = nx.Graph() 
        self.edges_list = []

    def shortest_path(self, start, end):
        try:
            route = nx.dijkstra_path(self.G, start, end, weight='weight')
            length = nx.dijkstra_path_length(self.G, start, end, weight='weight')
            return route, length
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return [], -1

    def random_edges(self):
        self.clear() # Limpa o grafo anterior
        
        # Define um tamanho aleatório (ex: entre 4 e 7 nós)
        n_nodes = rnd.randint(4, 7)
        
        # Cria nomes SEQUENCIAIS: ['A', 'B', 'C', 'D', ...]
        nodes = [chr(65 + i) for i in range(n_nodes)]
        
        # Adiciona os nós ao grafo (para garantir que existam mesmo sem arestas)
        self.G.add_nodes_from(nodes)
        
        # Garante conexidade mínima (A liga com B, B liga com C...)
        # Isso evita que fiquem nós isolados no mapa
        for i in range(n_nodes - 1):
            w = rnd.randint(1, 30)
            self.G.add_edge(nodes[i], nodes[i+1], weight=w)
            
        # Adiciona arestas extras aleatórias para criar ciclos e atalhos
        # Tenta criar (n_nodes) conexões extras
        for _ in range(n_nodes):
            u = rnd.choice(nodes)
            v = rnd.choice(nodes)
            
            # Se não for o mesmo nó e a aresta ainda não existir
            if u != v and not self.G.has_edge(u, v):
                w = rnd.randint(1, 30)
                self.G.add_edge(u, v, weight=w)

        return self.G.edges(data=True)

    # -------------------------------------------------------------------- MÉTODOS DE SUPORTE (ADAPTADORES PARA O FRONTEND)

    def clear(self):
        self.G.clear()
        self.edges_list = []

    def load_from_matrix(self, matrix_text: str):
        """
        Lê a string da matriz do Frontend e preenche o NetworkX
        """
        self.clear()
        rows = [r.strip() for r in matrix_text.split(';') if r.strip()]
        size = len(rows)
        
        # Gera nós sequenciais A, B, C... baseados no tamanho da matriz
        node_names = [chr(65 + i) for i in range(size)]
        
        for i, row in enumerate(rows):
            cols = [int(x) for x in row.split(',')]
            for j, weight in enumerate(cols):
                if weight > 0:
                    # Adiciona aresta no NetworkX
                    self.G.add_edge(node_names[i], node_names[j], weight=weight)

    def generate_image_base64(self, highlight_path=None):
        """
        Gera a imagem usando Matplotlib + NetworkX
        """
        if self.G.number_of_nodes() == 0:
            return None

        # Cria figura
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Layout circular funciona bem para grafos pequenos
        pos = nx.circular_layout(self.G)

        # Desenha nós e arestas base
        nx.draw_networkx_nodes(self.G, pos, ax=ax, node_color='white', edgecolors='black', node_size=700)
        nx.draw_networkx_labels(self.G, pos, ax=ax, font_size=12, font_weight='bold')
        nx.draw_networkx_edges(self.G, pos, ax=ax, edge_color='black')
        
        # Desenha pesos
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, ax=ax)

        # Destaque do caminho (Vermelho)
        if highlight_path and len(highlight_path) > 1:
            # Converte lista de nós [A, B, C] em lista de arestas [(A,B), (B,C)]
            path_edges = list(zip(highlight_path, highlight_path[1:]))
            
            nx.draw_networkx_nodes(self.G, pos, nodelist=highlight_path, node_color='white', edgecolors='red', linewidths=2, node_size=700)
            nx.draw_networkx_edges(self.G, pos, edgelist=path_edges, edge_color='red', width=3)

        ax.axis('off')
        plt.tight_layout()

        # Salva em memória e converte para base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_b64}"

    def to_dict(self, path=None):
        """
        Formata os dados para o Frontend (incluindo recriar a matriz)
        """
        # Pega todos os nós ordenados (A, B, C...)
        nodes = sorted(list(self.G.nodes))
        size = len(nodes)
        
        # Reconstrói a matriz (List of Lists) para a tabela do frontend
        matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                u, v = nodes[i], nodes[j]
                # Verifica se existe aresta e pega o peso
                if self.G.has_edge(u, v):
                    row.append(self.G[u][v]['weight'])
                else:
                    row.append(0)
            matrix.append(row)

        return {
            "nodes": nodes,
            "edges": nx.to_dict_of_dicts(self.G), # Formato compatível
            "matrix": matrix,
            "image": self.generate_image_base64(path)
        }