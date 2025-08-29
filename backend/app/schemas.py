from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from .models import UserRole


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.BROKER


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class ClientBase(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None
    source: str
    status: str
    observations: Optional[str] = None
    product: Optional[str] = None
    property_value: Optional[float] = None
    follow_up_state: Optional[str] = "Sem Follow Up"


class ClientCreate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: UUID
    owner_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class InteractionBase(BaseModel):
    type: str
    observation: Optional[str] = None
    from_status: Optional[str] = None
    to_status: Optional[str] = None
    due_date: Optional[datetime] = None


class InteractionCreate(InteractionBase):
    pass


class InteractionRead(InteractionBase):
    id: UUID
    client_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
