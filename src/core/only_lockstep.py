import json
from core.utils import get_minimum_core, get_PRM_bound, argmax
from core.task_sche_check import assign_nc2PRM
from core.tda import tda_analysis, tda_analysis_onlyls

with open('cfg/prm_cfg.json', 'r') as f:
    cfg = json.load(f)


def check_schedulable_only_lockstep(tasks, delta=1.0, num_core=8):
    """
        Input: 
            [(period, execution, critical), (5, 3, 1), ...]
        Output:
            Schedulable(1,0)
    """    

    candnc_tasks = [task for task in tasks if (task[2] == 0 or task[2] == 1)]
    is_schedulable = False
    prms, mapped_tasks = [], []

    is_schedulable, mapped_tasks, assigned_utils = assign_onlyls_tda_reserve_rerun(int(num_core/2), candnc_tasks, delta)

    return is_schedulable, prms, mapped_tasks

def get_num_task_schedulable_only_lockstep(tasks, delta=1.0, num_core=8, max_num_task=40):

    num_task = 0
    is_schedulable = True

    while is_schedulable:
        num_task += 1
        if num_task > max_num_task:
            break

        is_schedulable, prms, mapped_tasks = check_schedulable_only_lockstep(tasks[0:num_task], delta, num_core)
        # print(f'DEBUG_only_lockstep___3: {num_task}')
        
    num_task_schedulable = num_task - 1
    return num_task_schedulable, prms, mapped_tasks

def get_num_core_only_lockstep(tasks, delta=1.0, max_num_core=16, max_num_task=40):
    num_core = 0
    prms = []
    mapped_tasks = []

    is_schedulable = False

    while not is_schedulable:
        num_core += 2
        
        if num_core > max_num_core:
            num_core -= 2
            break        
        
        is_schedulable, prms, mapped_tasks = check_schedulable_only_lockstep(tasks, delta, num_core)
        

        # print(f'DEBUG_only_lockstep___3: {num_task}')

    return num_core, prms, mapped_tasks

def assign_onlyls_tda_reserve_rerun(core, tasks, delta):
    mapped_tasks = [[] for _ in range(core)]
    modified_list = []
    for task in tasks: 
        for i in range(core):
            if tda_analysis_onlyls(mapped_tasks[i] + [task], delta):
                mapped_tasks[i].append(task)
                modified_list.append((*task, i))
                break
        else:
            return False, [], []
    
    assigned_utils = []
    for i in range(core):
        assigned_utils.append(0)
        max_exec = 0
        largest = mapped_tasks[i][0] if len(mapped_tasks[i]) > 0 else None
        for task in mapped_tasks[i]:
            utilization = task[1]/task[0]
            assigned_utils[i] += utilization
            if task[1] >= max_exec:
                max_exec = task[1]
                largest = task
        if largest != None:
            assigned_utils[i] += largest[1]/largest[0]

    return True, modified_list, assigned_utils
