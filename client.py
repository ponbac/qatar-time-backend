from typing import List
from supabase import create_client, Client

from config import Settings
from models.game import Game
from models.user import User


class SupaClient:
    def __init__(self, url, key):
        self.url = url
        self.key = key
        self.client = create_client(url, key)

    def fetch_users(self) -> List[User]:
        data = self.client.table("users").select("*").execute()
        assert len(data.data) > 0

        users = []
        for user in data.data:
            users.append(User.from_dict(user))

        return users

    def fetch_games(self) -> List[Game]:
        data = self.client.table("games").select("*").execute()
        assert len(data.data) > 0

        games = []
        for game in data.data:
            games.append(Game.from_dict(game))

        return games

    def update_score(self, user_id: str, score: int):
        self.client.table("users").update(
            {"score": score}).eq("id", user_id).execute()
