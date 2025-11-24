
import random as rnd
import string as str
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict


class Graph:
    def __init__(self):
        self.G = nx.Graph()## grafo vazio
        self.node_list = [self.G.edges] ## lista de tuplas (u,v,peso)
        self.adj = defaultdict(self.G.adj) ## dicionario de adjacencia
        
    def shortest_path(self,start, end):
        route = nx.dijkstra_path(self.G, start, end, weight='weight')
        weigth = nx.dijkstra_path_length(self.G, start, end, weight='weight')
        return route, weigth
    
    def random_edges(self,G):
        edges = []

        # Se o grafo não tem nós, cria dois
        if len(self.G.nodes) < 1:
            a = rnd.choice(str.ascii_uppercase)
            b = rnd.choice(str.ascii_uppercase)
            if a == b:
                b = rnd.choice(str.ascii_uppercase)
            w = rnd.randint(1, 30)
            edges.append((a, b, {'weight': w}))

        # Agora gera várias novas arestas
        for _ in range(rnd.randint(5, 10)):
            a = edges[-1][1]
            b = rnd.choice(str.ascii_uppercase)
            if a == b:
                b = rnd.choice(str.ascii_uppercase)
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
        return self.G.edges(data=True)
    def add_edges(self, edges):
        self.node_list.append(((self.node_list[-1][1]), edges, rnd.randint(1,25)))
        self.G.add_edge(self.node_list)
        return self.G.edges(data=True)