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
from random_values import Values

"""
Módulo principal de simulación de torneo de arquería.

Contiene las clases y lógica para modelar arqueros, equipos, rondas, juegos y el torneo completo,
incluyendo la conversión de puntos, manejo de experiencia, suerte, resistencia y estadísticas globales.
"""

class Archer:
    """
    Representa un arquero participante en el torneo.
    
    Attributes:
        name (str): Nombre del arquero.
        team (str): Nombre del equipo al que pertenece.
        initial_experience (int): Experiencia inicial.
        luck (float): Valor de suerte del arquero.
        gender (Gender): Género del arquero.
        points_converter (PointsConverter): Conversor de puntos según género.
        current_resistance (int): Resistencia actual durante el juego.
        current_experience (int): Experiencia actual durante el juego.
        total_points (int): Puntos totales acumulados.
        used_resistance (int): Resistencia utilizada.
        quantity_luckiest_games (int): Veces que fue el más afortunado.
        quantity_experienced_games (int): Veces que fue el más experimentado.
        puntuations (list): Lista de puntuaciones por tiro.
        round_points (list): Puntos por ronda.
        acumulation_points (list): Puntos acumulados por ronda.
    """
    def __init__(
        self,
        name: str,
        team: str,
        initial_resistance: int,
        luck: float,
        gender: Gender,
        points_converter: PointsConverter,
    ):
        """
        Inicializa un arquero
        
        Args:
            name (str): Nombre del arquero.
            team (str): Nombre del equipo al que pertenece.
            initial_experience (int): Experiencia inicial.
            luck (float): Valor de suerte del arquero.
            gender (Gender): Género del arquero.
            points_converter (PointsConverter): Conversor de puntos según género.
        """
        self.name = name
        self.team = team
        self.luck = luck
        self.gender = gender
        self.initial_experience = constants.INITIAL_EXPERIENCE
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
        """
        Suma los puntos a la ornda corresondiente, de no existir crea la ronda
        
        args:
            id (int): identificar de la ronda
            points (int): cantidad de puntos a sumar a la ronda
        """
        if len(self.round_points) > 0:
            for round in self.round_points:
                if round["id"] == id:
                    round["points"] += points
        else:

            self.round_points.append({"id": id, "points": points})

    def execute_normal_shot(self, value: float, game: int, round: int) -> int:
        """
        Ejecuta un tiro normal el cual sí afecta a la resistencia del arquero
        
        Args:
            value (float): valor aleatorio generado para conocer su puntuación
            game (int): identificador del juego en que se realizó el tiro
            round (int): identificador de la ronda en que se realizó el tiro
            
        Returns:
            int: puntuación obtenida a partir de value
        """
        points = self.__add_points(value, game, round)
        self.decrease_resistence(constants.RESISTANCE_CONSUMPTION)
        return points

    def execute_additional_shot(self, value: float, game: int, round: int) -> int:
        """
        Ejecuta un tiro adicional el cual no afecta a la resistencia del arquero
        
        Args:
            value (float): valor aleatorio generado para conocer su puntuación
            game (int): identificador del juego en que se realizó el tiro
            round (int): identificador de la ronda en que se realizó el tiro
            
        Returns:
            int: puntuación obtenida a partir de value
        """
        return self.__add_points(value, game, round)

    def __add_points(self, value: float, game: int, round: int) -> int:
        """
        Agrega los puntos obtenidos al jugador a partir de value
        
        Args:
            value (float): valor aleatorio generado para conocer su puntuación
            game (int): identificador del juego en que se realizó el tiro
            round (int): identificador de la ronda en que se realizó el tiro
            
        Returns:
            int: puntuación obtenida a partir de value
        """
        point = self.points_converter.obtain_point(value)
        self.add_puntuation_round(round, point)
        puntuation = Puntuation(len(self.puntuations), game, round, point)
        self.puntuations.append(puntuation)
        self.total_points += puntuation.points
        return point

    def acumulate_points(self):
        """
        Acumula los puntos obtenidos sumando los de la última ronda con el total de los que tiene en la ronda actual
        """
        if len(self.acumulation_points) > 0:
            last_position = len(self.acumulation_points) - 1
            self.acumulation_points.append(
                self.acumulation_points[last_position] + self.total_points
            )
        else:
            self.acumulation_points.append(self.total_points)

    def execute_special_shot(self, value: float) -> int:
        """
        Ejecuta un tiro especial obtenido al ser el más afortunado de la ronda, el cual no afecta a la resistencia del arquero y tampoco computa para la cantidad total de puntos
        
        Args:
            value (float): valor aleatorio generado para conocer su puntuación
            
        Returns:
            int: puntuación obtenida a partir de value
        """
        point = self.points_converter.obtain_point(value)
        return point

    def decrease_resistence(self, unitsToRemove: int):
        """
        Disminuye la resistencia del arquero
        
        Args:
            unitsToRemove (int): cantidad de resistecia a restar
        """
        self.current_resistance -= unitsToRemove
        self.used_resistance += unitsToRemove

    def can_continue(self) -> bool:
        """
        Define si el arquero puede continuar realizando lanzamientos a partir de comparar la resistencia actual con el valor de constants.RESISTANCE_CONSUMPTION
            
        Returns:
            bool: Si la resistencia actual es mayor retorna True, de lo contrario retorna False
        """
        return self.current_resistance >= constants.RESISTANCE_CONSUMPTION

    def add_experience(self, experience: int):
        """
        Agrega experiencia al arquero
        
        Args:
            experience (int): Cantidad de experiencia a agregar
        """
        self.current_experience += experience

    def restore_resistence(self, less_units: int):
        """
        Restaura la resistencia gastada del arquero menos la cantidad definida
        
        Args:
            less_units (int): cantidad de resistencia menos para restaurar
        """
        self.current_resistance += self.used_resistance - less_units
        self.used_resistance = 0

    def experience_gained(self) -> int:
        """
        Resistencia obtenida hasta el momento del juego
            
        Returns:
            int: diferencia de la resistencia inicial a la resistencia actual
        """
        return self.current_experience - self.initial_experience

    def reset_round_values(self, less_units: int, luck_value: float):
        """
        Resetea los valores del jugador correspondientes a una ronda
        
        Args:
            less_units (int): cantidad de resistencia menos para restaurar
            luck_value (float): nuevo valor de suerte para la próxima ronda
        """
        self.restore_resistence(less_units)
        self.luck = luck_value
        self.total_points = 0

    def reset_values(self, luck: float, resistance: int):
        """
        Resetea los valores del jugador correspondientes a un juego
        
        Args:
            luck (float): nuevo valor de suerte
            resistance (int): nuevo valor de resitencia para el juego
        """
        self.luck = luck
        self.current_resistance = resistance
        self.current_experience = self.initial_experience
        self.total_points = 0
        self.used_resistance = 0

    def add_lucky_game(self):
        """
        Aumenta la cantidad de juegos en los que ha sido el más afortunado
        """
        self.quantity_luckiest_games += 1

    def add_experienced_game(self):
        """
        Aumenta la cantidad de juegos en los que ha sido el que más experiencia ha ganado
        """
        self.quantity_experienced_games += 1


