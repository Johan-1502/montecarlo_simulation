import random, math

deviation = 1
medium = 1.5
min_value = 25
max_value = 45

def random_value():
    return random.random()
    
def norm_random_value():
    return (1/(math.sqrt(2*math.pi)*deviation))*math.exp(-(1/2)*math.pow(((random_value()-medium)/deviation), 2))

def uniform_value():
    return math.trunc(min_value+(max_value - min_value)*random_value())
