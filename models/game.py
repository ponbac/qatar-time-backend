from dataclasses import dataclass

from models.team import Team


@dataclass
class Game:
    id: int
    groupId: str
    homeTeam: int
    homeGoals: int
    awayTeam: int
    awayGoals: int
    date: str
    finished: bool
    winner: int

    @staticmethod
    def from_dict(data: dict):
        return Game(
            id=data['id'],
            groupId=data['groupId'],
            homeTeam=data['homeTeam'],
            homeGoals=data['homeGoals'],
            awayTeam=data['awayTeam'],
            awayGoals=data['awayGoals'],
            date=data['date'],
            finished=data['finished'],
            winner=data['winner'] if data['winner'] is not None else -1
        )


@dataclass
class GamePrediction:
    id: int
    homeGoals: int
    awayGoals: int
    winner: int

    @staticmethod
    def from_dict(data: dict):
        return GamePrediction(
            id=data['id'],
            homeGoals=data['homeGoals'],
            awayGoals=data['awayGoals'],
            winner=data['winner']
        )
