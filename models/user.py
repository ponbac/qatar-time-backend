from dataclasses import dataclass
from typing import List

from numpy import equal
from models.game import Game
from models.group import Group

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

    def calculate_score(self, games: List[Game], groups: List[Group]):
        if self.predictions is None:
            return 0

        GROUPS_CORRECT_WINNER = 3
        GROUPS_CORRECT_SCORE = 1
        QUARTERS_CORRECT_WINNER = 6
        QUARTERS_CORRECT_SCORE = 3
        SEMIS_CORRECT_WINNER = 8
        SEMIS_CORRECT_SCORE = 3
        FINAL_CORRECT_WINNER = 10
        FINAL_CORRECT_SCORE = 3

        score = 0
        # Games score
        finished_games = list(filter(lambda g: g.finished, games))
        for group_prediction in self.predictions.values():
            group_games = filter(lambda g: g.groupId ==
                                 group_prediction.groupId, finished_games)
            for finished_game in group_games:
                prediction = next(
                    filter(lambda p: p.id == finished_game.id, group_prediction.games), None)
                if prediction is not None:
                    if finished_game.winner == prediction.winner:
                        if (group_prediction.groupId == 'QUARTERS'):
                            score += QUARTERS_CORRECT_WINNER
                        elif (group_prediction.groupId == 'SEMIS'):
                            score += SEMIS_CORRECT_WINNER
                        elif (group_prediction.groupId == 'FINAL'):
                            score += FINAL_CORRECT_WINNER
                        else:
                            score += GROUPS_CORRECT_WINNER
                    else:
                        continue
                    if finished_game.homeGoals == prediction.homeGoals and finished_game.awayGoals == prediction.awayGoals:
                        if (group_prediction.groupId == 'QUARTERS'):
                            score += QUARTERS_CORRECT_SCORE
                        elif (group_prediction.groupId == 'SEMIS'):
                            score += SEMIS_CORRECT_SCORE
                        elif (group_prediction.groupId == 'FINAL'):
                            score += FINAL_CORRECT_SCORE
                        else:
                            score += GROUPS_CORRECT_SCORE

        # Groups score
        score += self._calculate_groups_score(groups)

        return score

    def _calculate_groups_score(self, groups: List[Group]):
        if self.predictions is None:
            return 0

        CORRECT_PLACING_SCORE = 3

        score = 0
        for group_prediction in self.predictions.values():
            if group_prediction.groupId == 'QUARTERS' or group_prediction.groupId == 'SEMIS' or group_prediction.groupId == 'FINAL':
                continue
            group_result = next(
                filter(lambda g: g.id == group_prediction.groupId, groups), None)
            if group_result is None or group_result.results is None or len(group_result.results) != 4:
                continue

            if int(group_result.results[0]) == int(group_prediction.results[0].id):
                score += CORRECT_PLACING_SCORE
            if int(group_result.results[1]) == int(group_prediction.results[1].id):
                score += CORRECT_PLACING_SCORE
            if int(group_result.results[2]) == int(group_prediction.results[2].id):
                score += CORRECT_PLACING_SCORE
            if int(group_result.results[3]) == int(group_prediction.results[3].id):
                score += CORRECT_PLACING_SCORE

        # print(f"Group score for {self.name}: {score}")
        return score
