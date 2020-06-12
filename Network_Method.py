import random
from Package import Package


def uniform_com_func(net):
    for node in net.node:
        r = random.random()
        if r <= node.prob:
            package = Package()
            node.send(net, package)


def to_string(net):
    min_energy = 10 ** 10
    min_node = -1
    for node in net.node:
        if node.energy < min_energy:
            min_energy = node.energy
            min_node = node
    min_node.print_node()