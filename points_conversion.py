from abc import ABC, abstractmethod
from enum import Enum

class Gender(Enum):
    """
    Enúmerado de generos.
    """
    MALE = "Masculino"
    FEMALE = "Femenino"

class PointsConverter(ABC):
    """
    Clase abstracta encargada de convertir los puntos
    """
    @abstractmethod
    def obtain_point(self, value:float) -> int:
        """
        Devuelve el puntaje obtenido a partir del valor aletorio pasado por parámetro
        
        Args:
            value (float): valor aleatorio obtenido el cual se utilizará para convertir y definir el puntaje obtenido
            
        Returns:
            int: puntaje obtenido a partir del valor aleatorio
        """
        pass
    
class FemalePointsConverter(PointsConverter):
    """
    Conversor de puntos para el género femenino
    """
    def obtain_point(self, value:float):
        """
        Devuelve el puntaje obtenido a partir del valor aletorio pasado por parámetro aplicando la matriz de probabilidades definida para el género femenino
        
        Args:
            value (float): valor aleatorio obtenido el cual se utilizará para convertir y definir el puntaje obtenido
            
        Returns:
            int: puntaje obtenido a partir del valor aleatorio
        """
        if value <= 0.25:
            return 10
        elif value <= 0.65:
            return 9
        elif value <= 0.95:
            return 8
        else:
            return 0
        
class MalePointsConverter(PointsConverter):
    """
    Conversor de puntos para el género másculino
    """
    def obtain_point(self, value):
        """
        Devuelve el puntaje obtenido a partir del valor aletorio pasado por parámetro aplicando la matriz de probabilidades definida para el género másculino
        
        Args:
            value (float): valor aleatorio obtenido el cual se utilizará para convertir y definir el puntaje obtenido
            
        Returns:
            int: puntaje obtenido a partir del valor aleatorio
        """
        if value <= 0.15:
            return 10
        elif value <= 0.45:
            return 9
        elif value <= 0.92:
            return 8
        else:
            return 0
        
class SubstractResistanceConverter(PointsConverter):
    """
    Conversor de puntos para definir la cantidad de resitencia a restar al momento de restaurarla
    """
    def obtain_point(self, value):
        """
        Devuelve el valor a restar a partir del valor aletorio pasado por parámetro dependiendo del rango en que se encuentre este valor
        
        Args:
            value (float): valor aleatorio obtenido el cual se utilizará para convertir y definir el puntaje obtenido
            
        Returns:
            int: valor a restar a partir del valor aleatorio
        """
        if value <= 0.33:
            return 1
        elif value <= 0.66:
            return 2
        else:
            return 3
        

def obtain_gender(value):
    """
    Devuelve el género a asignar del valor aletorio pasado por parámetro 
    
    Args:
        value (float): valor aleatorio obtenido el cual se utilizará para convertir y definir el género a asignar
        
    Returns:
        Gender: Género a asignar
    """
    if value <= 0.5:
        return Gender.FEMALE
    else:
        return Gender.MALE