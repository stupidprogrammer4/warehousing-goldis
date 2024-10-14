from .base_model import BaseModel, Base
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Product(BaseModel):
    __tablename__ = 'products'
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    store_id: Mapped[int] = mapped_column(ForeignKey('stores.id'), nullable=False)
    store: Mapped['Store'] = relationship('Store', back_populates='products')
    recharge_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=True)
    recharge: Mapped['Product'] = relationship('Product', remote_side=[id], back_populates='boosters')
    boosters: Mapped[list['Product']] = relationship('Product', back_populates='recharge', cascade='delete, delete-orphan')


class Store(BaseModel):
    __tablename__ = 'stores'
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    products: Mapped[list['Product']] = relationship('Product', back_populates='store', cascade='delete, delete-orphan')