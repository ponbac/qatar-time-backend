import os
from dotenv import load_dotenv
from realtime.connection import Socket

load_dotenv()

SUPABASE_ID = os.environ.get("SUPABASE_ID")
API_KEY = os.environ.get("SUPABASE_API_KEY")


def callback1(payload):
    print("Callback 1: ", payload)


if __name__ == "__main__":
    URL = f"wss://{SUPABASE_ID}.supabase.co/realtime/v1/websocket?apikey={API_KEY}&vsn=1.0.0"
    s = Socket(URL)
    s.connect()

    channel_1 = s.set_channel("realtime:public:users")
    channel_1.join().on("UPDATE", callback1)
    s.listen()
