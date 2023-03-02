from core.utils import argmin

def critical2core(tasks, num_core):
    """
        Input: 
            critical tasks
            [(period, execution, critical), (5, 3, 1), ...] 
        Output: (
                [{task1, assignedCore}, {task2, assignedCore}, ... ], 
                [core1_util, core2_util, ...]
            )
    """
    # assign tasks to cores
    mapped_tasks = []
    assigned_cores = [0.0 for _ in range(int(num_core))]
    max_util = [0.0 for _ in range(int(num_core))]

    for task in tasks:
        index = argmin(assigned_cores)
        mapped_tasks.append((*task, index))
        assigned_cores[index] += task[1] / task[0]
        if task[1] / task[0] > max_util[index]:
            max_util[index] = task[1] / task[0]

    return mapped_tasks, assigned_cores, max_util