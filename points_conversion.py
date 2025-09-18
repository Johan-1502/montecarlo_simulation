from abc import ABC, abstractmethod

class PointsConverter(ABC):
    @abstractmethod
    def obtain_point(self, value:float) -> int:
        pass
    
class FemalePointsConverter(PointsConverter):
    def obtain_point(self, value:float):
        if value <= 0.25:
            return 10
        elif value <= 0.65:
            return 9
        elif value <= 0.95:
            return 8
        else:
            return 0
        
class MalePointsConverter(PointsConverter):
    def obtain_point(self, value):
        if value <= 0.15:
            return 10
        elif value <= 0.45:
            return 9
        elif value <= 0.92:
            return 8
        else:
            return 0
        
class SubstractResistanceConverter(PointsConverter):
    def obtain_point(self, value):
        if value <= 0.33:
            return 1
        elif value <= 0.66:
            return 2
        else:
            return 3