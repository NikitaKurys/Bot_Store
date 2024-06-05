import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select, update

from data_base.models import User


# Просмотр пользователя
async def get_user(async_session: async_sessionmaker[AsyncSession], user_id: int) -> User | None:
    async with async_session() as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()


# Создание пользователя
async def create_user(async_session: async_sessionmaker[AsyncSession],
                      user_id: int, first_name: str | None,
                      last_name: str | None, username: str | None) -> None:
    from bot import logger

    handler = logging.FileHandler(f'user_logs/subscribers_logs/{datetime.now().strftime("%Y_%m_%d")}_subscribers.log',
                                  encoding="UTF-8")
    handler.setFormatter(logging.Formatter(fmt='[%(asctime)s] %(message)s'))
    logger.addHandler(handler)

    async with async_session() as session:
        check_user = await session.get(User, user_id)
        if check_user is None and user_id == 466999188:
            user = User(id=user_id, first_name=first_name, is_admin=True)
            session.add(user)
            await session.commit()

        elif check_user is None:
            user = User(id=user_id, first_name=first_name)
            session.add(user)
            await session.commit()
            logger.info(f"Пользователь: Имя - {first_name}, "
                        f"Фамилия - {last_name}, "
                        f"Никнейм - {username} - "
                        f"зарегистрирован")


# Получить всех пользователей
async def get_all_users(async_session: async_sessionmaker[AsyncSession]):
    async with async_session() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        return result.scalars().all()


# Получить всех админов
async def get_all_admins(async_session: async_sessionmaker[AsyncSession]):
    async with async_session() as session:
        stmt = select(User).where(User.is_admin == True)
        result = await session.execute(stmt)
        return result.scalars().all()


# Дать пользователю админа
async def set_admin(async_session: async_sessionmaker[AsyncSession],
                    user_id: int):
    async with async_session() as session:
        stmt = update(User).values(is_admin=True).where(User.id == user_id)
        await session.execute(stmt)
        await session.commit()
        return f"Появился новый админ!"
