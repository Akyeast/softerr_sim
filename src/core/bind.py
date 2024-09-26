import math
from core.utils import argmin, argmax
from generator.task import Task, TaskSet

def bind_nc_tasks(tasks, binding_policy="sort", binding_constant=0.1):
    # make new virtual tasks(Heuristic)
    # print(f"BIND:: binding_policy = {binding_policy}, binding_constant = {binding_constant}")
    sorted_tasks = sorted(tasks, key=lambda x: x[0], reverse=False)
    num_tasks = len(sorted_tasks)
    
    binded_tasks = []

    # period sorting
    if binding_policy=="sort" :
        # print(f"BIND:: sort")
        
        for i in range(0, num_tasks, 2):
            task_1 = sorted_tasks[i]
            # odd case
            if i + 1 < num_tasks:
                task_2 = sorted_tasks[i + 1]
            else:
                task_2 = task_1  

            binding_overhead = get_binding_overhead(task_1, task_2)

            if binding_overhead >= 2:
                binded_tasks.append(task_1)
                binded_tasks.append(task_2)
            else:
                binded_task=bind_task(task_1, task_2)
                binded_tasks.append(binded_task)
        
        # print(f'binded_tasks:{binded_tasks}')
        # overall_utilization = debug_overall_utilization(binded_tasks)      
        # print(f'overall_util:{overall_utilization}')
        # print(f"BIND:: sort end")
    
    elif binding_policy=="neighbor" :
        print("BIND:neighbor bind is not implemented")
        
    
    elif binding_policy == "iterative":
        # print(f"BIND:: iterative start")
        binding_threshold = 1 + binding_constant
        current_tasks = sorted_tasks[:]  # sorted_tasks copy
        # print(f'init tasks: {current_tasks}')

        while binding_threshold < 2.0:
            # print(f'binding_threshold: {binding_threshold}')
            
            if len(current_tasks) == 0:
                break

            binded_flag = [False] * len(current_tasks)
            next_tasks = []
            i = 0
            while i < len(current_tasks) - 1:
                if binded_flag[i]:
                    i += 1
                    continue

                task_1 = current_tasks[i]
                task_binded = False

                for j in range(i + 1, len(current_tasks)):
                    if binded_flag[j]:
                        continue

                    task_2 = current_tasks[j]
                    binding_overhead = get_binding_overhead(task_1, task_2)

                    if binding_overhead < binding_threshold:
                        binded_task = bind_task(task_1, task_2)
                        binded_tasks.append(binded_task)
                        # print(f'bind {task_1}, {task_2}, binded_task: {binded_task}')
                        task_binded = True
                        binded_flag[i] = True
                        binded_flag[j] = True
                        break

                i += 1
            
            for k in range(0, len(current_tasks)):
                if not binded_flag[k]:
                    # print(f'task {current_tasks[k]}is unbinded')
                    next_tasks.append(current_tasks[k])

            current_tasks = next_tasks
            binding_threshold += binding_constant

        # print(f'current_tasks = {current_tasks}')
        binded_tasks.extend(current_tasks)

        # print(f'binded_tasks:{binded_tasks}')
        # overall_utilization = debug_overall_utilization(binded_tasks)      
        # print(f'overall_util:{overall_utilization}')
        # print(f"BIND:: iterative end")
    elif binding_policy == "exhaustive":
        print('TBD')
        # sum_binding_overhead = 0.0
        # for i in range(num_tasks):
        #     task_1 = sorted_tasks[i]
        #     for j in range(num_tasks):
        #         if i==j:
        #             continue
        #         task_2 = sorted_tasks[j]

            
                

        # for i in range(0, num_tasks, 2):
        #     task_1 = sorted_tasks[i]
        #     # odd case
        #     if i + 1 < num_tasks:
        #         task_2 = sorted_tasks[i + 1]
        #     else:
        #         task_2 = task_1  

        #     binding_overhead = get_binding_overhead(task_1, task_2)

        #     if binding_overhead >= 2:
        #         binded_tasks.append(task_1)
        #         binded_tasks.append(task_2)
        #     else:
        #         binded_task=bind_task(task_1, task_2)
        #         binded_tasks.append(binded_task)        
    else :
        print("BIND:Never Reached")
      

    return binded_tasks, sorted_tasks

def get_binding_overhead(a, b):
    
    util_a = a[1]/a[0]
    util_b = b[1]/b[0]
    util_binded = max(a[1], b[1])/min(a[0], b[0])

    binding_overhead = 2 * util_binded / (util_a + util_b)

    return binding_overhead

def bind_task(a, b):
    period = min(a[0], b[0])
    execution_time = max(a[1], b[1])
    criticality = 0
    return (period, execution_time, criticality)

def debug_overall_utilization(tasks):
    sum = 0
    for task in tasks:
        sum += task[1]/task[0]
    
    return sum