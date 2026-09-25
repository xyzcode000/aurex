"""add snapshot type

Revision ID: bd67b4ea9d62
Revises: d1f242bc5e1f
Create Date: 2026-09-24 05:39:26.557342

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = "bd67b4ea9d62"
down_revision: Union[str, Sequence[str], None] = "d1f242bc5e1f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add snapshot type safely to existing project snapshots."""

    connection = op.get_bind()
    inspector = inspect(connection)

    existing_columns = {
        column["name"]
        for column in inspector.get_columns("project_snapshots")
    }

    # The previous migration attempt may already have added this
    # column before failing during SQLite table recreation.
    if "snapshot_type" not in existing_columns:
        op.add_column(
            "project_snapshots",
            sa.Column(
                "snapshot_type",
                sa.String(length=20),
                nullable=True,
            ),
        )

    # Existing snapshots have unknown provenance.
    # They must therefore be treated as observations, not baselines.
    op.execute(
        """
        UPDATE project_snapshots
        SET snapshot_type = 'observation'
        WHERE snapshot_type IS NULL
        """
    )

    # SQLite requires table recreation to enforce the final NOT NULL
    # constraint and add the CHECK constraint safely.
    with op.batch_alter_table(
        "project_snapshots",
        schema=None,
        recreate="always",
    ) as batch_op:

        batch_op.alter_column(
            "snapshot_type",
            existing_type=sa.String(length=20),
            nullable=False,
        )

        batch_op.create_check_constraint(
            "ck_project_snapshots_snapshot_type",
            "snapshot_type IN ('baseline', 'observation')",
        )


def downgrade() -> None:
    """Remove snapshot type."""

    with op.batch_alter_table(
        "project_snapshots",
        schema=None,
        recreate="always",
    ) as batch_op:

        batch_op.drop_constraint(
            "ck_project_snapshots_snapshot_type",
            type_="check",
        )

        batch_op.drop_column("snapshot_type")