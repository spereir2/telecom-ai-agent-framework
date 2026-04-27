from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class CustomerType(str, Enum):
    RESIDENTIAL = "residential"
    BUSINESS = "business"


class Customer(BaseModel):
    full_name: str = Field(min_length=1)
    email: EmailStr | None = None
    phone: str | None = None
    customer_type: CustomerType = CustomerType.RESIDENTIAL
