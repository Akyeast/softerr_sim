import scipy.stats as stats

def probability_exceeding(e, p, u):
    # 정규분포의 평균과 분산을 계산
    mean = p * (1 - u)
    variance = p * (1 - u) * u
    stddev = variance ** 0.5  # 분산의 제곱근이 표준편차

    # mean = (1 - u)
    # variance = (1 - u) * u
    # stddev = variance ** 0.5  # 분산의 제곱근이 표준편차
    
    # 정규분포 객체 생성
    norm_dist = stats.norm(loc=mean, scale=stddev)
    
    # CDF를 사용하여 e 이하의 확률을 계산한 후, 이를 1에서 빼서 e 초과의 확률을 구함
    probability = 1 - norm_dist.cdf(e)
    # probability = 1 - norm_dist.cdf(e/p)
    
    return probability

# 예시 사용
p = 1000  # period
u = 0.80  # total utilization
e = 100    # execution time

# 값이 e를 넘을 확률
exceed_probability = probability_exceeding(e, p, u)
print(f"The probability of exceeding {e} is {exceed_probability:.30f}")
# print(f"The probability of exceeding {e/p} is {exceed_probability:.30f}")