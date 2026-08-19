from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContactBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=255
    )

    phone_number: str = Field(
        ...,
        min_length=7,
        max_length=20
    )

    email: EmailStr | None = None

    address: str | None = Field(
        default=None,
        max_length=500
    )


class ContactCreate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)