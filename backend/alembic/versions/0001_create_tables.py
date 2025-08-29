"""create initial tables

Revision ID: 0001
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    role_enum = postgresql.ENUM("ADMIN", "MANAGER", "BROKER", name="user_role")
    role_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("role", sa.Enum("ADMIN", "MANAGER", "BROKER", name="user_role"), nullable=False, server_default="BROKER"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )

    op.create_table(
        "clients",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("email", sa.String()),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("observations", sa.Text()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("product", sa.String(length=255)),
        sa.Column("property_value", sa.Numeric(15, 2)),
        sa.Column("follow_up_state", sa.String(length=20), server_default="Sem Follow Up", nullable=False),
    )
    op.create_index("idx_clients_owner", "clients", ["owner_id"])
    op.create_index("idx_clients_status", "clients", ["status"])
    op.create_index("idx_clients_followup", "clients", ["follow_up_state"])

    op.create_table(
        "interactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("client_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("clients.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("type", sa.String(length=255), nullable=False),
        sa.Column("observation", sa.Text()),
        sa.Column("from_status", sa.String(length=255)),
        sa.Column("to_status", sa.String(length=255)),
        sa.Column("due_date", sa.DateTime()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("idx_interactions_client", "interactions", ["client_id"])
    op.create_index("idx_interactions_user", "interactions", ["user_id"])
    op.create_index("idx_interactions_type", "interactions", ["type"])
    op.create_index("idx_interactions_created", "interactions", ["created_at"])


def downgrade() -> None:
    op.drop_index("idx_interactions_created", table_name="interactions")
    op.drop_index("idx_interactions_type", table_name="interactions")
    op.drop_index("idx_interactions_user", table_name="interactions")
    op.drop_index("idx_interactions_client", table_name="interactions")
    op.drop_table("interactions")

    op.drop_index("idx_clients_followup", table_name="clients")
    op.drop_index("idx_clients_status", table_name="clients")
    op.drop_index("idx_clients_owner", table_name="clients")
    op.drop_table("clients")

    op.drop_table("users")
    role_enum = postgresql.ENUM("ADMIN", "MANAGER", "BROKER", name="user_role")
    role_enum.drop(op.get_bind(), checkfirst=True)
