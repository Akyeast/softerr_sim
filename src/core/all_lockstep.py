import math
from core.utils import argmin

def get_num_core_LS(task_set):
    """
        Input: [(period, execution, critical), (5, 3, 1), ...]
        Output: minimum number of core under lockstep
    """
    utilization = 0.0
    for task in task_set:
        utilization += task[1] / task[0]

    min_core = math.ceil(utilization)
    scheduable = False

    while not scheduable:
        scheduable = check_schedulability(task_set, min_core)
        min_core += 1

    return min_core * 2

def check_schedulability(task_set, num_core):
    """
        Input: [(period, execution, critical), (5, 3, 1), ...]
        Output: True if schedulable, False otherwise
    """
    allocated = [0.0 for _ in range(num_core)]

    for task in task_set:
        index = argmin(allocated)
        allocated[index] += task[1] / task[0]
        if (allocated[index] > 1.0):
            return False
    else :
        return True