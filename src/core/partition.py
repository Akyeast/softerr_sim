import json
from itertools import product
# from src.core.backups.task_sche_check import assign_nc2PRM, assign_nc_bind
from core.utils import argmin, argmax
from core.bind import bind_nc_tasks
import numpy as np

# with open('cfg/prm_cfg.json', 'r') as f:
#     cfg = json.load(f)

# ################## cfg
# {
#     "num_task_sets": 2000,
#     "num_tasks": 80,
#     "max_num_task": 80,
#     "critical_prob_list": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
#     "criticality_per_state": false,
#     "period": [10, 50],
#     "num_states_list": [1],
#     "num_states": 1,
#     "task_max_utilization": 0.3,
#     "max_util_list": [1.0],
#     "period_gen": "log",
#     "util_gen": "random",
#     "num_core": 8,
#     "max_num_core": 8,
#     "deltas": [1.0],
#     "binding_constant": 0.1,
#     "transform_constant": 0.1
# }

def partition(ls_tasks, num_ls_core=4,
                partitioning_policy="worstfit", transform_constant=0.1,
                cfg={}):
    
    overflow = False
    mapped_ls_tasks = [[] for _ in range(num_ls_core)]
    assigned_utils = [0.0 for _ in range(num_ls_core)]

    # mapped_ls_tasks[worstfit_core_num].append(task)
    # assigned_utils[worstfit_core_num] += task[1]/task[0]

    if partitioning_policy == "worstfit":
        for task in ls_tasks:
            worstfit_core = get_worstfit_core(num_ls_core, assigned_utils)
            if worstfit_core:
                mapped_ls_tasks[worstfit_core].append(task)
                assigned_utils[worstfit_core]+= task[1]/task[0]
            else:
                overflow = True

    elif partitioning_policy == "bestfit":
        for task in ls_tasks:
            bestfit_core = get_bestfit_core(num_ls_core)
            if bestfit_core:
                mapped_ls_tasks[bestfit_core].append(task)
                assigned_utils[bestfit_core]+= task[1]/task[0]
            else:
                overflow = True

    elif partitioning_policy == "nonamed":
        sorted_ls_tasks = sorted(ls_tasks, key=lambda x: x[1], reverse=True)
        for task in sorted_ls_tasks:
            bestfit_core = get_bestfit_core(num_ls_core, assigned_utils)
            if bestfit_core:
                mapped_ls_tasks[bestfit_core].append(task)
                assigned_utils[bestfit_core]+= task[1]/task[0]
            else:
                overflow = True

    elif partitioning_policy == "exhaustive":
        print(f'not implemented')

    else:
        print(f'never reached')
    
    return overflow, mapped_ls_tasks, assigned_utils

def get_worstfit_core(num_ls_core, assigned_utils):
    indices_sorted = np.argsort(assigned_utils)
    worstfit_core = None

    for index in indices_sorted:
        if assigned_utils[index] < 1.0:
            worstfit_core = index
            break
    
    return worstfit_core

def get_bestfit_core(num_ls_core, assigned_utils):
    indices_sorted = np.argsort(assigned_utils)
    bestfit_core = None

    for index in reversed(indices_sorted):
        if assigned_utils[index] < 1.0:
            bestfit_core = index
            break
    
    return bestfit_core

