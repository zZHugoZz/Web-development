from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: float
    description: str | None = None
