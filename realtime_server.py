import os
from dotenv import load_dotenv
from realtime.connection import Socket

from config import Settings


conf = Settings()


def game_callback(payload):
    print("Game callback: ", payload['record'])


def groups_callback(payload):
    print("Groups callback: ", payload['record'])


if __name__ == "__main__":
    URL = f"wss://{conf.SUPABASE_ID}.supabase.co/realtime/v1/websocket?apikey={conf.SUPABASE_KEY}&vsn=1.0.0"
    s = Socket(URL)
    s.connect()

    games_channel = s.set_channel("realtime:public:games")
    games_channel.join().on("UPDATE", game_callback)
    # groups_channel = s.set_channel("realtime:public:groups")
    # groups_channel.join().on("UPDATE", groups_callback)
    s.listen()
