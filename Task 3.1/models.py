from pydantic import BaseModel, validator
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None
    is_subscribed: Optional[bool] = None
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('Некорректный email')
        return v
    
    @validator('age')
    def validate_age(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Возраст должен быть положительным')
        return v
    
