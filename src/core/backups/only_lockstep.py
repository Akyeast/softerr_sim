import json
from core.utils import get_minimum_core, get_PRM_bound, argmin, argmax
from core.task_sche_check import assign_nc2PRM
from core.tda import tda_analysis, tda_analysis_onlyls

# with open('cfg/prm_cfg.json', 'r') as f:
#     cfg = json.load(f)

def check_schedulable_only_lockstep(tasks, num_core=8, binding_constant=0.1, transform_constant=0.1, cfg={}):
    """
        Input: 
            [(period, execution, critical), (5, 3, 1), ...]
        Output:
            Schedulable(1,0)
    """    

    candnc_tasks = [task for task in tasks if (task[2] == 0 or task[2] == 1)]

    is_schedulable = False
    mapped_tasks = [[] for _ in range(num_core)]

    is_schedulable, mapped_tasks, assigned_utils = assign_onlyls_tda_reserve_rerun(int(num_core), candnc_tasks, )

    # print("###############################")
    # print(f'DEBUG_only_lockstep: {len(mapped_tasks)}, {assigned_utils}')
    # print("###############################")

    return is_schedulable, mapped_tasks

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

def get_num_task_schedulable_only_lockstep(tasks, num_core=8, max_num_task=40, binding_constant=0.1, transform_constant=0.1, cfg={}):

    # print("Avg. Utilization of Tasksets")
    # utils = [task[1]/task[0] for task in tasks]
    # print(utils)
    print('debug::entrance!')
    
    num_task = 0
    is_schedulable = True

    while is_schedulable:
        num_task += 1
        if num_task > max_num_task:
            break

        is_schedulable, prms, mapped_tasks = check_schedulable_only_lockstep(tasks[0:num_task], num_core, binding_constant, transform_constant, cfg)
        # print(f'DEBUG_only_lockstep___3: {num_task}')
        
    num_task_schedulable = num_task - 1
    # num_task_schedulable = len(mapped_tasks)
    
    # print("###############################")
    # print(f'DEBUG_only_lockstep: {len(mapped_tasks)}, {assigned_utils}')
    # print("###############################")

    
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

def assign_onlyls_tda_reserve_rerun(core, tasks, ):
    mapped_tasks = [[] for _ in range(core)]
    heuristic = 'wf'
    assigned_cores = [0.0 for _ in range(core)]
    index = 0

    for task in tasks: 
        #### get index
        # print(f'in critical {task}')
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
        if tda_analysis_onlyls(mapped_tasks[index] + [task], delta):
            mapped_tasks[index].append(task)
            mapped_tasks[index_pair].append(task)
            utilization = task[1]/task[0]
            assigned_cores[index] += utilization
            assigned_cores[index_pair] += utilization
        else:
            return False, mapped_tasks, assigned_cores

    ## reserve rerun
    for i in range(core):
        max_exec = 0
        largest = None
        for task in mapped_tasks[i]:
            if task[2] == 1 and task[1] >= max_exec:
                ### always task[2] == 1  here
                max_exec = task[1]
                largest = task
        if largest != None:
            assigned_cores[i] += largest[1]/largest[0]            
    
    # print("only!!!!!!!!!!!!!!!!!!!Lockstep!!!!!!!!!!!!!")
    # print(assigned_cores)
    
    return True, mapped_tasks, assigned_cores


# def assign_onlyls_tda_reserve_rerun(core, tasks, delta):
#     mapped_tasks = [[] for _ in range(core)]
#     modified_list = []
#     for task in tasks: 
#         for i in range(core):
#             if tda_analysis_onlyls(mapped_tasks[i] + [task], delta):
#                 mapped_tasks[i].append(task)
#                 modified_list.append((*task, i))
#                 break
#         else:
#             return False, [], []
    
#     assigned_utils = []
#     for i in range(core):
#         assigned_utils.append(0)
#         max_exec = 0
#         largest = mapped_tasks[i][0] if len(mapped_tasks[i]) > 0 else None
#         for task in mapped_tasks[i]:
#             utilization = task[1]/task[0]
#             assigned_utils[i] += utilization
#             if task[1] >= max_exec:
#                 max_exec = task[1]
#                 largest = task
#         if largest != None:
#             assigned_utils[i] += largest[1]/largest[0]

#     return True, modified_list, assigned_utils
