from Node import Node
import random
from Network import Network
import pandas as pd
from ast import literal_eval
from MobileCharger import MobileCharger
from Q__Learning import Q_learning
from Inma import Inma

index = 0
df = pd.read_csv("data/thaydoitileguitin.csv")
node_pos = list(literal_eval(df.node_pos[index]))
list_node = []
for i in range(len(node_pos)):
    location = node_pos[i]
    com_ran = df.commRange[index]
    energy = df.energy[index]
    energy_max = df.energy[index]
    prob = df.freq[index]
    node = Node(location=location, com_ran=com_ran, energy=energy, energy_max=energy_max, id=i,
                energy_thresh=0.4 * energy, prob=prob)
    list_node.append(node)
mc = MobileCharger(energy=df.E_mc[index], capacity=df.E_max[index], e_move=df.e_move[index],
                   e_self_charge=df.e_mc[index], velocity=df.velocity[index])
target = [int(item) for item in df.target[index].split(',')]
net = Network(list_node=list_node,  mc=mc, target=target)
print(len(net.node), len(net.target), max(net.target))
q_learning = Q_learning(network=net)
inma = Inma()
net.simulate(q_learning=q_learning, max_time=20000, file_name="log/q_learning_information_log.csv")
