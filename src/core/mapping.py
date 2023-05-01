from core.utils import argmin, argmax

def critical2core(tasks, num_core, heuristic='wf'):
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
        if heuristic == 'wf':   
            index = argmin(assigned_cores)
        elif heuristic == 'bf':
            max_util_idx = [(val, idx) for idx, val in enumerate(max_util)]
            max_util_sorted = sorted(max_util_idx, reverse=True)

            for max_util_core, i in max_util_sorted:
                if max_util_core + task[1] / task[0] <= 1.0:
                    index = i
                    break
            else:
                raise ValueError("task {} cannot be assigned to any core".format(task))
        else:
            raise ValueError("heuristic must be 'wf' or 'bf'")
        
        mapped_tasks.append((*task, index))
        assigned_cores[index] += task[1] / task[0]
        if task[1] / task[0] > max_util[index]:
            max_util[index] = task[1] / task[0]
    return mapped_tasks, assigned_cores, max_util