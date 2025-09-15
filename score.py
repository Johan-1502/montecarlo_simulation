class Puntuation:
    def __init__(self, id:int, game:int, round:int, points:int):
        self.id = id
        self.game = game
        self.round = round
        self.points = points 

class PuntuationTeam(Puntuation):
    def __init__(self, id, game, round, points, experience_gained:int, total_special_shots:int):
        super().__init__(id, game, round, points)
        self.experience_gained = experience_gained
        self.total_special_shots = total_special_shots