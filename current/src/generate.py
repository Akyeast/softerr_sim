import math
import random
import util

def random_task_set(num_tasks, period_range, utilization_range, critical_p):
    tasks = []
    for i in range(num_tasks):
        period = math.floor(util.log_uniform(period_range[0], period_range[1]))
        execution_time = max(1, math.floor(util.log_uniform(utilization_range[0], utilization_range[1])*period))
        critical = random.random() < critical_p
        task={
            "index": i,
            "period": period,
            "execution_time": execution_time,
            "deadline" : period,
            "critical" : critical
        }
        tasks.append(task)
    return tasks
