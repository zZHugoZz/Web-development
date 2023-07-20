from pydantic import BaseModel


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    price: float
    description: str | None = None
