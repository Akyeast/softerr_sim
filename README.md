# synthetic-experiments
Experiments for synthetic workloads

## 실행방법
1. Lockstep만 돌리는거, PF without drop, PF with drop(ours) 비교하는거
    - `python3 src/cmp_rerun.py` 실행하면 실험내용 `output/rerun`에 저장됨
    - 실험을 위한 config들은 `cfg/state_exp_cfg.json`에 있어요
    - `vis/vis_rerun.ipynb`에서 output 시각화 가능

2. stateless, statewise(ours) 비교하는거
    - `python3 src/cmp_state.py` 실행하면 실험내용 `output/state`에 저장됨
    - 실험을 위한 config들은 `cfg/rerun_exp_cfg.json`에 있어요
    - `vis/vis_state.ipynb`에서 output 시각화 가능

## configs
- `num_task_sets`: 하나의 config당 총 몇번의 실험을 반복할지
- `num_tasks`: 한번의 실험에서 task set의 task를 몇개로 구성할지
- `critical_prob_list`: 이 리스트에 기반해 critical prob config 조합
- `period`: 두 값 사이의 uniform으로 task period 뽑음,
- `num_states_list`: 이 리스트에 기반해 state config 조합,
- `task_max_utilization`: 하나의 task가 가질 수 있는 최대 max utilzation
- ex) 만약에 `critical_prob_list`가 [0.0, 0.5, 1.0]이고 `num_states_list`이 [1, 2, 3]이면 총 9개의 config 조합에 대해 `num_task_sets`만큼 실험이 진행되고, 그 log가 저장되는 형태