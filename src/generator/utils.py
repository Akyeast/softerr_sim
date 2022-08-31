import random

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