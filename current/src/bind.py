def get_binding_overhead(a, b):
    
    util_a = a['execution_time']/a['period']
    util_b = b['execution_time']/b['period']
    util_binded = max(a['execution_time'], b['execution_time'])/min(a['period'], b['period'])
    binding_overhead = 2 * util_binded / (util_a + util_b)

    return binding_overhead

def bind_task(a, b):
    period = min(a['period'], b['period'])
    execution_time = max(a['execution_time'], b['execution_time'])
    task={
            "index": -1,
            "period": period,
            "execution_time": execution_time,
            "deadline" : period,
            "vertual_deadline" : (execution_time+(period-execution_time))/2,
            "critical" : False
        }
    return task

def bind_nc_tasks(tasks, binding_constant=0.1):
    if len(tasks)<2:
        return tasks
    # make new virtual tasks(Heuristic)
    sorted_tasks = sorted(tasks, key=lambda x: x['period'], reverse=False)
    
    binded_tasks = []
    binding_threshold = 1 + binding_constant
    current_tasks = sorted_tasks[:]  # sorted_tasks copy

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

            for j in range(i + 1, len(current_tasks)):
                if binded_flag[j]:
                    continue

                task_2 = current_tasks[j]
                binding_overhead = get_binding_overhead(task_1, task_2)

                if binding_overhead < binding_threshold:
                    binded_task = bind_task(task_1, task_2)
                    binded_tasks.append(binded_task)
                    # print(f'bind {task_1}, {task_2}, binded_task: {binded_task}')
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
    return binded_tasks