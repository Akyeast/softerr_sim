import json
from core.mapping import critical2core
from core.utils import get_minimum_core, get_PRM_bound
from core.task_sche_check import assign_nc2PRM
from core.rta import rta_all, rta_all_single
from core.tda import tda_analysis

with open('cfg/prm_cfg.json', 'r') as f:
    cfg = json.load(f)

def get_num_core_ours(tasks, delta=1.0):
    """
        Input: 
            [(period, execution, critical), (5, 3, 1), ...]
        Output:
            minimum required core number
    """
    core = get_minimum_core(tasks)
    c_tasks = [task for task in tasks if task[2] == 1]
    nc_tasks = [task for task in tasks if task[2] == 0]
    schedulable = False

    while not schedulable:
        schedulable, prms, mapped_tasks = assign_tasks(core, c_tasks, nc_tasks, delta)
        
        if not schedulable:
            core += 2

        if core > 99:
            break

    # print("PRMs: ", prms)
    # print("Mapped all tasks: ", mapped_tasks)

    return core, prms, mapped_tasks

def get_num_core_ours_delta(tasks, delta=1.0):
    """
        Input: 
            [(period, execution, critical), (5, 3, 1), ...]
        Output:
            minimum required core number
    """
    core = get_minimum_core(tasks)
    c_tasks = [task for task in tasks if task[2] == 1]
    nc_tasks = [task for task in tasks if task[2] == 0]
    schedulable = False
    prms, mapped_tasks = [], []

    while not schedulable:
        if core > 99:
            break

        schedulable, mapped_c_tasks, assigned_utils = assign_critical_tda(int(core/2), c_tasks, delta)

        if not schedulable:
            core += 2
            continue

        prm_bounds = get_PRM_bound(assigned_utils)
        prms, mapped_nc_tasks = assign_nc2PRM(prm_bounds, nc_tasks)

        mapped_tasks = mapped_c_tasks + mapped_nc_tasks

        schedulable =  all([t[3] != None for t in mapped_tasks])
        
        if not schedulable:
            core += 2

    return core, prms, mapped_tasks

def assign_critical_tda(core, c_tasks, delta):
    mapped_tasks = [[] for _ in range(core)]
    modified_list = []
    for task in c_tasks: 
        for i in range(core):
            if tda_analysis(mapped_tasks[i] + [task]):
                mapped_tasks[i].append(task)
                modified_list.append((*task, i))
                break
        else:
            return False, None, []

    assigned_utils = [sum([t[1]/t[0] for t in tasks]) for tasks in mapped_tasks]
    return True, modified_list, assigned_utils

def assign_tasks(core, c_tasks, nc_tasks, delta=1.0):
    mapped_c_tasks, assigned_cores, _ = critical2core(c_tasks, int(core/2), delta=delta)

    if assigned_cores is None:
        return False, None, None

    if not check_fault_case(mapped_c_tasks, assigned_cores):
        return False, None, None

    prm_bounds = get_PRM_bound(assigned_cores)
    prms, mapped_nc_tasks = assign_nc2PRM(prm_bounds, nc_tasks)
    
    mapped_tasks = mapped_c_tasks + mapped_nc_tasks

    return all([t[3] != None for t in mapped_tasks]), prms, mapped_tasks

def check_fault_case(tasks, cores):
    for i in range(len(cores)):
        assigned_tasks = [t[:3] for t in filter(lambda x: x[3]==i, tasks)]
        schedulability = rta_all_single(assigned_tasks, fault=True)
        # schedulability = rta_all(assigned_tasks, num_core=1, fault=True)
        if not schedulability:
            return False
    else:
        return True