from dataclasses import dataclass
import json
from typing import List
from models.game import Game

from models.team import Team


@dataclass
class Prediction:
    groupId: str
    games: List[Game]
    result: List[Team]

    @staticmethod
    def from_dict(data: dict):
        if data is None:
            return None

        games = []
        for game in data['games']:
            games.append(Game.from_dict(game))
        result = []
        for team in data['result']:
            result.append(Team.from_dict(team))

        return Prediction(
            groupId=data['groupId'],
            games=games,
            result=data['result']
        )

    @staticmethod
    def from_json(jsonStr: str):
        # parse json
        data = json.loads(jsonStr)
        predictions: List[Prediction] = []
        for p in data:
            predictions.append(Prediction.from_dict(p))

        return predictions
