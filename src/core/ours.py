from core.mapping import critical2core
from core.utils import get_minimum_core, get_PRM_bound
from core.task_sche_check import assign_nc2PRM

def get_num_core_ours(tasks):
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
        schedulable, prms, mapped_nc = assign_tasks(core, c_tasks, nc_tasks)
        core += 2

    print("PRMs: ", prms)
    print("Mapped NC tasks: ", mapped_nc)

    return core

def assign_tasks(core, c_tasks, nc_tasks):
    mapped_c_tasks, assigned_cores = critical2core(c_tasks, int(core/2))

    # TODO: check schedulability with fault case, if not schedulable, increase core by 2
    
    prm_bounds = get_PRM_bound(assigned_cores)
    prms, mapped_nc_tasks = assign_nc2PRM(prm_bounds, nc_tasks)
    
    mapped_tasks = mapped_c_tasks + mapped_nc_tasks

    return all([t[3] != None for t in mapped_tasks]), prms, mapped_tasks