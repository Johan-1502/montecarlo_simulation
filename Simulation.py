from enum import Enum
from points_conversion import (
    PointsConverter,
    FemalePointsConverter,
    MalePointsConverter,
)
from score import Puntuation, PuntuationTeam
import constants
import random


class Gender(Enum):
    MALE = "masculino"
    FEMALE = "femenino"


class Archer:
    def __init__(
        self,
        name: str,
        initial_resistance: int,
        luck: float,
        gender: Gender,
        points_converter: PointsConverter,
    ):
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

    def execute_normal_shot(self, value: float, game: int, round: int) -> int:
        points = self.__add_points(value, game, round)
        self.decrease_resistence(constants.RESISTANCE_CONSUMPTION)
        return points

    def execute_additional_shot(self, value: float, game: int, round: int):
        self.__add_points(value, game, round)

    def __add_points(self, value: float, game: int, round: int):
        point = self.points_converter.obtain_point(value)
        puntuation = Puntuation(len(self.puntuations), game, round, point)
        self.puntuations.append(puntuation)
        self.total_points += puntuation.points
        return point

    def execute_special_shot(self, value: float) -> int:
        point = self.points_converter.obtainPoint(value)
        self.has_special_shot = True
        return point

    def decrease_resistence(self, unitsToRemove: int):
        self.current_resistance -= unitsToRemove
        self.used_resistance += unitsToRemove

    def can_continue(self) -> bool:
        return self.current_resistance >= constants.RESISTANCE_CONSUMPTION

    def add_experience(self, experience: int):
        self.current_experience += experience

    def restore_resistence(self, less_units: int):
        self.resistence = self.used_resistance - less_units
        self.current_resistance = self.resistence
        self.used_resistance = 0

    def experience_gained(self) -> int:
        return self.current_experience - self.initial_experience

    def clone(self):
        archerCloned = Archer(
            self.name,
            self.initial_resistance,
            self.luck,
            self.gender,
            self.points_converter,
        )
        archerCloned.current_experience = self.current_experience
        archerCloned.current_resistance = self.current_resistance
        archerCloned.has_special_shot = self.has_special_shot
        archerCloned.total_points = self.total_points
        archerCloned.used_resistance = self.used_resistance
        archerCloned.has_additional_shot = self.has_additional_shot


class Team:
    def __init__(self, name: str):
        self.name = name
        self.archers = []
        self.total_points = 0
        self.total_special_shots = 0
        self.puntuations = []

    def add_archer(self, archer: Archer):
        self.archers.append(archer)

    def add_puntuation(
        self,
        game: int,
        round: int,
    ):
        self.puntuations.append(
            PuntuationTeam(
                len(self.puntuations),
                game,
                round,
                self.total_points,
                self.__total_experience_gained(),
                self.total_special_shots,
            )
        )

    def add_points(self, points: int):
        self.total_points += points

    def __total_experience_gained(self) -> int:
        total_experience = 0
        for archer in self.archers:
            total_experience += archer.experience_gained()
        return total_experience

    def add_special_shot(self):
        self.total_special_shots += 1

    def the_most_lucky_archer(self):
        most_lucky_archer = None
        for archer in self.archers:
            if most_lucky_archer:
                if archer.luck > most_lucky_archer.luck:
                    most_lucky_archer = archer
            else:
                most_lucky_archer = archer
        return most_lucky_archer

    def the_most_experienced_archer(self):
        most_experienced_archer = None
        for archer in self.archers:
            if most_experienced_archer:
                if (
                    archer.current_experience
                    > most_experienced_archer.current_experience
                ):
                    most_experienced_archer = archer
            else:
                most_experienced_archer = archer
        return most_experienced_archer

    def best_archer_points(self):
        best_archers = list()
        for archer in self.archers:
            if len(best_archers) > 0:
                if archer.total_points > best_archers[0].total_points:
                    best_archers = list()
                    best_archers.append(archer)
                elif archer.total_points == best_archers[0].total_points:
                    best_archers.append(archer)
            else:
                best_archers.append(archer)
        return list(set(best_archers))


class Round:
    def __init__(self, id: int, game: int):
        self.id = id
        self.game_id = game
        self.isATiedRound = False
        self.best_archer = None
        self.best_team = None
        self.mostLuckyArcher = None

    def execute(self, teams):
        for team in teams:
            for archer in team.archers:
                self.compare_luck(archer)
                # print(f"Jugador: {archer.name}\n")
                while archer.can_continue():
                    self.add_points(archer, team)
                    # print(f" Puntos obtenidos: {archer.total_points}")
                # print(f" resitencia final: {archer.current_resistance}\n\n Puntos finales: {archer.total_points}")

    def compare_luck(self, archer):
        if self.mostLuckyArcher:
            if archer.luck > self.mostLuckyArcher.luck:
                self.mostLuckyArcher = archer

    def add_points(self, archer, team):
        points_archer = archer.execute_normal_shot(
            self.random_shot_value(), self.game_id, self.id
        )
        team.add_points(points_archer)

    def random_shot_value(self):
        return random.random()

    def define_winning_team(self, teams):
        for team in teams:
            if self.best_team:
                if team.total_points > self.best_team.total_points:
                    self.best_team = team
            else:
                self.best_team = team

    def define_winning_archer(self, teams):
        best_archers = list()
        for team in teams:
            best_archers_team = team.best_archer_points()
            if len(best_archers) > 0:
                if best_archers_team[0].total_points > best_archers[0].total_points:
                    best_archers = list(best_archers_team)
                elif best_archers_team[0].total_points == best_archers[0].total_points:
                    best_archers.extend(best_archers_team)
            else:
                best_archers = list(best_archers_team)
        if len(best_archers) == 1:
            self.best_archer = best_archers[0]
        return best_archers

    def set_best_archer(self, best_archer: Archer):
        self.best_archer = best_archer

    def getMostLuckyArcher(self) -> Archer:
        return self.mostLuckyArcher