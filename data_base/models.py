from datetime import datetime
from typing import Annotated, Dict, Any
from sqlalchemy import ForeignKey, func, BigInteger, Identity
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]


class Base(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSONB
    }


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    first_name: Mapped[str]


class Basket(Base):
    __tablename__ = "basket"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    products: Mapped[dict[str, Any]] = mapped_column(nullable=True)


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(primary_key=True, unique=True)
    products: Mapped[list["Product"]] = relationship()


class Product(Base):
    __tablename__ = "products"

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str]
    gender: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    path_to_img: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.name", ondelete="CASCADE"))

