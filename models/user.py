from dataclasses import dataclass
from typing import List
from models.game import Game

from models.prediction import Prediction


@dataclass
class User:
    id: str
    name: str
    description: str
    score: int
    avatar: str
    predictions: dict[str, Prediction]

    @staticmethod
    def from_dict(data: dict):
        predictions = None
        if data['predictions'] is not None:
            predictions = Prediction.from_json_to_map(data['predictions'])

        return User(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            score=data['score'],
            avatar=data['avatar'],
            predictions=predictions
        )

    def calculate_score(self, games: List[Game]):
        if self.predictions is None:
            return 0

        score = 0
        finished_games = list(filter(lambda g: g.finished, games))
        for group_prediction in self.predictions.values():
            group_games = filter(lambda g: g.groupId ==
                                 group_prediction.groupId, finished_games)
            for finished_game in group_games:
                prediction = next(
                    filter(lambda p: p.id == finished_game.id, group_prediction.games), None)
                if prediction is not None:
                    if finished_game.winner == prediction.winner:
                        score += 3
                    if finished_game.homeGoals == prediction.homeGoals and finished_game.awayGoals == prediction.awayGoals:
                        score += 1

        return score
