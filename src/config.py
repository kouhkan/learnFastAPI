import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    DEBUG: bool = bool(os.environ.get("DEBUG", True))
    SECRET_KEY: str = os.getenv("SECRET_KEY", default="<KEY>")
    ACCESS_TOKEN_EXPIRE_TIME: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_TIME"))
    REFRESH_TOKEN_EXPIRE_TIME: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_TIME"))
    ALGORITHM: str = os.getenv("ALGORITHM")


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True


class ProductionConfig(BaseConfig):
    DEBUG: bool = False


class TestingConfig(BaseConfig):
    DEBUG: bool = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "test": TestingConfig,
}
