import random

class Task():
    def __init__(self, period, execution, criticality):
        self.period = period
        self.execution = execution
        self.utilization = execution / period
        self.criticality = criticality
        self.critical_factor = max(criticality)

    def __str__(self):
        return "Task(period={}, execution={}, criticality={})\n".format(self.period, self.execution, self.criticality)
    
    def __repr__(self):
        return self.__str__()

    def get_task(self, state_num=None):
        if state_num is None:
            critical = max(self.criticality)
        else:
            critical = self.criticality[state_num]

        return (self.period, self.execution, critical)


class TaskSet():
    def __init__(self, tasks):
        self.tasks = tasks

    def append(self, task):
        self.tasks.append(task)
    
    def get_tasks(self, state_num=None, sort=False, desc=True) :
        tasks = [task.get_task(state_num) for task in self.tasks] 
        if sort:
            tasks.sort(key=lambda x: x[1]/x[0], reverse=desc)
        return tasks
    
    def assign_new_criticality(self, num_states):
        for i in range(len(self.tasks)):
            if self.tasks[i].critical_factor == 1:
                self.tasks[i].criticality = [1 if random.random() < 0.5 else 0 for _ in range(num_states)]
                if max(self.tasks[i].criticality) == 0:
                    self.tasks[i].criticality[random.randint(0, num_states-1)] = 1
            else:
                self.tasks[i].criticality = [0 for _ in range(num_states)]
        

    def __str__(self):
        return "TaskSet:\n{}".format(self.tasks)

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.tasks)