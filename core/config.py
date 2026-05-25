from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://dev_esuda:p87kq25@localhost:5432/esuda'

    JWT_SECRET: str = 'DOHVnT5S2e-KMO2xZy7xbozIIFfSOdzlxWxx3mjkpOg'
    """
    import secrets

    token: str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = 'HS256'

    # 60 minutos * 24 horas * 1 dia
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1

    class Config:
        case_sensitive = True


settings: Settings = Settings()