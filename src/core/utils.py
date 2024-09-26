import math

def argmin(lst, array=False):
    srt_lst = sorted(range(len(lst)), key=lambda k: lst[k])
    
    if array:
        return srt_lst
    else :
        return srt_lst[0]

def argmax(lst, array=False):
    srt_lst = sorted(range(len(lst)), key=lambda k: lst[k], reverse=True)
    
    if array:
        return srt_lst
    else :
        return srt_lst[0]
    
def lcm(lst):
    _lcm = 1
    for i in lst:
        _lcm = _lcm*i // math.gcd(_lcm, i)
    return _lcm