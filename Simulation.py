from enum import Enum
from points_conversion import (
    PointsConverter,
    FemalePointsConverter,
    MalePointsConverter,
    SubstractResistanceConverter,
)
from score import Puntuation, PuntuationTeam
import constants
import random
from random_values import random_value, norm_random_value, lineal_value


class Gender(Enum):
    MALE = "masculino"
    FEMALE = "femenino"


class Archer:
    def __init__(
        self,
        name: str,
        team: str,
        initial_resistance: int,
        luck: float,
        gender: Gender,
        points_converter: PointsConverter,
    ):
        self.name = name
        self.team = team
        self.initial_experience = constants.INITIAL_EXPERIENCE
        self.luck = luck
        self.gender = gender
        self.points_converter = points_converter
        self.current_resistance = initial_resistance
        self.current_experience = self.initial_experience
        self.total_points = 0
        self.used_resistance = 0
        self.puntuations = []

    def execute_normal_shot(self, value: float, game: int, round: int) -> int:
        points = self.__add_points(value, game, round)
        self.decrease_resistence(constants.RESISTANCE_CONSUMPTION)
        return points

    def execute_additional_shot(self, value: float, game: int, round: int) -> int:
        return self.__add_points(value, game, round)

    def __add_points(self, value: float, game: int, round: int):
        point = self.points_converter.obtain_point(value)
        puntuation = Puntuation(len(self.puntuations), game, round, point)
        self.puntuations.append(puntuation)
        self.total_points += puntuation.points
        return point

    def execute_special_shot(self, value: float) -> int:
        point = self.points_converter.obtain_point(value)
        return point

    def decrease_resistence(self, unitsToRemove: int):
        self.current_resistance -= unitsToRemove
        self.used_resistance += unitsToRemove

    def can_continue(self) -> bool:
        return self.current_resistance >= constants.RESISTANCE_CONSUMPTION

    def add_experience(self, experience: int):
        self.current_experience += experience

    def restore_resistence(self, less_units: int):
        self.current_resistance = self.used_resistance - less_units
        self.used_resistance = 0

    def experience_gained(self) -> int:
        return self.current_experience - self.initial_experience

    def reset_round_values(self, less_units: int, luck_value: float):
        self.restore_resistence(less_units)
        self.luck = luck_value
        self.total_points = 0
        
    def reset_values(self, luck:float, resistance:int):
        self.initial_experience = constants.INITIAL_EXPERIENCE
        self.luck = luck
        self.current_resistance = resistance
        self.current_experience = self.initial_experience
        self.total_points = 0
        self.used_resistance = 0


class Team:
    def __init__(self, name: str):
        self.name = name
        self.archers: list[Archer] = []
        self.total_points = 0
        self.total_special_shots = 0
        self.puntuations: list[PuntuationTeam] = []
        self.special_archer = None

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

    def set_special_archer(self, archer: Archer):
        self.special_archer = archer

    def reset_values(self):
        self.total_points = 0
        self.total_special_shots = 0
        self.special_archer = None


