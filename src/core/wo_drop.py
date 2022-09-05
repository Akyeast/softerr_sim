import json
from core.mapping import critical2core
from core.utils import get_minimum_core, get_PRM_bound
from core.task_sche_check import assign_nc2PRM
from core.rta import rta_all, rta_all_single, rta_all_single_wo_drop

with open('cfg/prm_cfg.json', 'r') as f:
    cfg = json.load(f)

def get_num_core_ours_wo_drop(tasks):
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
        schedulable, prms, mapped_tasks = assign_tasks_wo_drop(core, c_tasks, nc_tasks)

        # print("\nPRMS: ", prms)
        # print("mapped tasks: ", mapped_tasks, '\n')
        
        if not schedulable:
            core += 2

    return core

def assign_tasks_wo_drop(core, c_tasks, nc_tasks):
    mapped_c_tasks, assigned_cores = critical2core(c_tasks, int(core/2))
    prms = [ None ] * len(assigned_cores)
    
    if len(nc_tasks) > 0:
        prm_bounds = get_PRM_bound(assigned_cores)
        prms, nc_tasks = assign_nc2PRM(prm_bounds, nc_tasks, int(min([t[0] for t in nc_tasks])/2))

    mapped_tasks = mapped_c_tasks + nc_tasks

    if not check_fault_case_wo_drop(mapped_c_tasks, prms):
        return False, prms, mapped_tasks

    return all([t[3] != None for t in mapped_tasks]), prms, mapped_tasks

def check_fault_case_wo_drop(tasks, prms):
    # print('check fault case wo drop')
    # print('tasks: ', tasks)
    # print('prms: ', prms)
    for i in range(len(prms)):
        assigned_tasks = [t[:3] for t in filter(lambda x: x[3]==i, tasks)]
        # print(r"schedulability check on core {} with tasks {} and prm {}".format(i, assigned_tasks, prms[i]))
        schedulability = rta_all_single_wo_drop(assigned_tasks, fault=True, prm=prms[i])
        # schedulability = rta_all(assigned_tasks, num_core=1, fault=True)
        if not schedulability:
            return False
    else:
        return True