from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ALGORITHM: str
    SECRET_KEY: str
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()