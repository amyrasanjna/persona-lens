"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2026-05-26
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "persons",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("is_unknown", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "images",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("persons.id"), nullable=True),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("caption", sa.Text(), nullable=True),
        sa.Column("alt_text", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "face_embeddings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("persons.id"), nullable=True),
        sa.Column("image_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("images.id"), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("vector_id", sa.String(length=128), nullable=False, unique=True),
    )
    op.create_table(
        "semantic_embeddings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("image_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("images.id"), nullable=False),
        sa.Column("vector_id", sa.String(length=128), nullable=False, unique=True),
    )


def downgrade() -> None:
    op.drop_table("semantic_embeddings")
    op.drop_table("face_embeddings")
    op.drop_table("images")
    op.drop_table("persons")
