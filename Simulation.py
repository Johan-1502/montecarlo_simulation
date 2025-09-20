from points_conversion import (
    PointsConverter,
    FemalePointsConverter,
    MalePointsConverter,
    SubstractResistanceConverter,
    Gender,
    obtain_gender,
)
from score import Puntuation, PuntuationTeam
import constants
import math
from random_values import random_value, norm_random_value, uniform_value


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
        self.quantity_luckiest_games = 0
        self.quantity_experienced_games = 0
        self.puntuations = []
        self.round_points = []
        self.acumulation_points = []

    def add_puntuation_round(self, id: int, points: int):
        if len(self.round_points) > 0:
            for round in self.round_points:
                if round["id"] == id:
                    round["points"] += points
        else:

            self.round_points.append({"id": id, "points": points})

    def execute_normal_shot(self, value: float, game: int, round: int) -> int:
        points = self.__add_points(value, game, round)
        self.decrease_resistence(constants.RESISTANCE_CONSUMPTION)
        return points

    def execute_additional_shot(self, value: float, game: int, round: int) -> int:
        return self.__add_points(value, game, round)

    def __add_points(self, value: float, game: int, round: int):
        point = self.points_converter.obtain_point(value)
        self.add_puntuation_round(round, point)
        puntuation = Puntuation(len(self.puntuations), game, round, point)
        self.puntuations.append(puntuation)
        self.total_points += puntuation.points
        return point

    def acumulate_points(self):
        if len(self.acumulation_points) > 0:
            last_position = len(self.acumulation_points) - 1
            self.acumulation_points.append(
                self.acumulation_points[last_position] + self.total_points
            )
        else:
            self.acumulation_points.append(self.total_points)

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
        initial_resisteance = self.current_resistance
        self.current_resistance += self.used_resistance - less_units
        self.used_resistance = 0

    def experience_gained(self) -> int:
        # print(f"experiencia del jugador {self.name}: {self.current_experience}")
        return self.current_experience - self.initial_experience

    def reset_round_values(self, less_units: int, luck_value: float):
        self.restore_resistence(less_units)
        self.luck = luck_value
        self.total_points = 0

    def reset_values(self, luck: float, resistance: int):
        self.initial_experience = constants.INITIAL_EXPERIENCE
        self.luck = luck
        self.current_resistance = resistance
        self.current_experience = self.initial_experience
        self.total_points = 0
        self.used_resistance = 0

    def add_lucky_game(self):
        self.quantity_luckiest_games += 1

    def add_experienced_game(self):
        self.quantity_experienced_games += 1


class Team:
    def __init__(self, name: str):
        self.name = name
        self.archers: list[Archer] = []
        self.total_points = 0
        self.total_special_shots = 0
        self.puntuations: list[PuntuationTeam] = []
        self.special_archer = None
        self.quantity_games_won = 0
        self.points_by_round = []
        self.special_shots_by_game = []
        self.experience_by_game = []
        self.repeated_special_archer = 0

    def add_archer(self, archer: Archer):
        self.archers.append(archer)

    def add_special_shot_game(self, game: int):
        if (game) > (len(self.special_shots_by_game) - 1):
            self.special_shots_by_game.append(1)
        else:
            self.special_shots_by_game[game] += 1

    def add_experience_game(self):
        self.experience_by_game.append(self.__total_experience_gained())

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
        self.points_by_round.append(self.total_points)

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

    def reset_game_values(self):
        self.total_points = 0
        self.total_special_shots = 0
        self.special_archer = None

    def add_game_won(self):
        self.quantity_games_won += 1


