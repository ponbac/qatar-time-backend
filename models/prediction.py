from dataclasses import dataclass
import json
from typing import List
from models.game import Game, GamePrediction

from models.team import Team


@dataclass
class Prediction:
    groupId: str
    games: List[GamePrediction]
    result: List[Team]

    @staticmethod
    def from_dict(data: dict):
        if data is None:
            return None

        games = []
        for game in data['games']:
            games.append(GamePrediction.from_dict(game))
        result = []
        for team in data['result']:
            result.append(Team.from_dict(team))

        return Prediction(
            groupId=data['groupId'],
            games=games,
            result=result
        )

    @staticmethod
    def from_json_to_map(jsonStr: str):
        # parse json
        data = json.loads(jsonStr)
        predictions: dict[str, Prediction] = {}
        for p in data:
            predictions[p['groupId']] = Prediction.from_dict(p)

        return predictions
