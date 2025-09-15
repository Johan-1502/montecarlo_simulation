from enum import Enum
from points_conversion import points_converter
from score import Puntuation
import constants
 
class Gender(Enum):
    MALE = "masculino"
    FEMALE = "femenino"

class Archer:
    def __init__(self, name:str, initial_resistance:int, luck:float, gender:Gender, points_converter:points_converter):
        self.name = name 
        self.initial_resistance = initial_resistance
        self.initial_experience = constants.INITIAL_EXPERIENCE
        self.luck = luck
        self.gender = gender
        self.points_converter = points_converter
        self.current_resistance = initial_resistance
        self.current_experience = self.initial_experience
        self.has_special_shot = False
        self.total_points = 0
        self.used_resistance = 0
        self.has_additional_shot = False
        self.puntuations = []
    
    def execute_normal_shot(self, value:float, game:int, round:int):
        self.__add_points(value, game, round)
        self.decrease_resistence(constants.RESISTANCE_CONSUMPTION)
        
    def execute_additional_shot(self, value:float, game:int, round:int):
        self.__add_points(value, game, round)
    
    def __add_points(self, value:float, game:int, round:int):
        point = self.points_converter.obtainPoint(value)
        puntuation = Puntuation(len(self.puntuations),game, round, point)
        self.puntuations.append(puntuation)
        self.total_points += puntuation
    
    def execute_special_shot(self, value:float) -> int:
        point = self.points_converter.obtainPoint(value)
        self.has_special_shot = True
        return point
    
    def decrease_resistence(self, unitsToRemove:int):
        self.current_resistance-=unitsToRemove
        self.used_resistance+=unitsToRemove
        
    def can_continue(self) -> bool: 
        return self.current_resistance >= constants.RESISTANCE_CONSUMPTION
    
    def add_experience(self, experience:int):
        self.current_experience += experience
        
    def restore_resistence(self, less_units:int):
        self.resistence = self.used_resistance-less_units
        self.current_resistance = self.resistence
        self.used_resistance = 0
        
    def experience_gained(self) -> int:
        return self.current_experience - self.initial_experience
    
    def clone(self):
        archerCloned = Archer(self.name, self.initial_resistance, self.luck, self.gender, self.points_converter)
        archerCloned.current_experience = self.current_experience
        archerCloned.current_resistance = self.current_resistance
        archerCloned.has_special_shot = self.has_special_shot
        archerCloned.total_points = self.total_points
        archerCloned.used_resistance = self.used_resistance
        archerCloned.has_additional_shot = self.has_additional_shot
        