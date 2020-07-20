import random
from Package import Package


def uniform_com_func(net):
    for node in net.node:
        if node.id in net.target and random.random() <= node.prob and node.is_active:
            package = Package()
            node.send(net, package)
    return True


def to_string(net):
    min_energy = 10 ** 10
    min_node = -1
    for node in net.node:
        if node.energy < min_energy:
            min_energy = node.energy
            min_node = node
    min_node.print_node()
