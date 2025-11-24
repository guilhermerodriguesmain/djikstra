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
        # Lógica do seu colega: Usar NetworkX
        self.G = nx.Graph() 
        self.edges_list = []

    def shortest_path(self, start, end):
        # Lógica do seu colega
        try:
            route = nx.dijkstra_path(self.G, start, end, weight='weight')
            # Correção: 'weight' (inglês correto)
            length = nx.dijkstra_path_length(self.G, start, end, weight='weight')
            return route, length
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return [], -1

    def random_edges(self):
        # Lógica do seu colega (adaptada para limpar o grafo antes, se quiser um novo)
        self.clear() # Limpa para gerar um novo mapa limpo
        
        edges = []
        # Garante nós iniciais
        if len(self.G.nodes) < 1:
            # Usa letras maiúsculas aleatórias
            nodes_pool = string.ascii_uppercase[:10] # Limita a A-J para não ficar gigante
            a = rnd.choice(nodes_pool)
            b = rnd.choice(nodes_pool)
            while a == b: # Garante que não é laço
                b = rnd.choice(nodes_pool)
            w = rnd.randint(1, 30)
            edges.append((a, b, {'weight': w}))

        # Gera novas arestas
        for _ in range(rnd.randint(4, 8)):
            if not edges: break
            
            # Pega um nó existente para garantir conexidade
            a = edges[-1][0] 
            b = rnd.choice(string.ascii_uppercase[:10])
            if a != b:
                w = rnd.randint(1, 30)
                edges.append((a, b, {'weight': w}))
        
        self.G.add_edges_from(edges)
        self.edges_list.extend(edges)
        return self.G.edges(data=True)

    # --- MÉTODOS DE SUPORTE (ADAPTADORES PARA O FRONTEND) ---

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