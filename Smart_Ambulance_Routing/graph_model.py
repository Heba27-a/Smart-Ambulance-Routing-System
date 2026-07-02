import json
import math
import networkx as nx

class CityGraph:
    def __init__(self):
        self.G = nx.Graph()
        self.positions = {}  # {node: (x,y)} للرسم ولحساب المسافة الهوائية

    def load_from_json(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for node in data['nodes']:
            self.G.add_node(node['id'], label=node.get('label', node['id']))
            self.positions[node['id']] = (node['x'], node['y'])

        for edge in data['edges']:
            # edge: {u, v, distance, traffic, closed}
            self.G.add_edge(
                edge['u'], edge['v'],
                distance=edge['distance'],
                traffic=edge.get('traffic', 0.0),
                closed=edge.get('closed', False)
            )

    def neighbors(self, node):
        return self.G.neighbors(node)

    def is_closed(self, u, v):
        return self.G.edges[u, v].get('closed', False)

    def edge_cost(self, u, v):
        attrs = self.G.edges[u, v]
        return attrs['distance'] * (1.0 + attrs.get('traffic', 0.0))

    def heuristic(self, a, b):
        # مسافة إقليدية بين نقطتين
        ax, ay = self.positions[a]
        bx, by = self.positions[b]
        dx = ax - bx
        dy = ay - by
        return math.sqrt(dx*dx + dy*dy)