class Team:
    """
    Representa un equipo de arqueros participante en el torneo.
    
    Atributos:
        name (str): Nombre del equipo.
        archers (list[Archer]): Lista de arqueros.
        total_points (int): Puntos totales del equipo.
        total_special_shots (int): Tiros especiales realizados.
        puntuations (list[PuntuationTeam]): Puntuaciones por ronda.
        special_archer (Archer): Actual arquero especial del equipo de la ronda.
        quantity_games_won (int): Juegos ganados.
        points_by_round (list): Puntos por ronda.
        special_shots_by_game (list): Tiros especiales por juego.
        experience_by_game (list): Experiencia obtenida por juego.
        repeated_special_archer (int): Veces que el arquero especial se repite.
    """
    def __init__(self, name: str):
        """
        Inicializa un equipo
        
        Args:
            name (str): Nombre del equipo.
        """
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
        """
        Agrega un arquero al equipo
        
        Args:
            archer (Archer): Arquero a añadir al equipo
        """
        self.archers.append(archer)

    def add_special_shot_game(self, game: int):
        """
        Aumenta el conteo de tiros especiales ganados por juego
        
        Args:
            game (int): identificador del juego en que se realizó el tiro
        """
        if (game) > (len(self.special_shots_by_game) - 1):
            self.special_shots_by_game.append(1)
        else:
            self.special_shots_by_game[game] += 1

    def add_experience_game(self):
        """
        Agrega la experiencia ganada en el juego
        """
        self.experience_by_game.append(self.__total_experience_gained())

    def add_puntuation(
        self,
        game: int,
        round: int,
    ):
        """
        Añade el registro del puntaje de un lanzamiento
        
        Args:
            game (int): identificador del juego en que se realizó el tiro
            round (int): identificador de la ronda en que se realizó el tiro
        """
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
        """
        Aumenta el contador la cantidiad de puntos ganados en la ronda actual
        
        Args:
            points (int): cantidad de puntos sumar al contador
        """
        self.total_points += points

    def __total_experience_gained(self) -> int:
        """
        Experiencia total reunida fuera de la experiencia inicial
            
        Returns:
            int: experiencia reunida en total
        """
        total_experience = 0
        for archer in self.archers:
            total_experience += archer.experience_gained()
        return total_experience

    def add_special_shot(self):
        """
        Aumenta el contador de la cantidad total de lanzamientos especiales realizados del equipo
        """
        self.total_special_shots += 1

    def the_most_lucky_archer(self):
        """
        Define el arquero más afortunado del equipo
        
        Returns:
            Archer: Arquero más afortunado del equipo
        """
        most_lucky_archer = None
        for archer in self.archers:
            if most_lucky_archer:
                if archer.luck > most_lucky_archer.luck:
                    most_lucky_archer = archer
            else:
                most_lucky_archer = archer
        return most_lucky_archer

    def the_most_experienced_archer(self):
        """
        Define el arquero que más experiencia ha ganado del equipo
        
        Returns:
            Archer: Arquero más experimentado del equipo
        """
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
        """
        Define el o los arqueros que más han acumulado puntos del equipo
        
        Returns:
            list[Archer]: Arqueros con más puntos del equipo
        """
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
        """
        Define el arquero que actualmente ha ejecutado un lanzamiento especial
        
        Args:
            archer (Archer): arquero que acaba de ejecutar un lanzamiento especial
        """
        self.special_archer = archer

    def reset_values(self):
        """
        Resetea el contador de puntos ganados hasta el momento
        """
        self.total_points = 0

    def reset_game_values(self):
        """
        Resetea los valores pertinentes a un juego
        """
        self.total_points = 0
        self.total_special_shots = 0
        self.special_archer = None

    def add_game_won(self):
        """
        Aumenta el contador de juegos ganados
        """
        self.quantity_games_won += 1


