# implementa classe Grafo nao direcionado e ponderado
'''
usa as seguintes bibliotecas:
networkx
matplotlib.pyplot

métodos: 
'''

import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    G = nx.Graph()
    grafo ={
        
    }
    def adicionar_no(self, no):
        self.G.add_node(no)
        
    def adicionar_nos(self, lista_nos):
        self.G.add_nodes_from(lista_nos)
        
    def adicionar_arestas(self, a, b, peso):
        self.G.add_edge(a,b, weight=peso)
        
    