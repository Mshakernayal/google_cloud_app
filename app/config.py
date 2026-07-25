from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_NAME: str = "posts_db"
    DB_USER: str = "app_user"
    DB_PASS: str = ""
    INSTANCE_CONNECTION_NAME: str = ""

    model_config = {"env_file": ".env"}

    @property
    def     DATABASE_URL(self) -> str:
        if self.INSTANCE_CONNECTION_NAME:
            return (
                f"postgresql://{self.DB_USER}:{self.DB_PASS}"
                f"@/{self.DB_NAME}?host=/cloudsql/{self.INSTANCE_CONNECTION_NAME}"
            )
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}/{self.DB_NAME}"
        )


settings = Settings()
