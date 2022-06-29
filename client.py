import os
from supabase import create_client, Client

from config import Settings

conf = Settings()

supabase: Client = create_client(conf.SUPABASE_URL, conf.SUPABASE_KEY)
