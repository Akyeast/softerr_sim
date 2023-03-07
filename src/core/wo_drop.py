import json
from core.mapping import critical2core
from core.utils import get_minimum_core, get_PRM_bound
from core.task_sche_check import assign_nc2PRM
from core.rta import rta_all, rta_all_single, rta_all_single_wo_drop, rta_all_wo_drop

with open('cfg/prm_cfg.json', 'r') as f:
    cfg = json.load(f)

def get_num_core_ours_wo_drop(tasks, method='rta_single'):
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
        schedulable, prms, mapped_tasks = assign_tasks_wo_drop(core, c_tasks, nc_tasks, method)

        # print("\nPRMS: ", prms)
        # print("mapped tasks: ", mapped_tasks, '\n')
        
        if not schedulable:
            core += 2

    return core, prms, mapped_tasks


def assign_tasks_wo_drop(core, c_tasks, nc_tasks, method):
    mapped_c_tasks, assigned_cores, max_utils = critical2core(c_tasks, int(core/2))
    
    if len(nc_tasks) > 0:
        # prm_bounds = get_PRM_bound(assigned_cores)
        prm_bounds = get_PRM_bound([sum(value) for value in zip(assigned_cores, max_utils)])
        # 2(pi-theta) < t-e (for all)에 따라 ..
        prms, nc_tasks = assign_nc2PRM(prm_bounds, nc_tasks)
    else: 
        prms = [None] * len(assigned_cores)

    mapped_tasks = mapped_c_tasks + nc_tasks

    if not check_fault_case_wo_drop(mapped_c_tasks, prms, method):
        return False, prms, mapped_tasks

    return all([t[3] != None for t in mapped_tasks]), prms, mapped_tasks


def check_fault_case_wo_drop(tasks, prms, method):
    if method == 'rta_single':
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
    elif method == 'rta':
        tasks = [t[:3] for t in tasks]
        prm_tasks = [(task[0], task[1], 0) for task in prms if task!=None]
        return rta_all_wo_drop(tasks, prm_tasks, len(prms), fault=True)