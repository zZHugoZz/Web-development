from sqlalchemy import TIMESTAMP, Column, Integer, String, Float, text
from .database import Base


class Product(Base):
    """this is a basic class that represents a model, this models is
    responsible for creating the different columns in the database. Here we
    just set the name of the table(using __tablename__) and we specify the different
    columns that we want in this table"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Float(precision=2), nullable=False)
    description = Column(String(300), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )
