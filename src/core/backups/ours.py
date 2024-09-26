import json
from core.utils import get_minimum_core, get_PRM_bound, argmin, argmax
from core.task_sche_check import assign_nc2PRM, assign_nc_bind
from core.tda import tda_analysis

# with open('cfg/prm_cfg.json', 'r') as f:
#     cfg = json.load(f)

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
    prms = []
    mapped_tasks = [[] for _ in range(num_core)]

    is_schedulable_c, mapped_c_tasks, assigned_utils = assign_critical_tda(int(num_core), c_tasks, delta)

    # prm_bounds = get_PRM_bound(assigned_utils)
    # prms, mapped_nc_tasks = assign_nc2PRM(prm_bounds, nc_tasks)
    is_schedulable_nc, mapped_nc_tasks_real, mapped_nc_tasks_binded, assigned_utils_real, assigned_utils_binded = assign_nc_bind(int(num_core), nc_tasks, mapped_c_tasks, assigned_utils)
    # real -> not used


    # is_schedulable_nc =  all([t[3] != None for t in mapped_tasks])
    
    for index in range(num_core):
        mapped_tasks[index] = mapped_c_tasks[index] + mapped_nc_tasks_binded[index]


    is_schedulable = is_schedulable_c & is_schedulable_nc

    # print(f'DEBUG_ours_c_nc: {len(mapped_c_tasks)}, {len(mapped_nc_tasks)}, {assigned_utils}')

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
    # num_task_schedulable = len(mapped_tasks)
    
    # print("###############################")
    # print(f'DEBUG_ours_overall: {len(mapped_tasks)}')
    # print("###############################")



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
    heuristic = 'wf'
    assigned_cores = [0.0 for _ in range(core)]
    index = 0
    
    for task in c_tasks: 
        ### get index
        if heuristic == 'wf':
            if min(assigned_cores) + task[1]/task[0] <= 1:
                index = argmin(assigned_cores)
                index_pair = index+1                
            else:
                return False, mapped_tasks, assigned_cores
        elif heuristic == 'bf':
            print('not implemented')
        else:
            raise ValueError("heuristic must be 'wf' or 'bf'")
        
        #### tda_analysis
        if tda_analysis(mapped_tasks[index] + [task], delta):
            mapped_tasks[index].append(task)
            mapped_tasks[index_pair].append(task)
            utilization = task[1]/task[0]
            assigned_cores[index] += utilization
            assigned_cores[index_pair] += utilization
        else:
            return False, mapped_tasks, assigned_cores

    #     for i in range(core):
    #         if tda_analysis(mapped_tasks[i] + [task], delta):
    #             mapped_tasks[i].append(task)
    #             modified_list.append((*task, i))
    #             break
    #     else:
    #         return False, [], []

    # assigned_utils = []
    # for i in range(core):
    #     assigned_utils.append(0)
    #     max_exec = 0
    #     for task in mapped_tasks[i]:
    #         utilization = task[1]/task[0]
    #         assigned_utils[i] += utilization

    # print("!!!!!!!!!!!!!!!!!!OURS!!!!!!!!!!!!!")
    # print(assigned_cores)

    return True, mapped_tasks, assigned_cores