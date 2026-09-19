"""add database integrity constraints

Revision ID: d1f242bc5e1f
Revises: 45eb4f91047b
Create Date: 2026-09-19
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "d1f242bc5e1f"
down_revision: Union[str, Sequence[str], None] = "45eb4f91047b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Add database-level integrity constraints.

    SQLite requires table recreation for this type of schema change,
    so Alembic batch mode is used.
    """

    with op.batch_alter_table(
        "projects",
        recreate="always",
    ) as batch_op:
        batch_op.create_check_constraint(
            "ck_projects_approved_budget_nonnegative",
            "approved_budget >= 0",
        )

        batch_op.create_check_constraint(
            "ck_projects_revised_budget_nonnegative",
            "revised_budget IS NULL OR revised_budget >= 0",
        )

        batch_op.create_check_constraint(
            "ck_projects_expenditure_nonnegative",
            "expenditure >= 0",
        )

        batch_op.create_check_constraint(
            "ck_projects_planned_progress_range",
            "planned_progress >= 0 AND planned_progress <= 100",
        )

        batch_op.create_check_constraint(
            "ck_projects_actual_progress_range",
            "actual_progress >= 0 AND actual_progress <= 100",
        )

        batch_op.create_check_constraint(
            "ck_projects_planned_dates_valid",
            "planned_start_date IS NULL "
            "OR planned_end_date IS NULL "
            "OR planned_end_date >= planned_start_date",
        )

        batch_op.create_check_constraint(
            "ck_projects_actual_dates_valid",
            "actual_start_date IS NULL "
            "OR actual_end_date IS NULL "
            "OR actual_end_date >= actual_start_date",
        )

    with op.batch_alter_table(
        "project_snapshots",
        recreate="always",
    ) as batch_op:
        batch_op.create_check_constraint(
            "ck_project_snapshots_approved_budget_nonnegative",
            "approved_budget >= 0",
        )

        batch_op.create_check_constraint(
            "ck_project_snapshots_revised_budget_nonnegative",
            "revised_budget IS NULL OR revised_budget >= 0",
        )

        batch_op.create_check_constraint(
            "ck_project_snapshots_expenditure_nonnegative",
            "expenditure >= 0",
        )

        batch_op.create_check_constraint(
            "ck_project_snapshots_planned_progress_range",
            "planned_progress >= 0 AND planned_progress <= 100",
        )

        batch_op.create_check_constraint(
            "ck_project_snapshots_actual_progress_range",
            "actual_progress >= 0 AND actual_progress <= 100",
        )

        batch_op.create_check_constraint(
            "ck_project_snapshots_planned_dates_valid",
            "planned_start_date IS NULL "
            "OR planned_end_date IS NULL "
            "OR planned_end_date >= planned_start_date",
        )

        batch_op.create_check_constraint(
            "ck_project_snapshots_actual_dates_valid",
            "actual_start_date IS NULL "
            "OR actual_end_date IS NULL "
            "OR actual_end_date >= actual_start_date",
        )


def downgrade() -> None:
    """
    Remove the database-level integrity constraints.
    """

    with op.batch_alter_table(
        "project_snapshots",
        recreate="always",
    ) as batch_op:
        batch_op.drop_constraint(
            "ck_project_snapshots_actual_dates_valid",
            type_="check",
        )

        batch_op.drop_constraint(
            "ck_project_snapshots_planned_dates_valid",
            type_="check",
        )

        batch_op.drop_constraint(
            "ck_project_snapshots_actual_progress_range",
            type_="check",
        )

        batch_op.drop_constraint(
            "ck_project_snapshots_planned_progress_range",
            type_="check",
        )

        batch_op.drop_constraint(
            "ck_project_snapshots_expenditure_nonnegative",
            type_="check",
        )

        batch_op.drop_constraint(
            "ck_project_snapshots_revised_budget_nonnegative",
            type_="check",
        )

        batch_op.drop_constraint(
            "ck_project_snapshots_approved_budget_nonnegative",
            type_="check",
        )

    with op.batch_alter_table(
        "projects",
        recreate="always",
    ) as batch_op:
        batch_op.drop_constraint(
            "ck_projects_actual_dates_valid",
            type_="check",
        )

        batch_op.drop_constraint(
            "ck_projects_planned_dates_valid",
            type_="check",
        )

        batch_op.drop_constraint(
            "ck_projects_actual_progress_range",
            type_="check",
        )

        batch_op.drop_constraint(
            "ck_projects_planned_progress_range",
            type_="check",
        )

        batch_op.drop_constraint(
            "ck_projects_expenditure_nonnegative",
            type_="check",
        )

        batch_op.drop_constraint(
            "ck_projects_revised_budget_nonnegative",
            type_="check",
        )

        batch_op.drop_constraint(
            "ck_projects_approved_budget_nonnegative",
            type_="check",
        )