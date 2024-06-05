from typing import Any

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import update, select, delete
from data_base.models import User, Basket


# Добавить корзину
async def add_basket(async_session: async_sessionmaker[AsyncSession],
                     user_id: int, products: dict) -> None:
    async with async_session() as session:
        basket = Basket(
            user_id=user_id,
            products=products,
        )
        session.add(basket)
        await session.commit()


# Показать корзину
async def show_basket(async_session: async_sessionmaker[AsyncSession],
                      user_id: int) -> Any:
    async with async_session() as session:
        stmt = select(Basket).where(Basket.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().all()


# Получить один продукт из корзины
async def get_product_basket(async_session: async_sessionmaker[AsyncSession],
                             basket_id: int) -> dict:
    async with async_session() as session:
        stmt = await session.get(Basket, basket_id)
        return stmt.products


# Удалить продукт из корзины
async def del_basket(async_session: async_sessionmaker[AsyncSession],
                     basket_id: list[int]) -> str:
    async with async_session() as session:
        if len(basket_id) > 1:
            for basket in basket_id:
                stmt = delete(Basket).where(Basket.id == int(basket))
                await session.execute(stmt)
                await session.commit()
            return f"Продукты удалены с корзины"
        else:
            stmt = delete(Basket).where(Basket.id == int(basket_id[0]))
            await session.execute(stmt)
            await session.commit()
            return f"Продукт удалён из корзины"
