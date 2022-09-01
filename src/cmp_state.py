import json
from generator.generator import generate_tasksets
from core.all_lockstep import get_num_core_LS
from core.ours import get_num_core_ours

def main():
    tasks = generate_tasksets()
    for task_set in tasks:
        with open('cfg/task_cfg.json', 'r') as f:
            cfg = json.load(f)

        stateless_ts = task_set.get_tasks(sort=True, desc=True)
        
        num_core_stateless = get_num_core_ours(stateless_ts)
        num_core_statewise = 0

        for state in range(cfg['num_states']):
            state_ts = task_set.get_tasks(sort=True, desc=True, state_num=state)
            num_core = get_num_core_ours(state_ts)

            if num_core_statewise < num_core:
                num_core_statewise = num_core

        print(num_core_stateless, num_core_statewise)

if __name__ == '__main__':
    main()