class Round:
    def __init__(self, id: int, game: int):
        self.id = id
        self.game_id = game
        self.isATiedRound = False
        self.best_archer: dict = None
        self.best_team: dict = None
        self.luckiest_archer: dict = None

    def execute(self, teams: list[Team]):
        self.make_shots(teams)
        most_lucky_archers = self.obtain_most_lucky_archers(teams)
        self.execute_special_shots(most_lucky_archers, teams, self.id)
        self.define_winning_team(teams)
        self.define_winning_archer(teams)
        self.save_team_points(teams)
        self.restore_values(teams)

        # print(f"Ronda {self.id}:")
        # if self.best_team:
        #    print(f"Equipo ganador: {self.best_team[constants.NAME_ATRIBUTE]} / puntos: {self.best_team[constants.PUNTUATION_ATRIBUTE]}")
        # else:
        #    print("Ronda empatada")

    def save_team_points(self, teams: list[Team]):
        for team in teams:
            team.add_puntuation(self.game_id, self.id)

    def restore_values(self, teams: list[Team]):
        substractConverter = SubstractResistanceConverter()
        for team in teams:
            for archer in team.archers:
                if archer.experience_gained() >= 9:
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
        archer.add_experience(3)
        # print(archer)
        # print(f"arquero: {archer.name}, experiencia: {archer.current_experience}")
        self.best_archer = {
            constants.NAME_ATRIBUTE: archer.name,
            constants.PUNTUATION_ATRIBUTE: archer.total_points,
            constants.GENDER: archer.gender,
        }

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
            team.add_special_shot_game(self.game_id)
            team.add_points(points)

    def validate_additional_shot(self, team: Team, archer: Archer, round: int):
        if team.special_archer:
            # print(f"{team.special_archer.name}:{archer.name}")
            if team.special_archer.name == archer.name:
                # print("Jugador especial repetido")
                team.repeated_special_archer += 1
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
        else:
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
            for archer in team.archers:
                archer.acumulate_points()
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
                    # print("Equipos empatados")
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
                    best_archers = list()
                    best_archers.extend(best_archers_team)
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
        self.quantity_of_tied_rounds = 0
        self.female_experience_by_round = []
        self.male_experience_by_round = []

    def execute(self, teams: list[Team]):
        self.execute_rounds(teams)

    def execute_rounds(self, teams: list[Team]):
        for i in range(constants.QUANTITY_OF_ROUNDS):
            round = Round(i, self.id)
            self.rounds.append(round)
            round.execute(teams)
        self.experience_by_gender(teams)
        self.define_winner_team(teams)
        self.define_winner_archer()
        self.define_luckiest_archer(teams)
        self.define_most_experienced_archers(teams)
        self.count_victories_by_gender()
        self.reset_values(teams)

        # self.show_results()

    def show_results(self):
        print(f"\nResultados del juego {self.id}: \n")
        if self.bestTeam:
            print(
                f"Equipo ganador: {self.bestTeam[constants.NAME_ATRIBUTE]} / Rondas: {self.bestTeam[constants.ROUNDS_WON]}"
            )
        else:
            print("Juego empatado")

        if self.bestArcher:
            print(
                f"Jugador ganador: {self.bestArcher[constants.NAME_ATRIBUTE]} / Rondas: {self.bestArcher[constants.ROUNDS_WON]}"
            )
        else:
            print("Jugadores empatados")

        if self.the_luckiest_archer:
            print(
                f"Jugador más afortunado: {self.the_luckiest_archer[constants.NAME_ATRIBUTE]} / Suerte: {self.the_luckiest_archer[constants.LUCK]}"
            )

        print("JUGADORES CON MÁS EXPERIENCIA")
        for archer in self.the_most_experienced_archers:
            print(
                f"Jugador: {archer[constants.NAME_ATRIBUTE]} / Experiencia: {archer[constants.EXPERIENCE]}"
            )

        print(f"Victorias femeninas: {self.female_wins}")
        print(f"Victorias masculinas: {self.male_wins}")
        print(f"Cantidad de rondas empatadas: {self.quantity_of_tied_rounds}")

    def define_winner_team(self, teams: list[Team]):
        best_teams = self.count_victories_by_team()
        self.bestTeam = self.define_winner(best_teams, constants.ROUNDS_WON)
        if self.bestTeam:
            self.search_team(
                teams, self.bestTeam[constants.NAME_ATRIBUTE]
            ).add_game_won()
        # if not self.bestTeam:
        #    print(f"Empate de equipos en el juego {self.id}")

    def search_team(self, teams: list[Team], team_name) -> Team:
        for team in teams:
            if team.name == team_name:
                return team

    def count_victories_by_team(self):
        list = []
        for round in self.rounds:
            if round.best_team:
                team_name = round.best_team[constants.NAME_ATRIBUTE]
                team = self.search_item(list, team_name)
                self.add_won_round(team, team_name, list)
            elif round.isATiedRound:
                self.quantity_of_tied_rounds += 1
        return list

    def define_winner_archer(self):
        best_archers = self.count_victories_by_archer()
        self.bestArcher = self.define_winner(best_archers, constants.ROUNDS_WON)
        # if not self.bestArcher:
        #    print(f"Empate de jugadores en el juego {self.id}")

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

    def define_luckiest_archer(self, teams: list[Team]):
        luckiest_archers = self.obtain_luckiest_archers()
        self.the_luckiest_archer = self.define_winner(luckiest_archers, constants.LUCK)
        self.search_archer(
            teams, self.the_luckiest_archer[constants.NAME_ATRIBUTE]
        ).add_lucky_game()
        if not self.the_luckiest_archer:
            print(f"Empate de jugador afortunado en el juego {self.id}")

    def search_archer(search, teams: list[Team], archer_name) -> Archer:
        for team in teams:
            for archer in team.archers:
                if archer.name == archer_name:
                    return archer

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
                # print(f"experiencia del jugador {archer.name}: {experience_gained}")
                most_experienced_archers = self.compare_experience(
                    experience_gained, archer, most_experienced_archers
                )
        self.the_most_experienced_archers = most_experienced_archers
        self.increase_experienced_count(teams)

    def increase_experienced_count(self, teams: list[Team]):
        for archer in self.the_most_experienced_archers:
            self.search_archer(
                teams, archer[constants.NAME_ATRIBUTE]
            ).add_experienced_game()

    def compare_experience(
        self, experience_gained: int, archer: Archer, most_experienced_archers: list
    ):
        experienced_archers = most_experienced_archers
        if len(experienced_archers) > 0:
            if experience_gained > experienced_archers[0][constants.EXPERIENCE]:
                experienced_archers = []
                self.add_object_to_list(
                    experienced_archers,
                    archer,
                    constants.EXPERIENCE,
                    experience_gained,
                )
            elif experience_gained == experienced_archers[0][constants.EXPERIENCE]:
                self.add_object_to_list(
                    experienced_archers,
                    archer,
                    constants.EXPERIENCE,
                    experience_gained,
                )
        else:
            self.add_object_to_list(
                experienced_archers,
                archer,
                constants.EXPERIENCE,
                experience_gained,
            )
        return experienced_archers

    def add_object_to_list(
        self, values: list, object: Archer, criterion_value, value: int
    ):
        values.append(
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

    def reset_values(self, teams: list[Team]):
        for team in teams:
            team.add_experience_game()
            for archer in team.archers:
                archer.reset_values(norm_random_value(), uniform_value())
            team.reset_game_values()

    def experience_by_gender(self, teams: list[Team]):
        female_exp = 0
        male_exp = 0
        for team in teams:
            for archer in team.archers:
                if archer.gender == Gender.MALE:
                    male_exp += archer.experience_gained()
                else:
                    female_exp += archer.experience_gained()
        self.acumulate_value(self.female_experience_by_round, female_exp)
        self.acumulate_value(self.male_experience_by_round, male_exp)

    def acumulate_value(self, values:list, value_to_acumulate:int):
        size = len(values)
        if size>0:
            values.append((values[size-1]+value_to_acumulate))
        else:
            values.append(value_to_acumulate)

    def acumulate_values(self, values:list, values_to_acumulate:list):
        size = len(values)
        for value in values_to_acumulate:
            self.acumulate_value(values, value)
    
    def acumulate_experience_by_gender(self,female_experience_by_round:list, male_experience_by_round:list, teams: list[Team]):
        self.acumulate_values(female_experience_by_round, self.female_experience_by_round)
        self.acumulate_values(male_experience_by_round, self.male_experience_by_round)


class Tournament:
    def __init__(self):
        self.teams: list[Team] = []
        self.luckiest_archer: Archer = None
        self.the_most_experienced_archer: Archer = None
        self.best_team: Team = None
        self.female_wins = 0
        self.male_wins = 0
        self.tied_rounds = 0
        self.games: list[Game] = []
        self.female_experience_by_round = []
        self.male_experience_by_round = []

    def execute(self):
        self.__assign_team_values()
        self.__execute_games()
        self.__define_luckiest_archer()
        self.__define_most_experienced_archer()
        self.__define_best_team()

        self.tied_rounds_frequency = (
            self.tied_rounds
            / (constants.QUANTITY_OF_ROUNDS * constants.QUANTITY_OF_GAMES)
            * 100
        )
        print(
            "\nResultados torneo:\n"
            + f"Jugador más afortunado: {self.luckiest_archer.name} con {self.luckiest_archer.quantity_luckiest_games} rondas como el más afortunado\n"
            + f"Jugador más experimentado: {self.the_most_experienced_archer.name} con {self.the_most_experienced_archer.quantity_experienced_games} rondas como el que más experiencia ganó\n"
            + f"Mejor equipo: {self.best_team.name} con {self.best_team.quantity_games_won} rondas ganadas\n"
            + f"Cantidad de rondas ganadas por el género femenino: {self.female_wins} rondas\n"
            + f"Cantidad de rondas ganadas por el género másculino: {self.male_wins} rondas\n"
            + f"Cantidad de rondas empatadas: {self.tied_rounds} rondas\n"
            + f"Frecuencia relativa de rondas empatadas: {self.tied_rounds_frequency:.2f}%\n"
        )

    def __assign_team_values(self):
        number_archers = 1
        for i in range(constants.QUANTITY_OF_TEAMS):
            team = Team(f"Equipo {(i+1)}")
            for j in range(constants.QUANTITY_OF_ARCHERS_BY_TEAM):
                gender = obtain_gender(random_value())
                points_converter = None
                if gender == Gender.MALE:
                    points_converter = MalePointsConverter()
                else:
                    points_converter = FemalePointsConverter()
                team.add_archer(
                    Archer(
                        f"Arquero {(number_archers)}",
                        team.name,
                        uniform_value(),
                        norm_random_value(),
                        gender,
                        points_converter,
                    )
                )
                number_archers += 1
            self.teams.append(team)

    def __execute_games(self):
        for i in range(constants.QUANTITY_OF_GAMES):
            porcentaje = (i + 1) / constants.QUANTITY_OF_GAMES * 100
            print(
                f"\rProgreso: {porcentaje:.1f}% ({i + 1}/{constants.QUANTITY_OF_GAMES})",
                end="",
                flush=True,
            )
            game = Game(i)
            self.games.append(game)
            game.execute(self.teams)
            game.acumulate_experience_by_gender(
                self.female_experience_by_round, self.male_experience_by_round, self.teams
            )
            self.female_wins += game.female_wins
            self.male_wins += game.male_wins
            self.tied_rounds += game.quantity_of_tied_rounds

    def __define_luckiest_archer(self):
        for team in self.teams:
            for archer in team.archers:
                if self.luckiest_archer:
                    if (
                        archer.quantity_luckiest_games
                        > self.luckiest_archer.quantity_luckiest_games
                    ):
                        self.luckiest_archer = archer
                else:
                    self.luckiest_archer = archer

    def __define_most_experienced_archer(self):
        for team in self.teams:
            for archer in team.archers:
                if self.the_most_experienced_archer:
                    if (
                        archer.quantity_experienced_games
                        > self.luckiest_archer.quantity_experienced_games
                    ):
                        self.the_most_experienced_archer = archer
                else:
                    self.the_most_experienced_archer = archer

    def __define_best_team(self):
        for team in self.teams:
            if self.best_team:
                if team.quantity_games_won > self.best_team.quantity_games_won:
                    self.best_team = team
            else:
                self.best_team = team

    def winning_genre(self):
        if self.male_wins > self.female_wins:
            return Gender.MALE.value
        else:
            return Gender.FEMALE.value

    def points_by_archer(self):
        points_archers = {}
        for team in self.teams:
            for archer in team.archers:
                points_archers.update({archer.name: archer.acumulation_points})
        return points_archers

    def points_by_team(self) -> dict:
        points_team = {}
        for team in self.teams:
            points_team.update({team.name: team.points_by_round})
        return points_team

    def experience_by_gender(self):
        experience = {
            "Masculino": self.male_experience_by_round,
            "Femenino": self.female_experience_by_round,
        }
        return experience
