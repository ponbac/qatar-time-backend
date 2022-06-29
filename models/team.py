from dataclasses import dataclass


@dataclass
class Team:
    id: int
    name: str
    flagCode: str
    groupId: str
    points: int

    @staticmethod
    def from_dict(data: dict):
        return Team(
            id=data['id'],
            name=data['name'],
            flagCode=data['flagCode'],
            groupId=data['groupId'],
            points=data['points']
        )
