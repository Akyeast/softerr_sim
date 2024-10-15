import math
import random

def find_longest_critical_task_e(tasks):
    critical_tasks = [task for task in tasks if task["critical"]]
    if not critical_tasks:
        return 0
    longest_task = max(critical_tasks, key=lambda task: task["execution_time"])
    return longest_task["execution_time"]

def L_max(tasks):
    longest_c_e=find_longest_critical_task_e(tasks)
    # longest_c_e=0
    busy_period = sum(task["execution_time"] for task in tasks)+longest_c_e
    while(True):
        workload = sum(((busy_period//task["period"] +1) * task["execution_time"]) for task in tasks)+longest_c_e
        if workload == busy_period:
            break
        if workload >=300:
            # print("ex150")
            return 300
        busy_period = workload
    return busy_period

def log_uniform(a, b):
    log_a = math.log(a)
    log_b = math.log(b)
    return math.exp(random.uniform(log_a, log_b))