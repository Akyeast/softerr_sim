import random 
import json
import math
from utils import UUniFastDiscard
from task import Task, TaskSet

def generate_tasksets():
    with open('cfg/task_cfg.json', 'r') as f:
        cfg = json.load(f)
    
    tasksets_util = UUniFastDiscard(cfg['num_tasks'], cfg['utilization'], cfg['num_task_sets'])
    period_from, period_to = cfg['period']
    critical_prob = cfg['critical_prob']

    gen_taskset = []

    for task_set in tasksets_util:
        tasks = []
        for task_util in task_set :
            period = random.randint(period_from, period_to) # both included
            execution = math.ceil(task_util * period)
            criticality = [1 if random.random() < critical_prob else 0 for _ in range(cfg['num_states'])]        
            tasks.append(Task(period, execution, criticality))

        gen_taskset.append(TaskSet(tasks))

    return gen_taskset

if __name__ == '__main__':
    tasks = generate_tasksets()
    print(tasks[0].get_tasks(sort=True, desc=True))