import os
from typing import List
from dotenv import load_dotenv
from realtime.connection import Socket
from client import SupaClient

from config import Settings


conf = Settings()
SUPA_CLIENT = SupaClient(conf.SUPABASE_URL, conf.SUPABASE_KEY)


def game_callback(payload):
    print("Game callback: ", payload['record'])

    games = SUPA_CLIENT.fetch_games()
    print("Calculating scores...")
    for user in SUPA_CLIENT.fetch_users():
        score = user.calculate_score(games)
        SUPA_CLIENT.update_score(user.id, score)
        if score > 0:
            print(f"{user.name}: {score} points")


def groups_callback(payload):
    print("Groups callback: ", payload['record'])


def main():
    try:
        URL = f"wss://{conf.SUPABASE_ID}.supabase.co/realtime/v1/websocket?apikey={conf.SUPABASE_KEY}&vsn=1.0.0"
        s = Socket(URL)
        s.connect()

        games_channel = s.set_channel("realtime:public:games")
        games_channel.join().on("UPDATE", game_callback)
        # groups_channel = s.set_channel("realtime:public:groups")
        # groups_channel.join().on("UPDATE", groups_callback)
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
