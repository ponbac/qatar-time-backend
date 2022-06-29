from dataclasses import dataclass
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