class Round:
    def __init__(self, id: int, game: int):
        self.id = id
        self.game_id = game
        self.isATiedRound = False
        self.best_archer:dict = None
        self.best_team:dict = None
        self.luckiest_archer:dict = None

    def execute(self, teams: list[Team]):
        self.make_shots(teams)
        most_lucky_archers = self.obtain_most_lucky_archers(teams)
        self.execute_special_shots(most_lucky_archers, teams, self.id)
        # VALIDAR QUÉ SUCEDE CUANDO HAY EMPATE
        self.define_winning_team(teams)
        self.define_winning_archer(teams)
        self.save_team_points(teams)
        self.restore_values(teams)

    def save_team_points(self, teams: list[Team]):
        for team in teams:
            team.add_puntuation(self.game_id, self.id)

    def restore_values(self, teams: list[Team]):
        substractConverter = SubstractResistanceConverter()
        for team in teams:
            for archer in team.archers:
                if archer.experience_gained >= 9:
                    archer.reset_round_values(
                        constants.DEFAULT_EXPERIENCE_TO_SUBSTRACT, norm_random_value()
                    )
                else:
                    archer.reset_round_values(
                        substractConverter.obtain_point(random_value()),
                        norm_random_value(),
                    )
            team.reset_values()

    def verify_tie(self, archers: list[Archer], teams: list[Team]):
        best_archers: list[Archer] = list()
        for archer in archers:
            if len(best_archers) > 0:
                if archer.total_points > best_archers[0].total_points:
                    best_archers = list()
                    best_archers.append(archer)
                elif archer.total_points == best_archers[0].total_points:
                    best_archers.append(archer)
            else:
                best_archers = list()
                best_archers.append(archer)
        if len(best_archers) == 1:
            self.set_winner_archer(best_archers[0])
        elif len(best_archers) > 1:
            self.execute_additional_shots(archers, teams)

    def execute_additional_shots(self, archers: list[Archer], teams: list[Team]):
        for archer in archers:
            points = archer.execute_additional_shot(
                random_value(), self.game_id, self.id
            )
            team = self.searchTeam(archer.team, teams)
            team.add_points(points)
        self.verify_tie(archers, teams)

    def set_winner_archer(self, archer: Archer):
        self.best_archer = {
            constants.NAME_ATRIBUTE: archer.name,
            constants.PUNTUATION_ATRIBUTE: archer.total_points,
            constants.GENDER: archer.gender
        }
        archer.add_experience(3)

    def make_shots(self, teams: list[Team]):
        for team in teams:
            self.make_archers_shots(team)

    def make_archers_shots(self, team: Team):
        for archer in team.archers:
            self.compare_luck(archer)
            # print(f"Jugador: {archer.name}\n")
            while archer.can_continue():
                self.add_points(archer, team)
                # print(f" Puntos obtenidos: {archer.total_points}")
            # print(f" resitencia final: {archer.current_resistance}\n\n Puntos finales: {archer.total_points}")

    def execute_special_shots(
        self, most_lucky_archers: list[Archer], teams: list[Team], round: int
    ):
        for archer in most_lucky_archers:
            points = archer.execute_special_shot(random_value())
            team = self.searchTeam(archer.team, teams)
            self.validate_additional_shot(team, archer, round)
            team.add_special_shot()
            team.add_points(points)

    def validate_additional_shot(self, team: Team, archer: Archer, round: int):
        if team.special_archer:
            if team.special_archer.name == archer.name:
                additional_point = archer.execute_additional_shot(
                    random_value(), self.id, round
                )
                team.add_points(additional_point)
            else:
                team.set_special_archer(archer)
        else:
            team.set_special_archer(archer)

    def searchTeam(self, name: str, teams: list[Team]) -> Team:
        for team in teams:
            if team.name == name:
                return team
        return None

    def obtain_most_lucky_archers(self, teams: list[Team]) -> list[Archer]:
        most_lucky_archers = []
        for team in teams:
            most_lucky_archers.append(team.the_most_lucky_archer())
        return most_lucky_archers

    def compare_luck(self, archer: Archer):
        if self.luckiest_archer:
            if archer.luck > self.luckiest_archer[constants.LUCK]:
                self.luckiest_archer = {
                    constants.NAME_ATRIBUTE: archer.name,
                    constants.LUCK: archer.luck,
                }

    def add_points(self, archer: Archer, team: Team):
        points_archer = archer.execute_normal_shot(
            random_value(), self.game_id, self.id
        )
        team.add_points(points_archer)

    def define_winning_team(self, teams: list[Team]):
        for team in teams:
            if self.best_team:
                if team.total_points > self.best_team[constants.PUNTUATION_ATRIBUTE]:
                    self.isATiedRound = False
                    self.best_team = {
                        constants.NAME_ATRIBUTE: team.name,
                        constants.PUNTUATION_ATRIBUTE: team.total_points,
                    }
                elif team.total_points == self.best_team[constants.PUNTUATION_ATRIBUTE]:
                    self.best_team = None
                    self.isATiedRound = True
                    print("Equipos empatados")
            else:
                self.best_team = {
                    constants.NAME_ATRIBUTE: team.name,
                    constants.PUNTUATION_ATRIBUTE: team.total_points,
                }

    def define_winning_archer(self, teams: list[Team]):
        best_archers: list[Archer] = list()
        for team in teams:
            best_archers_team: list[Archer] = team.best_archer_points()
            if len(best_archers) > 0:
                if best_archers_team[0].total_points > best_archers[0].total_points:
                    best_archers = list(best_archers_team)
                elif best_archers_team[0].total_points == best_archers[0].total_points:
                    best_archers.extend(best_archers_team)
            else:
                best_archers = list(best_archers_team)
        if len(best_archers) == 1:
            self.set_winner_archer(best_archers[0])
        elif len(best_archers) > 1:
            self.execute_additional_shots(best_archers, teams)

    def get_luckiest_archer(self) -> Archer:
        return self.luckiest_archer


