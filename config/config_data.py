from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str
    pay_token: str


@dataclass
class DbConfig:
    db_url: str


@dataclass
class Config:
    tg_bot: TgBot
    db_config: DbConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env("BOT_TOKEN"),
            pay_token=env("PAY_TOKEN"),
        ),
        db_config=DbConfig(
            db_url=f"postgresql+asyncpg://{env('DB_USER')}:{env('DB_PASS')}@"
                   f"{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}"
        )
    )
