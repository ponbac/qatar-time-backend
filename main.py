from typing import Union
from client import SupaClient

from fastapi import FastAPI
from config import Settings


app = FastAPI()

conf = Settings()  # type: ignore
SUPA_CLIENT = SupaClient(conf.SUPABASE_URL, conf.SUPABASE_KEY)


def game_callback():
    games = SUPA_CLIENT.fetch_games()
    groups = SUPA_CLIENT.fetch_groups()
    print("Calculating scores...")
    for user in SUPA_CLIENT.fetch_users():
        score = user.calculate_score(games, groups)
        SUPA_CLIENT.update_score(user.id, score)
        if score > 0:
            print(f"{user.name}: {score} points")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/calc-scores")
def calc_scores():
    game_callback()
    return {"status": "ok"}
