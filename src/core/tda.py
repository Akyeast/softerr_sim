import math
from core.task_sche_check import lcm

def tda_analysis(tasks, delta=1.0, fault=True):
    max_t = lcm([t[0] for t in tasks])
    rerun = max([task[1] for task in tasks]) if fault else 0
    min_t = math.floor(min([task[0]*delta for task in tasks]))

    for idx, rerun_task in enumerate(tasks):
        interference_tasks = tasks[:idx] + tasks[idx+1:]
        for t in range(0, max_t+1):
            # demand = sum(math.floor(((t - task[0]*delta) / task[0]) + 1)*task[1] for task in tasks) + rerun
            interference = sum(math.floor(((t - task[0]*delta) / task[0]) + 1)*task[1] for task in interference_tasks)
            fault_task_workload = math.floor(t / rerun_task[0]) * rerun_task[1]

            demand = interference + fault_task_workload

            if t >= rerun_task[0]:
                demand += rerun_task[1]

            # print(demand, t)
            if demand > t :
                return False
            if demand + 1000 < t :
                # return True
                break
    else:
        return True