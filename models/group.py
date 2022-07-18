from dataclasses import dataclass
from typing import List
from unittest import result


@dataclass
class Group:
    id: int
    results: List[int]

    @staticmethod
    def from_dict(data: dict):
        return Group(
            id=data['id'],
            results=data['results']
        )
