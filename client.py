import os
from supabase import create_client, Client

from config import Settings
from models.user import User

conf = Settings()

supabase: Client = create_client(conf.SUPABASE_URL, conf.SUPABASE_KEY)

data = supabase.table("users").select("*").execute()
# Assert we pulled real data.
assert len(data.data) > 0

for user in data.data:
    userObject = User.from_dict(user)
    print(userObject.name)
