import json
# from src.core.backups.task_sche_check import assign_nc2PRM, assign_nc_bind
from core.utils import argmin, argmax
from core.bind import bind_nc_tasks
from core.tda import tda_analysis_ol, tda_analysis_ls, tda_analysis_ours

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

def get_num_task_schedulable(tasks, num_core=8, max_num_task=40,
                             fault_handling_policy="only_lockstep",
                             binding_policy="sort", binding_constant=0.1,
                             partitioning_policy="worstfit", transform_constant=0.1,
                             cfg={}):

    print('DYNAMIC SWITCHING::entrance!')
    
    num_task = 0
    is_schedulable = True
    num_task_schedulable = 0
    mapped_tasks = []

    # ## task binding debug
    # check_schedulable_dynamic_switching(tasks[0:max_num_task], num_core, max_num_task, binding_policy, binding_constant, partitioning_policy, transform_constant, cfg)

    ## tda debug
    # check_schedulable_dynamic_switching(tasks[0:max_num_task], num_core, max_num_task, binding_policy, binding_constant, partitioning_policy, transform_constant, cfg)

    while is_schedulable:
        num_task += 1
        if num_task > max_num_task:
            break
        
        is_schedulable, mapped_tasks = check_schedulable(tasks[0:num_task], num_core, max_num_task,
                                                         fault_handling_policy,
                                                         binding_policy, binding_constant,
                                                         partitioning_policy, transform_constant,
                                                         cfg)
        

    num_task_schedulable = num_task - 1
    # num_task_schedulable = len(mapped_tasks)

    # print("###############################")
    # print(f'DEBUG_ds_overall: {len(mapped_tasks)}')
    # print("###############################")

    return num_task_schedulable, mapped_tasks

def check_schedulable(tasks, num_core=8, max_num_task=40,
                      fault_handling_policy="only_lockstep",
                      binding_policy="sort", binding_constant=0.1,
                      partitioning_policy="worstfit", transform_constant=0.1,
                      cfg={}):
    """
        Input: 
            [(period, execution, critical), (5, 3, 1), ...] 
        Output:
            Schedulable(1,0)
    """    
    is_schedulable = False
    mapped_ls_tasks = [[] for _ in range(num_core)]
    assigned_util = [0.0 for _ in range(num_core)]
    
    # print("DYNAMIC_SWITCHING: taskbinding call")
    c_tasks = [task for task in tasks if task[2] == 1]
    nc_tasks = [task for task in tasks if task[2] == 0]

    nc_tasks_binded, _ = bind_nc_tasks(nc_tasks, binding_policy, binding_constant)
    # print("DYNAMIC_SWITCHING: return")
    
    #lockstep_tasks
    ls_tasks = c_tasks+nc_tasks_binded
    # print(f'ls_tasks = {ls_tasks}')
    # print('DYNAMIC SWITCHING::call tda_analysis')
    is_schedulable, mapped_ls_tasks, assigned_util = partition_and_analysis(ls_tasks, num_core,
                                                                            partitioning_policy, transform_constant,
                                                                            cfg)
    print(f'return is_schedulable: {is_schedulable}')
    print(f'return mapped_ls_tasks: {mapped_ls_tasks}')
    print(f'return assigned_util: {assigned_util}')
    
    return is_schedulable, mapped_ls_tasks, assigned_util

def partition_and_analysis(tasks, num_core=8,
                           partitioning_policy="worstfit", transform_constant=0.1,
                           cfg={}):
    
    is_schedulable = False
    mapped_tasks = [[] for _ in range(num_core)]
    assigned_utils = [0.0 for _ in range(num_core)]

    if partitioning_policy == "worstfit":
        print(f'partitioning_policy is {partitioning_policy}')

    elif partitioning_policy == "transform":
        print(f'partitioning_policy is {partitioning_policy}')
        
    elif partitioning_policy == "exhaustive":
        print(f'partitioning_policy is {partitioning_policy}')
        
    else:
        print(f'never reached')

    return is_schedulable, mapped_tasks, assigned_utils

#####################NOT Used##########################

def assign_critical_tda_reserve_rerun(core, c_tasks, delta):
    mapped_tasks = [[] for _ in range(core)]
    heuristic = 'wf'
    assigned_cores = [0.0 for _ in range(core)]
    index = 0

    for task in c_tasks: 
        #### get index
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

    # print("!!!!!!!!!!!!!!!!!!DS!!!!!!!!!!!!!")
    # print(assigned_cores)

    return True, mapped_tasks, assigned_cores

def assign_critical_tda_reserve_rerun(core, c_tasks, delta):
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

def get_num_core_dynamic_switching(tasks, delta=1.0, max_num_core=16, max_num_task=40):
    num_core = 0
    prms = []
    mapped_tasks = []

    is_schedulable = False

    while not is_schedulable:
        num_core += 2
        
        if num_core > max_num_core:
            num_core -= 2
            break        
        
        is_schedulable, prms, mapped_tasks = check_schedulable_dynamic_switching(tasks, delta, num_core)
        

        # print(f'DEBUG_only_lockstep___3: {num_task}')

    return num_core, prms, mapped_tasks