from core.mapping import critical2core
from core.utils import get_minimum_core, get_PRM_bound

def get_num_core_ours(tasks):
    """
        Input: 
            [(period, execution, critical), (5, 3, 1), ...]
        Output:
            minimum required core number
    """
    mim_core = get_minimum_core(tasks)
    mapped_tasks, assigned_cores = critical2core(tasks, mim_core)
    prms = get_PRM_bound(assigned_cores)
    
    return prms