import json
from core.mapping import critical2core
from core.utils import get_minimum_core, get_PRM_bound
from core.task_sche_check import assign_nc2PRM
from core.rta import rta_all_baseline

def get_num_core_baseline(tasks):
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
        schedulable, prms, mapped_tasks = assign_tasks(core, tasks, [])
        if not schedulable:
            core += 2

    return core, prms, mapped_tasks

def assign_tasks(core, c_tasks, nc_tasks):
    mapped_c_tasks, assigned_cores, _ = critical2core(c_tasks, int(core/2))

    if not check_fault_case(mapped_c_tasks, assigned_cores):
        return False, None, None

    prm_bounds = get_PRM_bound(assigned_cores)
    prms, mapped_nc_tasks = assign_nc2PRM(prm_bounds, nc_tasks)
    
    mapped_tasks = mapped_c_tasks + mapped_nc_tasks

    return all([t[3] != None for t in mapped_tasks]), prms, mapped_tasks

def check_fault_case(tasks, cores):
    for i in range(len(cores)):
        assigned_tasks = [t[:3] for t in filter(lambda x: x[3]==i, tasks)]

        critical = [t for t in filter(lambda x: x[2]==1, assigned_tasks)]
        non_critical = [t for t in filter(lambda x: x[2]==0, assigned_tasks)]

        schedulability = rta_all_baseline(critical, non_critical, fault=True)
        if not schedulability:
            return False
    else:
        return True