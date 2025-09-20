from simulation import Team, Archer, Round, Game, Tournament
from points_conversion import MalePointsConverter, FemalePointsConverter,Gender, obtain_gender
import constants
from random_values import uniform_value, norm_random_value, random_value
import time
from datetime import timedelta

array = []

def add_value():
    array.append(1)
        
def value():
    return array.pop()

class RoundTest:
    def test():    
        teams = []

        for i in range(constants.QUANTITY_OF_TEAMS):    
            team = Team(f"Team {(i+1)}")
            for j in range(constants.QUANTITY_OF_ARCHERS_BY_TEAM):    
                gender = obtain_gender(random_value())
                points_converter = None
                if gender == Gender.MALE:
                    points_converter = MalePointsConverter()
                else:
                    points_converter = FemalePointsConverter()
                team.add_archer(Archer(f"Archer {(j+1)}",team.name, uniform_value(), norm_random_value(), gender, points_converter))
            teams.append(team)

        print("Ejecución iniciada")
        start_time = time.time()
        for i in range(constants.QUANTITY_OF_GAMES):
            porcentaje = (i + 1) / constants.QUANTITY_OF_GAMES * 100
            print(f"\rProgreso: {porcentaje:.1f}% ({i + 1}/{constants.QUANTITY_OF_GAMES})", end="", flush=True)
            game = Game(i)
            game.execute(teams)
        
        end_time = time.time()
        execution_time = end_time - start_time
        tiempo_formateado = str(timedelta(seconds=execution_time))
        print(f"\nTiempo de ejecución: {tiempo_formateado}")
        print("Ejecución terminada")
        
    def execute_tournament():
        tournament = Tournament()
        tournament.execute()


#var = []
#var.append({constants.NAME_ATRIBUTE:"Johan", constants.EXPERIENCE:10})
#var.append({constants.NAME_ATRIBUTE:"Johan", constants.EXPERIENCE:10})
#
#print(var[0][constants.NAME_ATRIBUTE])
#
#Test de un conjunto con set()

#class Person:
#    def __init__(self, name, age):
#        self.name = name
#        self.age = age
#
#people = list()
#person = Person("Carlos", 15)
#people.append(person)
#people.append(person)
#people.append(Person("Ángela", 15))
#people.append(Person("Danna", 15))
#print(len(people))
#
#
#set = set()
#set.update(people)
#print(len(set))
#print(f"Nombre: {people[0].name}, edad: {people[0].age}\n")


#
#print("Lista:")
#for person in people:
#    print(f"Nombre: {person.name}, edad: {person.age}\n")
#    
#print("Set:")
#people2 = set(people)
#for person in people2:
#    print(f"Nombre: {person.name}, edad: {person.age}\n")

#tied_people = set()
#oldest_person = None
#for person in people:
#    if oldest_person:
#        if person.age > oldest_person.age:
#            print("Mayor")
#            oldest_person = person
#            tied_archers = []
#        elif person.age == oldest_person.age:
#            print("Igual")
#            tied_people.add(oldest_person)
#            tied_people.add(person)
#    else:
#        oldest_person = person
#    
#print(len(tied_people))
#for person in tied_people:
#    print(f"Nombre: {person.name}, edad: {person.age}\n")