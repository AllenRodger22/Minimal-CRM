from app.db import SessionLocal, Base, engine
from app import models
from app.auth import get_password_hash
import uuid


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(models.User).first():
            admin = models.User(
                name="Admin",
                email="admin@example.com",
                password_hash=get_password_hash("admin123"),
                role=models.UserRole.ADMIN,
            )
            broker = models.User(
                name="Broker",
                email="broker@example.com",
                password_hash=get_password_hash("broker123"),
                role=models.UserRole.BROKER,
            )
            db.add_all([admin, broker])
            db.flush()

            clients = [
                models.Client(
                    name=f"Cliente {i+1}",
                    phone="000000000",
                    source="Web",
                    status="Primeiro Atendimento",
                    owner_id=broker.id,
                )
                for i in range(3)
            ]
            db.add_all(clients)
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
