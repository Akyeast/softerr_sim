import math
from functools import reduce
from core.utils import lcm

def tda_analysis_ol(tasks, delta=1.0, fault=True):

    c_tasks = [task for task in tasks if task[2] == 1]
    deadline_points = get_deadline_points(tasks)

    for t in deadline_points:
        # demand = sum(math.floor(((t - task[0]*delta) / task[0]) + 1)*task[1] for task in tasks) 
        dbf = sum(math.floor((t / task[0]))*task[1] for task in tasks)
        max_exec_c_task = get_max_exec_c_task(c_tasks, t)
        rerun_capacity = max_exec_c_task[1]
        if fault:
            demand_tot = dbf + rerun_capacity
        else:
            demand_tot = dbf
            
        if demand_tot > t :
            return False                
    else:
        return True

def tda_analysis_ds(tasks, delta=1.0, fault=True):

    c_tasks = [task for task in tasks if task[2] == 1]
    deadline_points = get_deadline_points(tasks) 

    for t in deadline_points:
        # demand = sum(math.floor(((t - task[0]*delta) / task[0]) + 1)*task[1] for task in tasks) 
        dbf = sum(math.floor((t / task[0]))*task[1] for task in tasks)
        max_exec_c_task = get_max_exec_c_task(c_tasks, t)
        rerun_capacity = max_exec_c_task[1]
        if fault:
            demand_tot = dbf + rerun_capacity
        else:
            demand_tot = dbf

        if demand_tot > t :
            return False                
    else:
        return True

def tda_analysis_ours(tasks, delta=1.0, fault=True):

    c_tasks = [task for task in tasks if task[2] == 1]
    deadline_points = get_deadline_points(tasks)

    for t in deadline_points:
        # demand = sum(math.floor(((t - task[0]*delta) / task[0]) + 1)*task[1] for task in tasks) 
        dbf_fault = sum(math.floor((t / task[0]))*task[1] for task in c_tasks)
        dbf_normal = sum(math.floor((t / task[0]))*task[1] for task in tasks)
        
        max_exec_c_task = get_max_exec_c_task(c_tasks, t)
        rerun_capacity = max_exec_c_task[1]

        demand_tot_normal = dbf_normal
        if fault:
            demand_tot_fault = dbf_fault + rerun_capacity
        else:
            demand_tot_fault = dbf_fault
        
        if demand_tot_fault > t or demand_tot_normal > t:
            return False
        
    else:
        return True
    
def tda_analysis_ol_transform(transformed_ls_tasks, transform_multipliers, min_period, min_exec, transform_constant, delta=1.0, fault=True):

    c_tasks = [task for task in transformed_ls_tasks if task[2] == 1]
    deadline_points = get_deadline_points_transform(transform_multipliers, min_period, transform_constant)

    for t in deadline_points:
        # demand = sum(math.floor(((t - task[0]*delta) / task[0]) + 1)*task[1] for task in tasks) 
        dbf = sum(math.floor((t / task[0]))*task[1] for task in transformed_ls_tasks)
        max_exec_c_task = get_max_exec_c_task(c_tasks, t)
        rerun_capacity = max_exec_c_task[1]
        if fault:
            demand_tot = dbf + rerun_capacity
        else:
            demand_tot = dbf
            
        if demand_tot > t :
            return False                
    else:
        return True

def tda_analysis_ds_transform(transformed_ls_tasks, transform_multipliers, min_period, min_exec, transform_constant, delta=1.0, fault=True):

    c_tasks = [task for task in transformed_ls_tasks if task[2] == 1]
    deadline_points = get_deadline_points_transform(transform_multipliers, min_period, transform_constant)

    for t in deadline_points:
        # demand = sum(math.floor(((t - task[0]*delta) / task[0]) + 1)*task[1] for task in tasks) 
        dbf = sum(math.floor((t / task[0]))*task[1] for task in transformed_ls_tasks)
        max_exec_c_task = get_max_exec_c_task(c_tasks, t)
        rerun_capacity = max_exec_c_task[1]
        if fault:
            demand_tot = dbf + rerun_capacity
        else:
            demand_tot = dbf

        if demand_tot > t :
            return False                
    else:
        return True

def tda_analysis_ours_transform(transformed_ls_tasks, transform_multipliers, min_period, min_exec, transform_constant, delta=1.0, fault=True):

    c_tasks = [task for task in transformed_ls_tasks if task[2] == 1]
    deadline_points = get_deadline_points_transform(transform_multipliers, min_period, transform_constant)

    for t in deadline_points:
        # demand = sum(math.floor(((t - task[0]*delta) / task[0]) + 1)*task[1] for task in transformed_tasks) 
        dbf_fault = sum(math.floor((t / task[0]))*task[1] for task in c_tasks)
        dbf_normal = sum(math.floor((t / task[0]))*task[1] for task in transformed_ls_tasks)
        
        max_exec_c_task = get_max_exec_c_task(c_tasks, t)
        rerun_capacity = max_exec_c_task[1]

        demand_tot_normal = dbf_normal
        if fault:
            demand_tot_fault = dbf_fault + rerun_capacity
        else:
            demand_tot_fault = dbf_fault
        
        if demand_tot_fault > t or demand_tot_normal > t:
            return False
        
    else:
        return True    
    
def get_max_exec_c_task(c_tasks, t):
    filtered_tasks = [task for task in c_tasks if task[0] <= t]
    if filtered_tasks:
        max_exec_task = max(filtered_tasks, key=lambda x: x[1], default=None)
    else:
        max_exec_task = (0, 0, 0)
    return max_exec_task

def get_deadline_points(tasks):
    # implicit deadline!
    deadlines = [task[0] for task in tasks]
    lcm_deadlines = lcm(deadlines)
    # print(f'deadlines = {deadlines}')
    # print(f'lcm_deadlines = {lcm_deadlines}')

    ## temporary max cut
    if lcm_deadlines >= 10000 :
        lcm_deadlines = 10000
    
    # print(f'lcm_deadlines = {lcm_deadlines}')

    deadline_points = sorted(set(p for deadline in deadlines for p in range(deadline, lcm_deadlines+1, deadline)))
    # print(f'deadline_points = {deadline_points}')
    return deadline_points

def get_deadline_points_transform(multipliers, min_period, transform_constant):
    # implicit deadline!
    if not multipliers:
        return []
    
    deadlines = [min_period*(1+transform_constant)**multiplier[0] for multiplier in multipliers]

    unique_deadlines = set(deadlines)
    for deadline in deadlines:
        # 각 deadline에 대해 floor 값과 ceil 값을 추가
        unique_deadlines.add(math.floor(deadline))
        unique_deadlines.add(math.ceil(deadline))

    min_deadline = min(unique_deadlines)
    max_deadline = max(unique_deadlines) 
    
    # print(f'lcm_deadlines = {lcm_deadlines}')

    deadline_points = sorted(unique_deadlines)
    
    return deadline_points


# [(period, execution, critical), (5, 3, 1), ...]
#             Schedulable(1,0)