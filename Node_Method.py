from scipy.spatial import distance
import Parameter as para
import numpy as np


def to_string(node):
    print("Id =", node.id, "Location =", node.location, "Energy =", node.energy, "ave_e =", node.avg_energy,
          "Neighbor =", node.neighbor)


def find_receiver(node, net, package):
    """
    find receiver node
    :param node: node send this package
    :param net: network
    :return: find node nearest base from neighbor of the node and return id of it
    """
    if not node.neighbor:
        return -1
    list_d = [distance.euclidean(para.base, net.node[neighbor_id].location) if net.node[
        neighbor_id].is_active else float("inf") for neighbor_id in node.neighbor]
    if not len(list_d):
        return -1
    id_min = np.argmin(list_d)
    if distance.euclidean(node.location, para.base) <= list_d[id_min]:
        return -1
    else:
        return node.neighbor[id_min]
