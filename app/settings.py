from pydantic_settings import BaseSettings  # ✅ nouveau module

class Settings(BaseSettings):
    ADMIN_PASSWORD: str
    JWT_SECRET: str
    JWT_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()
