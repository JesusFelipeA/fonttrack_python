from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# Convertidor para usar ObjectId con Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Product(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    description: str
    price: float
    stock: int
    category: str

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
