import json
from core.utils import get_minimum_core, get_PRM_bound
from core.task_sche_check import assign_nc2PRM
from core.tda import tda_analysis

with open('cfg/prm_cfg.json', 'r') as f:
    cfg = json.load(f)

### Solution
def check_schedulable_ours(tasks, delta=1.0, num_core=8):
    """
        Input: 
            [(period, execution, critical), (5, 3, 1), ...]
        Output:
            Schedulable(1,0)
    """    

    c_tasks = [task for task in tasks if task[2] == 1]
    nc_tasks = [task for task in tasks if task[2] == 0]

    is_schedulable = False
    prms, mapped_tasks = [], []

    is_schedulable_c, mapped_c_tasks, assigned_utils = assign_critical_tda(int(num_core/2), c_tasks, delta)

    prm_bounds = get_PRM_bound(assigned_utils)
    prms, mapped_nc_tasks = assign_nc2PRM(prm_bounds, nc_tasks)

    mapped_tasks = mapped_c_tasks + mapped_nc_tasks

    is_schedulable_nc =  all([t[3] != None for t in mapped_tasks])
    
    is_schedulable = is_schedulable_c & is_schedulable_nc


    return is_schedulable, prms, mapped_tasks


### Evaluation
def get_num_task_schedulable_ours(tasks, delta=1.0, num_core=8, max_num_task=40):

    num_task = 0
    is_schedulable = True

    while is_schedulable:
        num_task += 1
        if num_task > max_num_task:
            break

        is_schedulable, prms, mapped_tasks = check_schedulable_ours(tasks[0:num_task], delta, num_core)

    num_task_schedulable = num_task - 1

    return num_task_schedulable, prms, mapped_tasks

def get_num_core_ours(tasks, delta=1.0, max_num_core=16, max_num_task=40):
    num_core = 0
    prms = []
    mapped_tasks = []

    is_schedulable = False

    while not is_schedulable:
        num_core += 2
        
        if num_core > max_num_core:
            num_core -= 2
            break        
        
        is_schedulable, prms, mapped_tasks = check_schedulable_ours(tasks, delta, num_core)
        

        # print(f'DEBUG_only_lockstep___3: {num_task}')

    return num_core, prms, mapped_tasks

def assign_critical_tda(core, c_tasks, delta):
    mapped_tasks = [[] for _ in range(core)]
    modified_list = []
    for task in c_tasks: 
        for i in range(core):
            if tda_analysis(mapped_tasks[i] + [task], delta):
                mapped_tasks[i].append(task)
                modified_list.append((*task, i))
                break
        else:
            return False, [], []

    assigned_utils = []
    for i in range(core):
        assigned_utils.append(0)
        max_exec = 0
        for task in mapped_tasks[i]:
            utilization = task[1]/task[0]
            assigned_utils[i] += utilization

    return True, modified_list, assigned_utils