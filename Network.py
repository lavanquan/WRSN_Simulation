import csv

from scipy.spatial import distance

import Parameter as para
from Network_Method import uniform_com_func, to_string, count_function


class Network:
    def __init__(self, list_node=None, mc=None, target=None):
        self.node = list_node
        self.set_neighbor()
        self.set_level()
        self.mc = mc
        self.target = target

    def set_neighbor(self):
        for node in self.node:
            for other in self.node:
                if other.id != node.id and distance.euclidean(node.location, other.location) <= node.com_ran:
                    node.neighbor.append(other.id)

    def set_level(self):
        queue = []
        for node in self.node:
            if distance.euclidean(node.location, para.base) < node.com_ran:
                node.level = 1
                queue.append(node.id)
        while queue:
            for neighbor_id in self.node[queue[0]].neighbor:
                if not self.node[neighbor_id].level:
                    self.node[neighbor_id].level = self.node[queue[0]].level + 1
                    queue.append(neighbor_id)
            queue.pop(0)

    def communicate(self, func=uniform_com_func):
        return func(self)

    def run_per_second(self, t, q_learning):
        state = self.communicate()
        request_id = []
        for index, node in enumerate(self.node):
            if node.energy < node.energy_thresh:
                node.request(mc=self.mc, t=t)
                request_id.append(index)
            else:
                node.is_request = False
        if request_id:
            for index, node in enumerate(self.node):
                if index not in request_id and (t - node.check_point[-1]["time"]) > 50:
                    node.set_check_point(t)
            # for node in self.node:
            #     print("avg_energy =", node.id, node.avg_energy,)
        self.mc.run(network=self, time_stem=t, net=self, q_learning=q_learning)
        return state

    def simulate(self, q_learning, file_name="log/energy_log.csv"):
        energy_log = open(file_name, "w")
        writer = csv.DictWriter(energy_log, fieldnames=["time", "mc energy", "min energy"])
        writer.writeheader()
        t = 0
        while self.node[self.find_min_node()].energy >= 0:
            t = t + 1
            print(t, self.mc.current, self.node[self.find_min_node()].energy)
            state = self.run_per_second(t, q_learning)
            if not (t - 1) % 100:
                writer.writerow(
                    {"time": t, "mc energy": self.mc.energy, "min energy": self.node[self.find_min_node()].energy})
            # if not state:
            #     break
        writer.writerow({"time": t, "mc energy": self.mc.energy, "min energy": self.node[self.find_min_node()].energy})
        energy_log.close()

    # def simulate(self, q_learning):
    #     t = 0
    #     while t < 20000:
    #         t += 1
    #         print(t, self.mc.current, self.find_min_node(), self.count_dead_node(), self.count_package())
    #         state = self.run_per_second(t, q_learning)
    #         if not state:
    #             break

    def print_net(self, func=to_string):
        func(self)

    def find_min_node(self):
        min_energy = 10 ** 10
        min_id = -1
        for node in self.node:
            if node.energy < min_energy:
                min_energy = node.energy
                min_id = node.id
        return min_id

    def count_dead_node(self):
        count = 0
        for node in self.node:
            if node.energy < 0:
                count += 1
        return count

    def count_package(self, count_func=count_function):
        count = count_func(self)
        return count
