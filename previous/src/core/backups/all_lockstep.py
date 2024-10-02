import math
from core.utils import argmin
from core.rta import rta_all, rta_all_single

def get_num_core_LS(task_set, method='rta_single'):
    """
        Input: [(period, execution, critical), (5, 3, 1), ...], method = 'deadline' or 'rta'
        Output: minimum number of core under lockstep
    """
    utilization = 0.0
    for task in task_set:
        utilization += task[1] / task[0]

    min_core = math.ceil(utilization)
    scheduable = False

    while not scheduable:
        scheduable, allocated_tasks = check_schedulability(task_set, min_core, method=method)
        if not scheduable:
            min_core += 1

    return min_core * 2, allocated_tasks

def check_schedulability(task_set, num_core, method):
    """
        Input: [(period, execution, critical), (5, 3, 1), ...]
        Output: True if schedulable, False otherwise
    """

    if method == 'deadline':
        return check_schedulability_deadline(task_set, num_core)
    elif method == 'rta':
        return check_schedulability_rta(task_set, num_core)
    elif method == 'rta_single':
        return check_schedulability_rta_single(task_set, num_core)
    else:
        raise NotImplementedError


def check_schedulability_deadline(task_set, num_core):
    allocated_core = [0.0 for _ in range(num_core)]
    allocated_task = [[] for _ in range(num_core)]

    for task in task_set:
        index = argmin(allocated_core)
        allocated_core[index] += task[1] / (task[0] - task[1])
        allocated_task[index].append(task)
        if (allocated_core[index] > 1.0):
            return False, None
    else :
        return True, allocated_task

def check_schedulability_rta(task_set, num_core):
    # no exact allocated task in this method
    return rta_all(task_set, num_core, fault=True), None

def check_schedulability_rta_single(task_set, num_core):
    allocated_core = [[] for _ in range(num_core)]
    allocated_util = [0.0 for _ in range(num_core)]

    for task in task_set:
        index = argmin(allocated_util)
        allocated_util[index] += task[1] / task[0]
        allocated_core[index].append(task)

    for core in allocated_core:
        if not rta_all_single(core, fault=True):
            return False, None
    else :
        return True, allocated_core