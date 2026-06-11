# config.py
# All the app settings live here
# If you need to change something like the db url or token expiry, this is the place

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Using SQLite locally to keep things simple during development
    # we'll swap this out for PostgreSQL when we push to production
    DATABASE_URL: str = "sqlite:///./waste_hub.db"

    # Used to sign our JWT tokens — don't leave this as default in production
    SECRET_KEY: str = "your-secret-key-change-in-production"

    # JWT signing algorithm
    ALGORITHM: str = "HS256"

    # Tokens expire after 30 minutes by default
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        # pulls in any variables we set in the .env file
        env_file = ".env"

# one instance shared across the whole app
settings = Settings()