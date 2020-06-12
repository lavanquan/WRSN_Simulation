from Node import Node
import random
from Network import Network
list_node = []
for i in range(20):
    location = (random.random()*100, random.random()*100)
    com_ran = 20
    energy = 10
    energy_max = 10
    node = Node(location=location, com_ran=com_ran, energy=energy, energy_max=energy_max, id=i)
    list_node.append(node)
net = Network(list_node)
t = 0
while t < 100:
    t = t + 1
    net.communicate()
    net.node[0].print_node()
