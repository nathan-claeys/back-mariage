from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    ADMIN_PASSWORD: str
    ALLOWED_ORIGINS: str  # pour les CORS (front autorisé)

    class Config:
        env_file = ".env"

settings = Settings()
