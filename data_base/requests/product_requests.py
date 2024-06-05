import os

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from data_base.models import Product


# Создать продукт
async def create_product(async_session: async_sessionmaker[AsyncSession],
                         name: str, category: str, path_to_img: str,
                         description: str, price: int, gender: str) -> str:
    async with async_session() as session:
        product = Product(
            name=name,
            description=description,
            price=price,
            gender=gender,
            path_to_img=path_to_img,
            category_id=category,
        )
        session.add(product)
        await session.commit()
        return f"Создан продукт {name}"


# Просмотр всех продуктов
async def get_products(async_session: async_sessionmaker[AsyncSession],
                       category_name: str, gender=None) -> any:
    async with async_session() as session:
        if category_name.lower() == 'духи' or category_name.lower() == 'масло':
            if gender is None or gender.lower() == 'все':
                stmt = select(Product).where(Product.category_id == category_name)
                result = await session.execute(stmt)
            else:
                stmt = select(Product).where(Product.category_id == category_name).where(Product.gender == gender)
                result = await session.execute(stmt)
        else:
            stmt = select(Product).where(Product.category_id == category_name)
            result = await session.execute(stmt)
        return result.scalars().all()


# Удалить продукт
async def delete_product(async_session: async_sessionmaker[AsyncSession], product_id: int, ) -> str:
    async with async_session() as session:
        stmt = delete(Product).where(Product.id == product_id)
        query = await session.execute(select(Product.path_to_img).where(Product.id == product_id))
        os.remove(query.scalars().one())
        await session.execute(stmt)
        await session.commit()
        return f"Продукт успешно удален"


# Получить всю информацию о продукте
async def get_one_product(async_session: async_sessionmaker[AsyncSession],
                          product_id: int) -> dict:
    async with async_session() as session:
        stmt = await session.get(Product, product_id)
        product = {
            "id": stmt.id,
            "name": stmt.name,
            "description": stmt.description,
            "gender": stmt.gender,
            "price": stmt.price,
            "img": stmt.path_to_img,
            "category_id": stmt.category_id,
        }
        return product


# Получить имя продукта
async def get_name_product(async_session: async_sessionmaker[AsyncSession],
                           product_id: int) -> str:
    async with async_session() as session:
        stmt = await session.get(Product, product_id)
        return stmt.name


# Изменить продукт
async def update_product(async_session: async_sessionmaker[AsyncSession], product_id: int,
                         product_name: str | None = None,
                         product_price: int | None = None,
                         product_gender: str | None = None,
                         product_img: str | None = None,
                         product_description: str | None = None,
                         category: str | None = None) -> str:
    async with async_session() as session:
        if product_name is not None:
            stmt = update(Product).values(name=product_name).where(Product.id == product_id)
            await session.execute(stmt)
            await session.commit()
            return f"Имя успешно изменено !"

        if product_price is not None:
            stmt = update(Product).values(price=product_price).where(Product.id == product_id)
            await session.execute(stmt)
            await session.commit()
            return f"Цена успешно изменена !"

        if product_gender is not None:
            stmt = update(Product).values(gender=product_gender).where(Product.id == product_id)
            await session.execute(stmt)
            await session.commit()
            return f"Гендер  успешно изменен !"

        if product_img is not None:
            query = await session.execute(select(Product.path_to_img).where(Product.id == product_id))
            os.remove(query.scalars().one())
            stmt = update(Product).values(path_to_img=product_img).where(Product.id == product_id)
            await session.execute(stmt)
            await session.commit()
            return f"Фото успешно изменено !"

        if product_description is not None:
            stmt = update(Product).values(description=product_description).where(Product.id == product_id)
            await session.execute(stmt)
            await session.commit()
            return f"Описание успешно изменено !"

        if category is not None:
            stmt = update(Product).values(category_id=category).where(Product.id == product_id)
            await session.execute(stmt)
            await session.commit()
            return f"Категория товара изменена !"


# Просмотр продуктов согласно гендера
async def get_products_gender(async_session: async_sessionmaker[AsyncSession],
                              gender: str) -> any:
    async with async_session() as session:
        stmt = select(Product).where(Product.gender == gender)
        result = await session.execute(stmt)
        return result.scalars().all()
