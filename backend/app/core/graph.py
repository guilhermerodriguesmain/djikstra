
import random as rnd
import string 
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple

class Graph:
    def __init__(self):
        self.G = nx.Graph()## grafo vazio
        self.edges_list = []
    def shortest_path(self,start, end):
        route = nx.dijkstra_path(self.G, start, end, weight='weight')
        weigth = nx.dijkstra_path_length(self.G, start, end, weight='weight')
        return route, weigth
    
    def random_edges(self):
        edges = []

        # Se o grafo não tem nós, cria dois
        if len(self.G.nodes) < 1:
            a = rnd.choice(string.ascii_uppercase)
            b = rnd.choice(string.ascii_uppercase)
            if a == b:
                b = rnd.choice(string.ascii_uppercase)
            w = rnd.randint(1, 30)
            edges.append((a, b, {'weight': w}))

        # Agora gera várias novas arestas
        for _ in range(rnd.randint(5, 10)):
            a = edges[-1][1]
            b = rnd.choice(string.ascii_uppercase)
            if a == b:
                b = rnd.choice(string.ascii_uppercase)
            w = rnd.randint(1, 30)
            edges.append((a, b, {'weight': w}))
            
        # adiciona arestas entre nós já existentes   
            c = edges[-1][1]
            d = edges[rnd.randint(0, len(edges)-2)][1]
            if a == b:
                edges[rnd.randint(0, len(edges)-3)][1]
            w = rnd.randint(1, 30)
            edges.append((c, d, {'weight': w}))

        self.G.add_edges_from(edges)
        self.edges_list.extend(edges)
        return self.G.edges(data=True)
    
    def add_edges(self, edges):
        self.edges_list.append(((self.edges_list[-1][1]), edges, rnd.randint(1,25)))
        self.G.add_edge(self.edges_list)
        return list(self.G.edges(data=True))
    
    def get_nodes(self) -> List[str]:
        return list(self.G.nodes)

    def get_edges(self) -> List[Dict]:
        return [{"u": u, "v": v, "w": data.get("weight")} for u, v, data in self.G.edges(data=True)]