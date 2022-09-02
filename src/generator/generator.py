import random 
import json
import math
from generator.utils import UUniFastDiscard, SimpleRandom
from generator.task import Task, TaskSet

def generate_tasksets(cfg):
    # tasksets_util = UUniFastDiscard(cfg['num_tasks'], cfg['task_set_utilization'], cfg['num_task_sets'])
    tasksets_util = SimpleRandom(cfg['num_tasks'], cfg['num_task_sets'])
    period_from, period_to = cfg['period']
    critical_prob = cfg['critical_prob']
    criticality_per_state = cfg['criticality_per_state']

    gen_taskset = []

    for task_set in tasksets_util:
        tasks = []
        for task_util in task_set :
            period = random.randint(period_from, period_to) # both included
            execution = max(math.floor(task_util * period), 1)
            if criticality_per_state :
                criticality = [1 if random.random() < critical_prob else 0 for _ in range(cfg['num_states'])]
            else :
                criticality = [1 if random.random() < critical_prob else 0] * cfg['num_states']
            tasks.append(Task(period, execution, criticality))

        gen_taskset.append(TaskSet(tasks))

    return gen_taskset

if __name__ == '__main__':
    tasks = generate_tasksets()
    # print(tasks[0].get_tasks(sort=True, desc=True))