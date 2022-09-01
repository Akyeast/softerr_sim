import random
import json

def UUniFastDiscard(n, u, nsets):
    sets = []
    while len(sets) < nsets:
        # Classic UUniFast algorithm:
        utilizations = []
        sumU = u
        for i in range(1, n):
            nextSumU = sumU * random.random() ** (1.0 / (n - i))
            utilizations.append(sumU - nextSumU)
            sumU = nextSumU
        utilizations.append(sumU)

        # If no task utilization exceeds 0.5:
        # HAEJOO: change this because heavy task(util>0.5) cannot be re-runed.
        if all(ut <= 0.5 for ut in utilizations):
            sets.append(utilizations)
    return sets

def SimpleRandom(n, nsets):
    """
        Simple Random algorithm
        generates task with utilization [0, task_max_utilization]
    """
    with open('cfg/task_cfg.json', 'r') as f:
        cfg = json.load(f)
    sets = []

    while len(sets) < nsets:
        utilizations = []
        for i in range(n):
            utilizations.append(random.random() * cfg['task_max_utilization'])
        sets.append(utilizations)

    return sets