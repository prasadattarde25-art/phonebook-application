from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


class ContactBase(BaseModel):
    name: str = Field(..., max_length=255)
    phone_number: str = Field(..., min_length=7, max_length=20)
    email: EmailStr | None = None
    address: str | None = None


class ContactCreate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)