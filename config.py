from pydantic import BaseSettings


class Settings(BaseSettings):
    # Supabase
    SUPABASE_ID: str
    SUPABASE_KEY: str
    SUPABASE_URL: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

# print(Settings().dict())
