from typing import Sequence

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseModel):
    host: str = 'localhost'
    port: int = 5432
    user: str = 'postgres'
    password: str = 'postgres'
    name: str = 'db'

    @property
    def url_async(self) -> str:
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


class CORSSettings(BaseModel):
    allow_origins: Sequence[str] = ('*',)
    allow_credentials: bool = True
    allow_methods: Sequence[str] = ('*',)
    allow_headers: Sequence[str] = ('*',)


class FApiSettings(BaseModel):
    title: str = "API"
    version: str = "0.0.1"
    description: str = """
### Key Features:
- **User Management**:
    - Create, update, and delete user accounts.
    - Fetch user profiles and manage user data.
- **Authentication**:
    - Secure sign-up and sign-in using hashed passwords and JWT token-based authentication.
    - Retrieve current user data through token verification.

Each endpoint is designed with scalability in mind, ensuring a smooth integration experience for developers."""
    redoc_url: str | None = None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8',
                                      env_nested_delimiter='__')

    cors: CORSSettings = CORSSettings()
    db: DbSettings = DbSettings()
    f_api: FApiSettings = FApiSettings()

settings = Settings()
