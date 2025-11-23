import heapq
import random as rnd
import strind as str
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict


class Graph:
    def __init__(self):
        self.G = nx.Graph()## grafo vazio
        self.node_list = [] ## lista de tuplas (u,v,peso)
        
        
    def dijkstra(self, start, end): # melhoria ---- all_nodes = set(self.G.nodes) precisa receber node_list antes para preencher o grafo
        all_nodes = set(self.G.nodes)
        distances = {node: float('inf') for node in all_nodes}
        distances[start] = 0
        queue = [(0, start)]
        previous_nodes = {}

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_distance > distances[current_node]:
                continue

            if current_node == end:
                break

            for neighbor in self.G.neighbors(current_node):
                weight = self.G[current_node][neighbor]['weight']
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))

        path = []
        node = end
        while node != start:
            path.append(node)
            node = previous_nodes[node]
        path.append(start)
        path.reverse()

        return distances[end], path
    
    def insert_random_edges(self):
        letras = str.ascii_uppercase
        for _ in range(1,7):
            if len(self.node_list) == 0:
                self.node_list.append((rnd.choice(letras), rnd.choice(letras), rnd.randint(1,10)))
                self.G.add_weighted_edges_from(self.node_list)
            else:
                self.node_list.append(((self.node_list[-1][1]), rnd.choice(letras), rnd.randint(1,10)))
                self.G.add_weighted_edges_from(self.node_list)
        return self.node_list
    
    def manual_insert_edges(self, edges):
        self.node_list.append(((self.node_list[-1][1]), edges, rnd.randint(1,25)))
        self.G.add_edge(self.node_list)
        return self.node_list