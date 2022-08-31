import math

def get_num_core_LS(task_set):
    """
        Input: [(period, execution, critical), (5, 3, 1), ...]
        Output: minimum number of core under lockstep
    """
    utilization = 0.0
    for task in task_set:
        utilization += task[1] / task[0]

    return math.ceil(utilization) * 2