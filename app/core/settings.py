from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    USERNAME: str
    PASSWORD: str
    DATABASE: str
    HOST: str
    PORT: str

    class Config:
        env_prefix = 'DB_'
        env_file = '.env'


db_setting = DBSettings()
