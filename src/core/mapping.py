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

    for task in tasks:
        index = argmin(assigned_cores)
        mapped_tasks.append((*task, index))
        assigned_cores[index] += task[1] / task[0]

    #TODO: add schedulability check? is it needed?
    return mapped_tasks, assigned_cores