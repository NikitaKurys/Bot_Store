from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.config_data import Config, load_config

config: Config = load_config()
engine = create_async_engine(url=config.db_config.db_url, echo=True)
session = async_sessionmaker(engine, expire_on_commit=False)
