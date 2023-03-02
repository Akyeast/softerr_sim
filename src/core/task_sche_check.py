import math
from core.utils import argmin, argmax
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
    prm_params = [None for _ in range(len(prm_bounds))] # PRM parameters (pi, theta)
    remain_utils = prm_bounds.copy()
    mapped_tasks = []

    for task in tasks:
        indexs = argmax(remain_utils, array=True)
        for index in indexs :
            groups = prms[index] + [task]

            ## schedulability check
            demand = Demand(groups)
            pi = int(min([(t[0]-t[1]) for t in groups])/2)
            theta = get_optimal_theta(pi, demand)
            # print("optimal parameters: {}, {}, {}\n\n\n".format(pi, theta, prm_bounds[index]))
            if theta / pi <= prm_bounds[index]:
                prms[index] = groups
                prm_params[index] = (pi, theta)
                remain_utils[index] -= task[1] / task[0]
                mapped_tasks.append((*task, index))
                break
        else :
            # not schedulable
            mapped_tasks.append((*task, None))

    return prm_params, mapped_tasks

def get_minimum_theta(t, pi, dbf):
    return (math.sqrt((t-2*pi)**2 + 4*pi*dbf) - (t - 2*pi)) / 4

def get_optimal_theta(pi, demand):
    maximum_theta = 0

    for i in range(len(demand.tasks)):
        for point in range(demand.tasks[i][0], lcm([task[0] for task in demand.tasks])+1):
            theta = get_minimum_theta(point, pi, demand.demand(point, i))
            if theta > maximum_theta:
                maximum_theta = theta

            # print(r'points {} and maximum A_k {} by theta {}'.format(point, demand.maximum_A_k(i, maximum_theta, pi), maximum_theta))
            if demand.maximum_A_k(i, maximum_theta, pi) <= point:
                break
    return maximum_theta

def lcm(lst):
    _lcm = 1
    for i in lst:
        _lcm = _lcm*i // math.gcd(_lcm, i)
    return _lcm

if __name__ == '__main__':
    tasks = [(10, 2, 0)]
    prm_bounds = [1.0]
    pi = 10
    prm_params, mapped_tasks = assign_nc2PRM(prm_bounds, tasks, pi)
    print(prm_params)
    print(mapped_tasks)
