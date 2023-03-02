import random 
import json
import math
from generator.utils import UUniFastDiscard, SimpleRandom
from generator.task import Task, TaskSet

def generate_tasksets(cfg):
    # tasksets_util = UUniFastDiscard(cfg['num_tasks'], cfg['task_set_utilization'], cfg['num_task_sets'])
    tasksets_util = SimpleRandom(cfg['num_tasks'], cfg['num_task_sets'], cfg['task_max_utilization'])
    # period_from, period_to = cfg['period']
    critical_prob = cfg['critical_prob']
    criticality_per_state = cfg['criticality_per_state']

    gen_taskset = []

    for task_set in tasksets_util:
        tasks = []
        for task_util in task_set :
            if len(cfg['period']) == 2 :
                period = random.randint(*cfg['period']) # both included
            else :
                period = random.sample(cfg['period'], k=1)[0]
            
            
            execution = max(math.floor(task_util * period), 1)

            if criticality_per_state :
                if 'criticality_threshold' in cfg.keys() :
                    if random.random() < critical_prob :
                        criticality = [1 if random.random() < cfg['criticality_threshold'] else 0 for _ in range(cfg['num_states'])]
                    else :
                        criticality = [0 for _ in range(cfg['num_states'])]
                else :
                    criticality = [1 if random.random() < critical_prob else 0 for _ in range(cfg['num_states'])]
            else :
                criticality = [1 if random.random() < critical_prob else 0] * cfg['num_states']


            tasks.append(Task(period, execution, criticality))

        gen_taskset.append(TaskSet(tasks))

    return gen_taskset


def generate_example_taskset() :
    # (period, execution, criticality per state)
    tasks = [
        Task(10, 3, [1]),
        Task(20, 7, [1]),
        Task(30, 10, [0]),
    ]

    return TaskSet(tasks)

if __name__ == '__main__':
    tasks = generate_tasksets()
    # print(tasks[0].get_tasks(sort=True, desc=True))