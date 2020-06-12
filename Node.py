from scipy.spatial import distance
import Parameter as para
import math
from Node_Method import to_string, find_receiver


class Node:
    def __init__(self, location=None, com_ran=None, sen_ran=None, energy=None, prob=para.prob, avg_energy=None,
                 len_cp=10, id=None, is_active=True, energy_max=None):
        self.location = location  # location of sensor
        self.com_ran = com_ran  # communication range
        self.sen_ran = sen_ran  # sensing range
        self.energy = energy  # energy of sensor
        self.energy_max = energy_max  # capacity of sensor
        self.prob = prob  # probability of sending data
        self.check_point = [{"e_avg": 0, "time": 0, "used_e": 0.0}]  # check point of information of sensor
        self.used_energy = 0.0  # energy was used
        self.avg_energy = avg_energy  # average energy of sensor
        self.len_cp = len_cp  # length of check point list
        self.id = id  # identify of sensor
        self.neighbor = []  # neighborhood of sensor
        self.is_active = is_active  # statement of sensor. If sensor dead, state is False

    def set_average_energy(self, func=None):
        """
        calculate average energy of sensor
        :param func: function to calculate
        :return: set value for average energy with estimate function is func
        """
        self.avg_energy = func()

    @staticmethod
    def estimate_average_energy(node):
        """
        function to estimate average energy
        user can replace with other function
        :return: a scalar which is calculated from check point list
        """
        return (node.check_point[-2]["used_e"] * node.check_point[-2]["time"] - node.check_point[-1]["used_e"] *
                node.check_point[-1]["time"]) / (
                       node.check_point[-2]["time"] + node.check_point[-1]["time"])

    def set_check_point(self, t):
        """
        add new check point in check_point list
        :param t: time stem
        :return: if queue of check point is not full, add new check point
        """
        if len(self.check_point) >= self.len_cp:
            self.check_point.pop(0)
        self.check_point.append(
            {"E_current": self.energy, "time": t, "used_e": self.used_energy / (t - self.check_point[-1]["time"])})
        self.used_energy = 0.0

    def charge(self, mc):
        """
        charging to sensor
        :param mc: mobile charger
        :return: if mc is standing and sensor is not full, sensor will charge
        """
        if self.energy <= self.energy_max - 10 ** -5 and mc.is_stand:
            d = distance.euclidean(self.location, mc.location)
            p = para.alpha / (d + para.beta) ** 2
            self.energy = min(self.energy_max, self.energy + p)

    def send(self, net, package, receiver=find_receiver, is_energy_info=False):
        """
        send package
        :param package:
        :param net: the network
        :param receiver: the function calculate receiver node
        :param is_energy_info: if this package is energy package, is_energy_info will be true
        :return: send package to the next node and reduce energy of this node
        """
        d0 = math.sqrt(para.EFS / para.EMP)
        package.update_path(self.id)
        if not self.is_active:
            pass
        elif distance.euclidean(self.location, para.base) > self.com_ran:
            receiver_id = receiver(self, net, package)
            if receiver_id != -1:
                d = distance.euclidean(self.location, net.node[receiver_id].location)
                e_send = para.ET + para.EFS * d ** 2 if d <= d0 else para.ET + para.EMP * d ** 4
                self.energy -= e_send * package.size
                self.used_energy += e_send * package.size
                net.node[receiver_id].receive(net, package)
                net.node[receiver_id].send(net, package, receiver, is_energy_info)
                self.check_active(net)
            else:
                pass
        else:
            d = distance.euclidean(self.location, para.base)
            e_send = para.ET + para.EFS * d ** 2 if d <= d0 else para.ET + para.EMP * d ** 4
            self.energy -= e_send * package.size
            self.used_energy += e_send * package.size
            self.check_active(net, )

    def receive(self, net, package):
        """
        receive package from other node
        :param net: the network
        :param package: size of package
        :return: reduce energy of this node
        """
        self.energy -= para.ER * package.size
        self.used_energy += para.ER * package.size
        self.check_active(net)

    def check_active(self, net):
        if self.energy < 0 or len(self.neighbor) == 0:
            self.is_active = False
        else:
            a = [1 for neighbor in self.neighbor if net.node[neighbor].is_active]
            self.is_active = True if len(a) > 0 else False

    def print_node(self, func=to_string):
        func(self)