class Round:
    """
    Representa una ronda dentro de un juego.

    Atributos:
        id (int): Identificador de la ronda.
        game_id (int): Identificador del juego.
        is_a_tied_round (bool): Indica si la ronda fue empatada.
        best_archer (dict): Mejor arquero de la ronda.
        best_team (dict): Mejor equipo de la ronda.
        luckiest_archer (dict): Arquero más afortunado de la ronda.
        values (Values): Generador de valores aleatorios.
    """
    def __init__(self, id: int, game: int, values:Values):
        """
        Inicializa una ronda
        
        Args:
            id (int): Identificador de la ronda
            game (int): Identificador del juego al que pertenece la ronda
            values (Values): Generador de valores aleatorios.
        """
        self.id = id
        self.game_id = game
        self.is_a_tied_round = False
        self.best_archer: dict = None
        self.best_team: dict = None
        self.luckiest_archer: dict = None
        self.values = values

    def execute(self, teams: list[Team]):
        """
        Realiza la ejecución de la ronda
        
        Args:
            teams (list[Team]): lista de equipos que van a jugar la ronda
        """
        self.make_shots(teams)
        most_lucky_archers = self.obtain_most_lucky_archers(teams)
        self.execute_special_shots(most_lucky_archers, teams, self.id)
        self.define_winning_team(teams)
        self.define_winning_archer(teams)
        self.save_team_points(teams)
        self.restore_values(teams)
        #self.show_results()

    def show_results(self):
        """
        Muestra algunos resultados de la ronda
        """
        print(f"Ronda {self.id}:")
        if self.best_team:
           print(f"Equipo ganador: {self.best_team[constants.NAME_ATRIBUTE]} / puntos: {self.best_team[constants.PUNTUATION_ATRIBUTE]}")
        else:
           print("Ronda empatada")

    def save_team_points(self, teams: list[Team]):
        """
        Guarda los puntajes alcanzados hasta el momento de cada equipo
        
        Args:
            teams (list[Team]): lista de equipos a los que se le guardarán los puntos
        """
        for team in teams:
            team.add_puntuation(self.game_id, self.id)

    def restore_values(self, teams: list[Team]):
        """
        Restaura los valores de los equipos y cada uno de sus arqueros
        
        Args:
            teams (list[Team]): lista de equipos a los que se le resetará los valores
        """
        substractConverter = SubstractResistanceConverter()
        for team in teams:
            for archer in team.archers:
                if archer.experience_gained() >= 9:
                    archer.reset_round_values(
                        constants.DEFAULT_EXPERIENCE_TO_SUBSTRACT, self.values.norm_random_value()
                    )
                else:
                    archer.reset_round_values(
                        substractConverter.obtain_point(self.values.random_value()),
                        self.values.norm_random_value(),
                    )
            team.reset_values()

    def verify_tie(self, archers: list[Archer], teams: list[Team]):
        """
        Verifica la existencia de un empate, de lo contrario define un ganador
        
        Args:
            archers (list[Archer]): Lista de jugadores a los que hay que verificar si hay empate
            teams (list[Team]): lista de equipos existentes para guardar registro de los lanzamientos
        """
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
        """
        Ejecuta los lanzamientos adicionales de los arqueros que lo ganaron
        
        Args:
            archers (list[Archer]): Lista de jugadores que realizarán los lanzamientos adicionales
            teams (list[Team]): lista de equipos existentes para guardar registro de los lanzamientos
        """
        for archer in archers:
            points = archer.execute_additional_shot(
                self.values.random_value(), self.game_id, self.id
            )
            team = self.searchTeam(archer.team, teams)
            team.add_points(points)
        self.verify_tie(archers, teams)

    def set_winner_archer(self, archer: Archer):
        """
        Setea el actual arquero ganador, agregándole la experiencia ganada
        
        Args:
            archer (Archer): Arquero a definir como ganador
        """
        archer.add_experience(constants.EXPERIENCE_TO_ADD)
        #self.show_archer_experience(archer)
        self.best_archer = {
            constants.NAME_ATRIBUTE: archer.name,
            constants.PUNTUATION_ATRIBUTE: archer.total_points,
            constants.GENDER: archer.gender,
        }
        
    def show_archer_experience(self, archer:Archer):
        """
        Muestra la experiencia del arquero
        
        Args:
            archer (Archer): Arquero a mostrar la experiencia
        """
        print(archer)
        print(f"arquero: {archer.name}, experiencia: {archer.current_experience}")
        
    def make_shots(self, teams: list[Team]):
        """
        Ejecuta los lanzamientos de cada equipo
        
        Args:
            teams (list[Team]): Lista de equipos que ejecutarán los disparos
        """
        for team in teams:
            self.make_archers_shots(team)

    def make_archers_shots(self, team: Team):
        """
        Ejecuta los lanzamientos de cada uno de los arqueros del equipos
        
        Args:
            team (Team): Equipo que ejecutará los lanzamientos
        """
        for archer in team.archers:
            self.compare_luck(archer)
            while archer.can_continue():
                self.add_points(archer, team)

    def execute_special_shots(
        self, most_lucky_archers: list[Archer], teams: list[Team], round: int
    ):
        """
        Ejecuta los lanzamientos especiales de los arqueros más afortunados, validando si el arquero se gana el disparo adicional
        
        Args:
            most_lucky_archers (list[Archer]): Lista de los arqueros más afortunados de cada equipo
            teams (list[Team]): Lista de equipos para guardad registro de los lanzamientos especiales realizados
            round (int): Identificador de la ronda actual
        """
        for archer in most_lucky_archers:
            points = archer.execute_special_shot(self.values.random_value())
            team = self.searchTeam(archer.team, teams)
            self.validate_additional_shot(team, archer, round)
            team.add_special_shot()
            team.add_special_shot_game(self.game_id)
            team.add_points(points)

    def validate_additional_shot(self, team: Team, archer: Archer, round: int):
        """
        Verifica si el arquero que acabó de ganar lanzamiento especial ya lo habia ganado en la ronda anterior, en caso de se así realiza el disparo adicional
        
        Args:
            team (Team): Equipo al cual pertenece el jugador que realizó el lanzamiento especial
            archer (Archer): Arquero al cual se le verificará si puede realizar el lanzamiento adicional
            round (int): Identificador de la ronda actual
        """
        if team.special_archer:
            if team.special_archer.name == archer.name:
                team.repeated_special_archer += 1
                additional_point = archer.execute_additional_shot(
                    self.values.random_value(), self.id, round
                )
                team.add_points(additional_point)
            else:
                team.set_special_archer(archer)
        else:
            team.set_special_archer(archer)

    def searchTeam(self, name: str, teams: list[Team]) -> Team:
        """
        Busca un equipo a partir del nombre en una lista de equipos
        
        Args:
            name (str): Nombre del equipo a buscar
            teams (list[Team]): Lista de equipos donde se buscará el equipo definido
            
        Returns:
            Team: Equipo encontrado en la lista de equipos, de no encontrarlo retorna None
        """
        for team in teams:
            if team.name == name:
                return team
        return None

    def obtain_most_lucky_archers(self, teams: list[Team]) -> list[Archer]:
        """
        Devuelve la lista de los arqueros más afortunados por equipo
        
        Args:
            teams (list[Team]): Lista de equipos en los que se buscarán los arqueros más afortunados
            
        Returns:
            list[Archer]: Lista de los arqueros más afortunados
        """
        most_lucky_archers = []
        for team in teams:
            most_lucky_archers.append(team.the_most_lucky_archer())
        return most_lucky_archers

    def compare_luck(self, archer: Archer):
        """
        Compara un arquero con el actual arquero más afortunado para definir si lo cambia por el que comparó en caso de que la suerte sea mayor
        
        Args:
            archer (Archer): Arquero a compara su suerte con el actual más afortunado
        """
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
        """
        Ejecuta un disparo y aumenta la cnatidad de puntos en el equipo
        
        Args:
            archer (Archer): Arquero a ejecutar el lazamiento
            team (Team): Equipo al que se le aumentará la cantidad de puntos
        """
        points_archer = archer.execute_normal_shot(
            self.values.random_value(), self.game_id, self.id
        )
        team.add_points(points_archer)

    def define_winning_team(self, teams: list[Team]):
        """
        Define el equipo ganador comparando la cantidad de puntos que logró
        
        Args:
            teams (Team): Lista de equipos en los que se comparará la cantidad total de puntos
        """
        for team in teams:
            for archer in team.archers:
                archer.acumulate_points()
            if self.best_team:
                if team.total_points > self.best_team[constants.PUNTUATION_ATRIBUTE]:
                    self.is_a_tied_round = False
                    self.best_team = {
                        constants.NAME_ATRIBUTE: team.name,
                        constants.PUNTUATION_ATRIBUTE: team.total_points,
                    }
                elif team.total_points == self.best_team[constants.PUNTUATION_ATRIBUTE]:
                    self.best_team = None
                    self.is_a_tied_round = True
                    # print("Equipos empatados")
            else:
                self.best_team = {
                    constants.NAME_ATRIBUTE: team.name,
                    constants.PUNTUATION_ATRIBUTE: team.total_points,
                }

    def define_winning_archer(self, teams: list[Team]):
        """
        Define el arquero ganador comparando la cantidad de puntos ganados con los demás arqueros
        
        Args:
            teams (list[Team]): lista de equipos para comparar el puntaje de cada uno de sus arqueros
        """
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
        """
        Devuelve el arquero más afortunado de la ronda
        
        Returns:
            Archer: Arquero más afortunado de la ronda
        """
        return self.luckiest_archer


