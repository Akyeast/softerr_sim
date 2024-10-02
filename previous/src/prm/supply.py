import math

def sbf(pi, theta, t, m=2):
    remain = pi - theta
    epsilon = max(t - 2*remain - pi*math.floor((t-remain) / pi), 0)
    return m * (math.floor((t-remain)/pi) * theta + epsilon)

def lsbf(pi, theta, t, m=2):
    return m * (theta / pi) * (t - 2*(pi-theta))