from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload

from data_base.models import User, Category


# Просмотр категорий
async def get_categories(async_session: async_sessionmaker[AsyncSession]) -> any:
    async with async_session() as session:
        stmt = (
            select(Category)
            .options(selectinload(Category.products))
        )
        result = await session.execute(stmt)
        return result.unique().scalars().all()


# Создание категории
async def create_category(async_session: async_sessionmaker[AsyncSession],
                          name: str) -> str:
    async with async_session() as session:
        check_category = await session.execute(select(Category).filter_by(name=name))

        # Проверка, существует категория или нет
        if check_category.scalars().one_or_none() is None:
            category = Category(name=name)
            session.add(category)
            await session.commit()
            return f"Создана категория {name}"
        else:
            return f"Категория {name} уже создана"


# Удаление категории
async def delete_category(async_session: async_sessionmaker[AsyncSession], name: str) -> str:
    async with async_session() as session:
        stmt = delete(Category).where(Category.name == name)
        await session.execute(stmt)
        await session.commit()
        return f"Категория {name} успешно удалена"


# Обновление категории
async def update_category(async_session: async_sessionmaker[AsyncSession], name: str, new_name: str) -> str:
    async with async_session() as session:
        check_category = await session.execute(select(Category).filter_by(name=new_name))
        if check_category.scalars().one_or_none() is None:
            stmt = update(Category).values(name=new_name).filter_by(name=name)
            await session.execute(stmt)
            await session.commit()
            return f"Категория {name} успешно переименован"
        else:
            return f"Категория {name} уже существует"


