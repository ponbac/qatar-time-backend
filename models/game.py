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
            finished=data['finished']
        )