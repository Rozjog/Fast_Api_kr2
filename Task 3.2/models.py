from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float