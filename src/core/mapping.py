import numpy as np

def critical2core(tasks, num_core):
    """
        Input: 
            [(period, execution, critical), (5, 3, 1), ...]
        Output: (
                [{task1, assignedCore}, {task2, assignedCore}, ... ], 
                [core1_util, core2_util, ...]
            )
    """
    # assign tasks to cores
    mapped_tasks = []
    assigned_cores = [0.0 for _ in range(num_core)]

    for task in tasks:
        if task[2] == 1:
            index = np.argmin(assigned_cores)
            mapped_tasks.append((*task, index))
            assigned_cores[index] += task[1] / task[0]
        else :
            mapped_tasks.append((*task, None))

    return mapped_tasks, assigned_cores