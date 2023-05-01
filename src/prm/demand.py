import math

class Demand() :
    def __init__(self, tasks):
        self.tasks = tasks # [(period, execution, critical), (5, 3, 0), ...]

    def maximum_A_k(self, k, theta, pi) :
        sum_utilization = sum([task[1] / task[0] for task in self.tasks])
        max_exct = max([task[1] for task in self.tasks])
        slope = (2*theta) / pi
        B = 2 * slope * (pi - theta)
        D = self.tasks[k][0] * (slope - sum_utilization)
        return (max_exct + 2 * self.tasks[k][1] + B - D) / (slope - sum_utilization)

    def number_of_jobs(self, t, i): # N_i(t)
        return math.floor(t / self.tasks[i][0])

    def carry_in(self, t, i): # CI_i(t)
        return min(self.tasks[i][1], max(0, t - self.number_of_jobs(t, i) * self.tasks[i][0]))

    def workload(self, t, i): # W_i(t)
        body_job = self.number_of_jobs(t, i) * self.tasks[i][1]
        return body_job + self.carry_in(t, i)

    def interference_bar(self, i, k, A_k): # bar{I}_{i, 2} or bar{I}_{k, 2}
        period, exct, _ = self.tasks[k]
        if i != k :
            return min(self.workload(A_k+period, i), A_k + period - exct)
        else :
            return min(self.workload(A_k+period, k) - exct, A_k)

    def interference_hat(self, i, k, A_k):  # hat{I}_{i, 2} or hat{I}_{k, 2}
        period, exct, _ = self.tasks[k]
        t = A_k + period
        if i != k :
            return min(self.workload(t, i) - self.carry_in(t, i), A_k + period - exct)
        else :
            return min(self.workload(t, k) - exct - self.carry_in(t, k), A_k)

    def demand(self, A_k, k) : # demand(A_k+D_k, k)
        m = 2
        task_len = len(self.tasks)
        body_job_sum = sum([self.interference_hat(i, k, A_k) for i in range(task_len)])
        carry_in_job_sum = max([self.interference_bar(i, k, A_k) - self.interference_hat(i, k, A_k) for i in range(task_len)])
        return body_job_sum + carry_in_job_sum + m * self.tasks[k][1]


if __name__ == '__main__':
    demand = Demand([(70, 5, 0), (70, 5, 0)])
    print("0: ", demand.demand(0, 0), demand.demand(0, 1))
    print("1: ", demand.demand(1, 0), demand.demand(1, 1))
    print("2: ", demand.demand(2, 0), demand.demand(2, 1))
    print("3: ", demand.demand(3, 0), demand.demand(3, 1))
    print("4: ", demand.demand(4, 0), demand.demand(4, 1))
    print("5: ", demand.demand(5, 0), demand.demand(5, 1))
    print("6: ", demand.demand(6, 0), demand.demand(6, 1))
    print("7: ", demand.demand(7, 0), demand.demand(7, 1))
    print("8: ", demand.demand(8, 0), demand.demand(8, 1))
    print("9: ", demand.demand(9, 0), demand.demand(9, 1))
    print("10: ", demand.demand(10, 0), demand.demand(10, 1))