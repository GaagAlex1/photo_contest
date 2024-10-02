from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from sqlalchemy import URL


class AuthSettings(BaseSettings):
    private_key_path: Path = Path(__file__).parent / 'certs' / 'jwt-private.pem'
    public_key_path: Path = Path(__file__).parent / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 3


class DbSettings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    @property
    def DATABASE_URL_asyncpg(self):
        return URL.create('postgresql+asyncpg',
                          username=self.db_user,
                          password=self.db_pass,
                          host=self.db_host,
                          port=self.db_port,
                          database=self.db_name)

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False)


class Settings(BaseModel):
    db: DbSettings = DbSettings()
    auth_jwt: AuthSettings = AuthSettings()


settings: Settings = Settings()