class Game:
    """
    Representa un juego completo compuesto por varias rondas.

    Atributos:
        id (int): Identificador del juego.
        rounds (list[Round]): Lista de rondas del juego.
        the_luckiest_archer (dict): Arquero más afortunado del juego.
        the_most_experienced_archers (list): Arqueros más experimentados del juego.
        bestTeam (dict): Mejor equipo del juego.
        bestArcher (dict): Mejor arquero del juego.
        male_wins (int): Rondas ganadas por hombres.
        female_wins (int): Rondas ganadas por mujeres.
        quantity_of_tied_rounds (int): Cantidad de rondas empatadas.
        female_experience_by_round (list): Experiencia femenina por ronda.
        male_experience_by_round (list): Experiencia masculina por ronda.
        values (Values): Generador de valores aleatorios.
    """
    def __init__(self, id: int, values:Values):
        """
        Inicializa un juego
        
        Args:
            id (int): Identificador del juego
            values (Values): Generador de valores aleatorios.
        """
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
        self.values = values

    def execute(self, teams: list[Team]):
        """
        Realiza la ejecución del juego y define las características del mismo
        
        Args:
            teams (list[Team]): Lista de equipos que partciparán del juego.
        """
        self.execute_rounds(teams)
        self.experience_by_gender(teams)
        self.define_winner_team(teams)
        self.define_winner_archer()
        self.define_luckiest_archer(teams)
        self.define_most_experienced_archers(teams)
        self.count_victories_by_gender()
        self.reset_values(teams)

    def execute_rounds(self, teams: list[Team]):
        """
        Ejecuta todas las rondas del juego
        
        Args:
            teams (list[Team]): Lista de los equipos que jugarán las rondas
        """
        for i in range(constants.QUANTITY_OF_ROUNDS):
            round = Round(i, self.id, self.values)
            self.rounds.append(round)
            round.execute(teams)

        # self.show_results()

    def show_results(self):
        """
        Muestra algunos resultados del juego
        """
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
        """
        Determina el equipo ganador comparando la cantidad de rondas ganadas
        
        Args:
            teams (list[Team]): Lista de los equipos que hacen parte del juego
        """
        best_teams = self.count_victories_by_team()
        self.bestTeam = self.define_winner(best_teams, constants.ROUNDS_WON)
        if self.bestTeam:
            self.search_team(
                teams, self.bestTeam[constants.NAME_ATRIBUTE]
            ).add_game_won()
        # if not self.bestTeam:
        #    print(f"Empate de equipos en el juego {self.id}")

    def search_team(self, teams: list[Team], team_name:str) -> Team:
        """
        Busca un equipo en una lista a partir l nombre del mismo.
        
        Args:
            teams (list[Team]): Lista de los equipos en la que se buscará el equipo
            team_name (str): nombre del equipo a buscar en la lista de equipos
            
        Returns:
            Team: Equipo encontrado en la lista de equipos
        """
        for team in teams:
            if team.name == team_name:
                return team

    def count_victories_by_team(self):
        """
        Cuenta la cantidad de rondas ganadas de cada equipo
        
        Returns:
            list : Lista de los equipos junto con la cantidad de rondas ganadas
        """
        list = []
        for round in self.rounds:
            if round.best_team:
                team_name = round.best_team[constants.NAME_ATRIBUTE]
                team = self.search_item(list, team_name)
                self.add_won_round(team, team_name, list)
            elif round.is_a_tied_round:
                self.quantity_of_tied_rounds += 1
        return list

    def define_winner_archer(self):
        """
        Define el equipo ganador del juego, comparando la cantidad de rondas ganadas
        """
        best_archers = self.count_victories_by_archer()
        self.bestArcher = self.define_winner(best_archers, constants.ROUNDS_WON)
        # if not self.bestArcher:
        #    print(f"Empate de jugadores en el juego {self.id}")

    def count_victories_by_archer(self):
        """
        Cuenta la cantidad de rondas ganadas por arquero
        
        Returns:
            list : Lista de los arqueros junto con el conteo de rondas ganadas
        """
        list = []
        for round in self.rounds:
            if round.best_archer:
                archer_name = round.best_archer[constants.NAME_ATRIBUTE]
                archer = self.search_item(list, archer_name)
                self.add_won_round(archer, archer_name, list)
        return list

    def add_won_round(self, object, object_name, list: list):
        """
        Aumenta el contador de rondas ganadas al objeto que se le pasa por parámetro, en caso de no existir lo agrega a la lista con un contador inicial de 1.
        
        Args:
            object: Objeto al que se le aumentará el contador de rondas ganadas.
            object_name: Nombre del objeto para crearlo en dado caso de que no exista.
            list (list): Lista en donde se agrega el objeto en dado caso de no existir.
        """
        if object:
            object[constants.ROUNDS_WON] += 1
        else:
            list.append({constants.NAME_ATRIBUTE: object_name, constants.ROUNDS_WON: 1})

    def define_winner(self, best_participants, criterion):
        """
        Define el arquero ganador del juego por medio del criterio pasado por parámetro
        
        Args:
            best_participants : Lista de los jugadores con su respectiva cantidad de rondas ganadas
            criterion : Criterio a utilizar para comparar y definir quién es el ganador
            
        Return: 
            dict: diccionario del mejor arquero el cual contiene el nombre y cantidad de rondas ganadas
            En caso de no haber ganador porque hubo empate retorna None
        """
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
        """
        Busca un objeto en la lista a partir del nombre del mismo
        
        Args:
            list: Lista en la que se buscará el objeto
            name: Nombre del objeto a buscar

        Returns:
            Retorna el objeto que tenga el nombre ingresado, de no encontrarse retorna None
        """
        for object in list:
            if object[constants.NAME_ATRIBUTE] == name:
                return object
        return None

    def define_luckiest_archer(self, teams: list[Team]):
        """
        Determina cual es el arquero más afortunado del juego
        
        Args:
            teams (list[Team]): Lista de los equipos en que se buscará el arquero más afortunado
        """
        luckiest_archers = self.obtain_luckiest_archers()
        self.the_luckiest_archer = self.define_winner(luckiest_archers, constants.LUCK)
        self.search_archer(
            teams, self.the_luckiest_archer[constants.NAME_ATRIBUTE]
        ).add_lucky_game()
        if not self.the_luckiest_archer:
            print(f"Empate de jugador afortunado en el juego {self.id}")

    def search_archer(search, teams: list[Team], archer_name) -> Archer:
        """
        Busca un arquero en la lista de equipos
        
        Args:
            teams (list[Team]): Lista de los equipos en la que se buscará el arquero
            archer_name : Nombre del arquero a buscar
            
        Returns:
            Archer: Arquero que coincida con el nombre del parámetro archer_name
        """
        for team in teams:
            for archer in team.archers:
                if archer.name == archer_name:
                    return archer

    def obtain_luckiest_archers(self):
        """
        Devuleve los arquero más afortunados de cada ronda
        
        Returns:
            list: Lista de arqueros más afortunados por ronda
        """
        luckiest_archers = []
        for round in self.rounds:
            luckiest_archers.append(round.luckiest_archer)
        return luckiest_archers

    def define_most_experienced_archers(self, teams: list[Team]):
        """
        Declara el o los arqueros más experimentados del juego
        
        Args:
            teams (list[Team]): Lista de los equipos participantes
        """
        most_experienced_archers = []
        for team in teams:
            for archer in team.archers:
                experience_gained = archer.experience_gained()
                
                most_experienced_archers = self.compare_experience(
                    experience_gained, archer, most_experienced_archers
                )
        self.the_most_experienced_archers = most_experienced_archers
        self.increase_experienced_count(teams)

    def increase_experienced_count(self, teams: list[Team]):
        """
        Aumenta la cantidad de juegos como el más experimentado de cada jugador
        
        Args:
            teams (list[Team]): Lista de los equipos participantes
        """
        for archer in self.the_most_experienced_archers:
            self.search_archer(
                teams, archer[constants.NAME_ATRIBUTE]
            ).add_experienced_game()

    def compare_experience(
        self, experience_gained: int, archer: Archer, most_experienced_archers: list
    ):
        """
        Compara la experiencia de cada uno de los jugadores para definir cual o cuales son los mas experimentados
        
        Args:
            experience_gained (int): Experiencia ganada por el arquero a comparar
            archer (Archer): Arquero a comparar
            most_experienced_archers (list): Lista de arqueros con más experiencia para comparar
            
        Returns:
            list: Lista de arqueros con más experiencia
        """
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
        """
        Añade un diccionario con el nombre y un valor específico de un arquero a la lista
        
        Args:
            values (list): Lista en la que se agregará el objeto
            object (Archer): Objeto del que se obtendrá la información para crear el diccionario a agregar en la lista
            criterion_value: Criterio o clave que se usará para crear el diccionario a agregar
            value (int): Valor de la clave del diccionario que se agregará
        """
        values.append(
            {
                constants.NAME_ATRIBUTE: object.name,
                criterion_value: value,
            }
        )

    def count_victories_by_gender(self):
        """
        Cuenta la cantidad de victorias por género
        """
        for round in self.rounds:
            winner = round.best_archer
            if winner:
                if winner[constants.GENDER] == Gender.MALE:
                    self.male_wins += 1
                else:
                    self.female_wins += 1

    def reset_values(self, teams: list[Team]):
        """
        Resetea los valores de cada equipo y arqueros referentes al juego
        
        Args:
            teams (list[Team]): Lista de los equipos a los que se reiniciará los valores
        """
        for team in teams:
            team.add_experience_game()
            for archer in team.archers:
                archer.reset_values(self.values.norm_random_value(), self.values.uniform_value())
            team.reset_game_values()

    def experience_by_gender(self, teams: list[Team]):
        """
        Suma la cantidad de experiencia obtenida por cada género, además de acumular la experiencia de las demás rondas
        
        Args:
            teams (list[Team]): Lista de los equipos participantes
        """
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
        """
        Agrega el valor acumulado sumando el nuevo valor con el último valor de la lista
        
        Args:
            values (list): lista de valores a la que se agregará el nuevo valor acumulado
            value_to_acumulate (int): valor a acumular
        """
        size = len(values)
        if size>0:
            values.append((values[size-1]+value_to_acumulate))
        else:
            values.append(value_to_acumulate)

    def acumulate_values(self, values:list, values_to_acumulate:list):
        """
        Agrega cierta cantidad de valores a la lista acumulandolo con la última posición de la lista
        
        Args:
            values (list): lista de valores a la que se agregará el nuevo valor acumulado
            value_to_acumulate (int): valor a acumular
        """
        size = len(values)
        for value in values_to_acumulate:
            self.acumulate_value(values, value)
    
    def acumulate_experience_by_gender(self,female_experience_by_round:list, male_experience_by_round:list, teams: list[Team]):
        """
        Acumula la experiencia ganada en todas las rondas por cada género
        
        Args:
            female_experience_by_round (list): Lista de experiencia femenina por ronda
            male_experience_by_round (list): Lista de experiencia másculina por ronda
            teams (list[Team]): Lista de los equipos participantes
        """
        self.acumulate_values(female_experience_by_round, self.female_experience_by_round)
        self.acumulate_values(male_experience_by_round, self.male_experience_by_round)


