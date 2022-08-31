from generator.generator import generate_tasksets
from core.all_lockstep import get_num_core_LS
from core.ours import get_num_core_ours

def main():
    tasks = generate_tasksets()

    for task_set in tasks:
        stateless_ts = task_set.get_tasks(sort=True, desc=True)
        print(stateless_ts)
        num_core_LS = get_num_core_LS(stateless_ts)
        num_core_ours = get_num_core_ours(stateless_ts)

        print(num_core_LS, num_core_ours)

if __name__ == '__main__':
    main()