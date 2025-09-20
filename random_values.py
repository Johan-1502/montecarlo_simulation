from random_numbers_library.Random import Random

deviation = 1
medium = 1.5
min_value = 25
max_value = 45
random = Random()
#uniform_values = random.uniform(min_value, max_value, 300000, True)
#normal_values = random.normal(medium, deviation, 3000000)


def random_value():
    return random.random()
    
def norm_random_value():
    return random.normal(medium, deviation)
#    return normal_values.pop()

def uniform_value():
    return random.uniform(min_value, max_value, integer=True)
#    return uniform_values.pop()
