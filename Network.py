from scipy.spatial import distance
from Network_Method import uniform_com_func, to_string


class Network:
    def __init__(self, list_node=None):
        self.node = list_node
        self.set_neighbor()

    def set_neighbor(self):
        for node in self.node:
            for other in self.node:
                if other.id != node.id and distance.euclidean(node.location, other.location) <= node.com_ran:
                    node.neighbor.append(other.id)

    def communicate(self, func=uniform_com_func):
        func(self)

    def print_net(self, func=to_string):
        func(self)
