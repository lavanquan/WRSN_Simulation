from scipy.spatial import distance
from Network_Method import uniform_com_func, to_string


class Network:
    def __init__(self, list_node=None, mc=None, target=None):
        self.node = list_node
        self.set_neighbor()
        self.mc = mc
        self.target = target

    def set_neighbor(self):
        for node in self.node:
            for other in self.node:
                if other.id != node.id and distance.euclidean(node.location, other.location) <= node.com_ran:
                    node.neighbor.append(other.id)

    def communicate(self, func=uniform_com_func):
        return func(self)

    def run_per_second(self, t, q_learning):
        state = self.communicate()
        for node in self.node:
            if node.energy < node.energy_thresh:
                node.request(mc=self.mc, t=t)
            else:
                node.is_request = False
        self.mc.run(network=self, time_stem=t, net=self, q_learning=q_learning)
        return state

    def simulate(self, q_learning):
        t = 0
        while self.find_min_node()[1] >= 0:
            t = t + 1
            print(t, self.mc.current, self.find_min_node())
            state = self.run_per_second(t, q_learning)
            if not state:
                break

    def print_net(self, func=to_string):
        func(self)

    def find_min_node(self):
        min_energy = 10**10
        min_id = -1
        for node in self.node:
            if node.energy < min_energy:
                min_energy = node.energy
                min_id = node.id
        return min_id, min_energy, self.node[min_id].location