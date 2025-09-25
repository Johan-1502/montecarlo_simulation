from random_library.Random import Random
import constants
import math

stddev = 1
mean = 1.5
min_value = 25
max_value = 45
random = Random()

quantity_unif_values = math.trunc(constants.QUANTITY_OF_GAMES*constants.QUANTITY_OF_ROUNDS + (constants.QUANTITY_OF_GAMES*constants.QUANTITY_OF_ROUNDS)*0.20)
quantity_norm_values = constants.QUANTITY_OF_TEAMS*constants.QUANTITY_OF_ARCHERS_BY_TEAM*quantity_unif_values

class Values:
    def __init__(self):
        self.uniform_values = random.uniform(min_value, max_value, quantity_unif_values, True)
        self.normal_values = random.normal(mean, stddev, quantity_norm_values)

    def random_value(self):
        return random.random()
        
    def norm_random_value(self):
        return self.normal_values.pop()

    def uniform_value(self):
        return self.uniform_values.pop()
