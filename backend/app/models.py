import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Text,
    Enum,
    ForeignKey,
    DateTime,
    Numeric,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .db import Base


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    BROKER = "BROKER"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.BROKER)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    clients = relationship("Client", back_populates="owner")


class Client(Base):
    __tablename__ = "clients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String)
    source = Column(String, nullable=False)
    status = Column(String, nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    observations = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    product = Column(String(255))
    property_value = Column(Numeric(15, 2))
    follow_up_state = Column(String(20), nullable=False, default="Sem Follow Up")

    owner = relationship("User", back_populates="clients")
    interactions = relationship(
        "Interaction", back_populates="client", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_clients_owner", "owner_id"),
        Index("idx_clients_status", "status"),
        Index("idx_clients_followup", "follow_up_state"),
    )


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(255), nullable=False)
    observation = Column(Text)
    from_status = Column(String(255))
    to_status = Column(String(255))
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    client = relationship("Client", back_populates="interactions")

    __table_args__ = (
        Index("idx_interactions_client", "client_id"),
        Index("idx_interactions_user", "user_id"),
        Index("idx_interactions_type", "type"),
        Index("idx_interactions_created", "created_at"),
    )
