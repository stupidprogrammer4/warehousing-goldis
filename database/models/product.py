from .base_model import BaseModel, Base
from sqlalchemy import String, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, registry, configure_mappers

mapper_registry = registry()

boosters = Table(
    'boosters',
    Base.metadata,
    Column('pid_to_boost', Integer, ForeignKey('products.id'), primary_key=True),
    Column('pid_booster', Integer, ForeignKey('products.id'), primary_key=True)
)

class Booster:
    pass

mapper_registry.map_imperatively(Booster, boosters)

class Product(BaseModel):
    __tablename__ = 'products'
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    min_stock: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    store_id: Mapped[int] = mapped_column(ForeignKey('stores.id'), nullable=False)
    store: Mapped['Store'] = relationship('Store', back_populates='products')

    boosters: Mapped[list['Product']] = relationship(
        'Product',
        secondary='boosters',
        primaryjoin='Product.id==boosters.c.pid_to_boost',
        secondaryjoin='Product.id==boosters.c.pid_booster',
        back_populates='boosters',
        overlaps='boosters',
        lazy='select',
        cascade='all'
    )

    to_boost_products: Mapped[list['Product']] = relationship(
        'Product',
        secondary='boosters',
        primaryjoin='Product.id==boosters.c.pid_booster',
        secondaryjoin='Product.id==boosters.c.pid_to_boost',
        back_populates='to_boost_products',
        overlaps='boosters',
        lazy='select',
        cascade='all'
    )

class Store(BaseModel):
    __tablename__ = 'stores'
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    products: Mapped[list['Product']] = relationship('Product', back_populates='store', cascade='delete, delete-orphan')

configure_mappers()