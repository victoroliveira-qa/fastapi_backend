from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str

    JWT_SECRET: str
    """
    import secrets

    token: str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = 'HS256'

    # 60 minutos * 24 horas * 1 dia
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    class Config:
        case_sensitive = True


settings: Settings = Settings()