import math
from core.utils import argmin
from prm.demand import Demand
from prm.supply import sbf, lsbf

def assign_nc2PRM(prm_bounds, tasks):
    """
        Input:
            prms: [prm1_max_util, prm2_max_util, ...]
            tasks: [(period, execution, critical), (5, 3, 0), ...]
        Output:
            prms: [core1_util, core2_util, ...]
            tasks: [(period, execution, critical, index), (5, 3, 0, 1), ...]
    """
    prms = [[] for _ in range(len(prm_bounds))] # assigned NC
    mapped_tasks = []

    for task in tasks:
        indexs = argmin(prms, array=True)
        for index in indexs :
            groups = prms[index] + [task]

            ## schedulability check
            demand = Demand(groups)
            pi = min([task[0] for task in groups])
            theta = get_optimal_theta(pi, demand)
            print("PRM parameter: ", pi, theta, prm_bounds[index])
            if theta / pi <= prm_bounds[index]:
                prms[index] = groups
                mapped_tasks.append((*task, index))
                break;
        else :
            # not schedulable
            mapped_tasks.append((*task, None))

    return prms, mapped_tasks

def get_minimum_theta(t, pi, dbf):
    return (math.sqrt((t-2*pi)**2 + 4*pi*dbf) - (t - 2*pi)) / 4

def get_optimal_theta(pi, demand):
    maximum_theta = 0
    for point in range(1, lcm([task[0] for task in demand.tasks])):
        for i in range(len(demand.tasks)):
            theta = get_minimum_theta(point, pi, demand.demand(point, i))
            if theta > maximum_theta:
                maximum_theta = theta
    return maximum_theta

def lcm(lst):
    _lcm = 1
    for i in lst:
        _lcm = _lcm*i // math.gcd(_lcm, i)
    return _lcm