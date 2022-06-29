from dataclasses import dataclass
from typing import List

from models.prediction import Prediction


@dataclass
class User:
    id: str
    name: str
    description: str
    score: int
    avatar: str
    predictions: List[Prediction]

    @staticmethod
    def from_dict(data: dict):
        predictions = []
        if data['predictions'] is not None:
            predictions = Prediction.from_json(data['predictions'])

        return User(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            score=data['score'],
            avatar=data['avatar'],
            predictions=predictions
        )