class Game:
    def __init__(self, id: int):
        self.id = id
        self.rounds: list[Round] = []
        self.the_luckiest_archer = None
        self.the_most_experienced_archers = []
        self.bestTeam = None
        self.bestArcher = None
        self.male_wins = 0
        self.female_wins = 0
        self.quantityOfTiedRounds = 0

    def execute(self, teams: list[Team]):
        self.execute_rounds(teams)

    def execute_rounds(self, teams: list[Team]):
        for i in range(constants.QUANTITY_OF_ROUNDS):
            round = Round(i, self.id)
            self.rounds.append(round)
            round.execute(teams)
            self.define_winner_team()
            self.define_winner_archer()
            self.define_luckiest_archer()
            self.define_most_experienced_archers(teams)
            self.count_victories_by_gender()
            self.reset_values(teams)

    def define_winner_team(self):
        best_teams = self.count_victories_by_team()
        self.bestTeam = self.define_winner(best_teams, constants.ROUNDS_WON)
        if not self.bestTeam:
            print(f"Empate de equipos en el juego {self.id}")

    def count_victories_by_team(self):
        list = []
        for round in self.rounds:
            if round.best_team:
                team_name = round.best_team[constants.NAME_ATRIBUTE]
                team = self.search_item(list, team_name)
                self.add_won_round(team, team_name)
            elif round.isATiedRound:
                self.quantityOfTiedRounds += 1
        return list

    def define_winner_archer(self):
        best_archers = self.count_victories_by_archer()
        self.bestArcher = self.define_winner(best_archers, constants.ROUNDS_WON)
        if not self.bestArcher:
            print(f"Empate de jugadores en el juego {self.id}")

    def count_victories_by_archer(self):
        list = []
        for round in self.rounds:
            if round.best_archer:
                archer_name = round.best_archer[constants.NAME_ATRIBUTE]
                archer = self.search_item(list, archer_name)
                self.add_won_round(archer, archer_name, list)
        return list

    def add_won_round(self, object, object_name, list: list):
        if object:
            object[constants.ROUNDS_WON] += 1
        else:
            list.append({constants.NAME_ATRIBUTE: object_name, constants.ROUNDS_WON: 1})

    def define_winner(self, best_participants, criterion):
        winner = None
        for participant in best_participants:
            if winner:
                if participant[criterion] > winner[criterion]:
                    winner = participant
                elif participant[criterion] == winner[criterion]:
                    winner = None
            else:
                winner = participant
        return winner

    def search_item(self, list, name):
        for object in list:
            if object[constants.NAME_ATRIBUTE] == name:
                return object
        return None

    def define_luckiest_archer(self):
        luckiest_archers = self.obtain_luckiest_archers()
        self.the_luckiest_archer = self.define_winner(luckiest_archers, constants.LUCK)
        if not self.the_luckiest_archer:
            print(f"Empate de jugador afortunado en el juego {self.id}")

    def obtain_luckiest_archers(self):
        luckiest_archers = []
        for round in self.rounds:
            luckiest_archers.append(round.luckiest_archer)
        return luckiest_archers

    def define_most_experienced_archers(self, teams: list[Team]):
        most_experienced_archers = []
        for team in teams:
            for archer in team.archers:
                experience_gained = archer.experience_gained()
                self.compare_experience(experience_gained, archer)
        self.the_most_experienced_archers = most_experienced_archers

    def compare_experience(self, experience_gained: int, archer: Archer):
        if len(most_experienced_archers) > 0:
            if experience_gained > most_experienced_archers[0][constants.EXPERIENCE]:
                most_experienced_archers = []
                self.add_object_to_list(
                    most_experienced_archers,
                    archer,
                    constants.EXPERIENCE,
                    experience_gained,
                )
            elif experience_gained == most_experienced_archers[constants.EXPERIENCE]:
                self.add_object_to_list(
                    most_experienced_archers,
                    archer,
                    constants.EXPERIENCE,
                    experience_gained,
                )
        else:
            self.add_object_to_list(
                most_experienced_archers,
                archer,
                constants.EXPERIENCE,
                experience_gained,
            )

    def add_object_to_list(
        self, list: list, object: Archer, criterion_value, value: int
    ):
        list.append(
            {
                constants.NAME_ATRIBUTE: object.name,
                criterion_value: value,
            }
        )

    def count_victories_by_gender(self):
        for round in self.rounds:
            winner = round.best_archer
            if winner:
                if winner[constants.GENDER] == Gender.MALE:
                    self.male_wins += 1
                else:
                    self.female_wins += 1
                    
    def reset_values(self, teams:list[Team]):
        for team in teams:
            for archer in team.archers:
                archer.reset_values(norm_random_value(), lineal_value())
            team.reset_values()
            