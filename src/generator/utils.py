import random
import json

def UUniFastDiscard(n, u, nsets, max_utils):
    sets = []
    while len(sets) < nsets:
        # Classic UUniFast algorithm:
        utilizations = []
        sumU = u
        for i in range(1, n):
            nextSumU = sumU * random.random() ** (1.0 / (n - i))
            utilizations.append(sumU - nextSumU)
            sumU = nextSumU

        # If no task utilization exceeds 0.5:
        # HAEJOO: change this because heavy task(util>0.5) cannot be re-runed.
        if all(ut <= max_utils for ut in utilizations):
            sets.append(utilizations)
    return sets

def SimpleRandom(n, nsets, max_utils):
    """
        Simple Random algorithm
        generates task with utilization [0, task_max_utilization]
    """
    sets = []
    
    for _ in range(nsets):
        utilizations = []
        for _ in range(n):
            utilizations.append(random.random() * max_utils)
        sets.append(utilizations)
    

    return sets

def SimpleFixed(n, nsets, max_utils):
    """
        Simple Random algorithm
        generates task with utilization [0, task_max_utilization]
    """
    sets = []
    
    for _ in range(nsets):
        utilizations = []
        for _ in range(n):
            utilizations.append(max_utils)
        sets.append(utilizations)
    

    return sets