class Tournament:
    """
    Representa el torneo completo de arquería.

    Atributos:
        teams (list[Team]): Lista de equipos participantes.
        luckiest_archer (Archer): Arquero más afortunado del torneo.
        the_most_experienced_archer (Archer): Arquero más experimentado del torneo.
        best_team (Team): Mejor equipo del torneo.
        female_wins (int): Rondas ganadas por mujeres.
        male_wins (int): Rondas ganadas por hombres.
        tied_rounds (int): Rondas empatadas.
        games (list[Game]): Lista de juegos del torneo.
        female_experience_by_round (list): Experiencia femenina acumulada por ronda.
        male_experience_by_round (list): Experiencia masculina acumulada por ronda.
        values (Values): Generador de valores aleatorios.
    """
    def __init__(self):
        """
        Inicializa un torneo
        """
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
        self.values = Values()

    def execute(self):
        """
        Ejecuta el torneo y define los resultados finales del mismo
        """
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
        """
        Asigna los valores iniciales a cada equipo utilizando los valores aleatorios generados y testeados previamente 
        """
        number_archers = 1
        for i in range(constants.QUANTITY_OF_TEAMS):
            team = Team(f"Equipo {(i+1)}")
            for j in range(constants.QUANTITY_OF_ARCHERS_BY_TEAM):
                gender = obtain_gender(self.values.random_value())
                points_converter = None
                if gender == Gender.MALE:
                    points_converter = MalePointsConverter()
                else:
                    points_converter = FemalePointsConverter()
                team.add_archer(
                    Archer(
                        f"Arquero {(number_archers)}",
                        team.name,
                        self.values.uniform_value(),
                        self.values.norm_random_value(),
                        gender,
                        points_converter,
                    )
                )
                number_archers += 1
            self.teams.append(team)

    def __execute_games(self):
        """
        Ejecuta todos los juegos del torneo, donde la cantidad se define a partir de la constante QUANTITY_OF_GAMES, además de que imprime el progreso del tiempo que lleva en ejecución
        """
        for i in range(constants.QUANTITY_OF_GAMES):
            porcentaje = (i + 1) / constants.QUANTITY_OF_GAMES * 100
            print(
                f"\rProgreso: {porcentaje:.1f}% ({i + 1}/{constants.QUANTITY_OF_GAMES})",
                end="",
                flush=True,
            )
            game = Game(i, self.values)
            self.games.append(game)
            game.execute(self.teams)
            game.acumulate_experience_by_gender(
                self.female_experience_by_round, self.male_experience_by_round, self.teams
            )
            self.female_wins += game.female_wins
            self.male_wins += game.male_wins
            self.tied_rounds += game.quantity_of_tied_rounds

    def __define_luckiest_archer(self):
        """
        Determina el arquero más afortunado a partir de la cantidad de juegos en los que fue el más afortunado
        """
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
        """
        Determina el arquero más experimentado a partir de la cantidad de juegos en los que fue el más experimentado
        """
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
        """
        Determina el mejor equipo del torneo a partir de la cantidad de juegos que ganó
        
        Returns:
            dict: Mejor equipo del torneo
        """
        for team in self.teams:
            if self.best_team:
                if team.quantity_games_won > self.best_team.quantity_games_won:
                    self.best_team = team
            else:
                self.best_team = team

    def winning_genre(self):
        """
        Determina el género ganador del torneo por medio de la cantidad de juegos que haya ganado
        
        Returns:
            str: Mejor género del torneo        
        """
        if self.male_wins > self.female_wins:
            return Gender.MALE.value
        else:
            return Gender.FEMALE.value

    def points_by_archer(self):
        """
        Devuelve el acumulado de puntos por ronda de cada arquero
        
        Returns:
            dict: diccionario de los puntos de cada arquero en cada ronda
        """
        points_archers = {}
        for team in self.teams:
            for archer in team.archers:
                points_archers.update({archer.name: archer.acumulation_points})
        return points_archers

    def points_by_team(self) -> dict:
        """
        Devuelve el acumulado de puntos por ronda de cada equipo
        
        Returns:
            dict: diccionario de los puntos de cada equipo en cada ronda      
        """
        points_team = {}
        for team in self.teams:
            points_team.update({team.name: team.points_by_round})
        return points_team

    def experience_by_gender(self):
        """
        Devuelve la experiencia de cada ronda obtenida por cada género
        
        Returns:
            dict: Experiencia por ronda de cada género
        """
        experience = {
            "Masculino": self.male_experience_by_round,
            "Femenino": self.female_experience_by_round,
        }
        return experience

    def archers_by_gender(self):
        """
        Devuelve el conteo de arqueros por género
        
        Returns:
            dict: Cantidad de arquero que hay de cada género
        """
        quantities:list[dict] = [
            {
                "gender": Gender.MALE,
                "quantity": 0
            },
            {
                "gender": Gender.FEMALE,
                "quantity": 0
            }
        ]
        for team in self.teams:
            for archer in team.archers:
                if archer.gender == Gender.MALE:
                    quantities[0]["quantity"]+=1
                else:
                    quantities[1]["quantity"]+=1                    
        return quantities