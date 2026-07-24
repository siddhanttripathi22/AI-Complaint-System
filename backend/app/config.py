
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str
    groq_model: str = "gemma2-9b-it"
    database_url: str = "mysql+pymysql://root:password@localhost:3306/complaints_db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")



settings = Settings()
