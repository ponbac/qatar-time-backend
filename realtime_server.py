import os
from typing import List
from dotenv import load_dotenv
from realtime.connection import Socket
from client import SupaClient
import sched
import time

from config import Settings


conf = Settings()  # type: ignore
SUPA_CLIENT = SupaClient(conf.SUPABASE_URL, conf.SUPABASE_KEY)


def game_callback(payload, sc=None):
    print("Game callback: ", payload['record'])

    games = SUPA_CLIENT.fetch_games()
    groups = SUPA_CLIENT.fetch_groups()
    print("Calculating scores...")
    for user in SUPA_CLIENT.fetch_users():
        score = user.calculate_score(games, groups)
        SUPA_CLIENT.update_score(user.id, score)
        if score > 0:
            print(f"{user.name}: {score} points")

    if sc:
        sc.enter(300, 1, game_callback, ({'record': "initial_load"}, sc))


def groups_callback(payload):
    print("Groups callback: ", payload['record'])


def main():
    try:
        URL = f"wss://{conf.SUPABASE_ID}.supabase.co/realtime/v1/websocket?apikey={conf.SUPABASE_KEY}&vsn=1.0.0"
        s = Socket(URL)
        s.connect()

        # Calculate on start and add scheduler
        sc = sched.scheduler(time.time, time.sleep)
        # game_callback({'record': "initial_load"})
        sc.enter(5, 1, game_callback, ({'record': "initial_load"}, sc))
        sc.run()

        games_channel = s.set_channel("realtime:public:games")
        games_channel.join().on("UPDATE", game_callback)
        groups_channel = s.set_channel("realtime:public:groups")
        groups_channel.join().on("UPDATE", game_callback)
        s.listen()
    except Exception as e:
        print(e)
        if e == KeyboardInterrupt:
            print("Exiting...")
            os._exit(0)
        else:
            print("Something went wrong, restarting...")
            main()


if __name__ == "__main__":
    main()
