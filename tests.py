from simulation import Team, Archer, Gender, Round
from points_conversion import MalePointsConverter, FemalePointsConverter
import constants

class RoundTest:
    def test():    
        teams = []

        team_1 = Team("Team 1")
        team_1.add_archer(Archer("Archer 1",team_1.name, 27, 1.09, Gender.MALE, MalePointsConverter()))
        team_1.add_archer(Archer("Archer 2",team_1.name, 37, 1.19, Gender.FEMALE, FemalePointsConverter()))
        teams.append(team_1)

        team_2 = Team("Team 2")
        team_2.add_archer(Archer("Archer 3",team_2.name, 32, 1.8, Gender.MALE, MalePointsConverter()))
        team_2.add_archer(Archer("Archer 4",team_2.name, 39, 1.29, Gender.FEMALE, FemalePointsConverter()))
        teams.append(team_2)

        round = Round(1, 1)
        round.execute(teams)

#var = []
#var.append({constants.NAME_ATRIBUTE:"Johan", constants.EXPERIENCE:10})
#var.append({constants.NAME_ATRIBUTE:"Johan", constants.EXPERIENCE:10})
#
#print(var[0][constants.NAME_ATRIBUTE])
#
#RoundTest.test()
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