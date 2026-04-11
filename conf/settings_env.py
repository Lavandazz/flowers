from pydantic_settings import BaseSettings

from conf.settings_proj import PROJECT_ROOT




class Settings(BaseSettings):
    # POSTGRES
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str

    # Django
    DEBUG: bool

    SECRET_KEY: str
    DJANGO_SUPERUSER_USERNAME: str
    DJANGO_SUPERUSER_PASSWORD: str
    DJANGO_SUPERUSER_EMAIL: str

    # Redis
    REDIS_PASSWORD: str


def get_settings():
    return Settings(_env_file=PROJECT_ROOT / ".env", _env_file_encoding='utf-8')


settings = get_settings()
