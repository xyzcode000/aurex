from datetime import date
from decimal import Decimal

from app.ml.dataset_builder import build_project_training_rows
from app.models.project_snapshot import ProjectSnapshot


def snapshot(
    snapshot_id,
    observation_date,
    expenditure,
    planned_progress,
    actual_progress,
    actual_end_date=None,
):
    return ProjectSnapshot(
        id=snapshot_id,
        project_id=1,
        observation_date=observation_date,
        implementing_agency="Demo Agency",
        location="Chhattisgarh",
        status="in_progress",
        approved_budget=Decimal("100000000"),
        revised_budget=Decimal("110000000"),
        expenditure=Decimal(str(expenditure)),
        planned_start_date=date(2026, 1, 1),
        planned_end_date=date(2027, 1, 1),
        actual_start_date=date(2026, 1, 15),
        actual_end_date=actual_end_date,
        planned_progress=Decimal(str(planned_progress)),
        actual_progress=Decimal(str(actual_progress)),
    )


snapshots = [
    snapshot(
        1,
        date(2026, 3, 31),
        40000000,
        45,
        35,
    ),
    snapshot(
        2,
        date(2026, 6, 30),
        65000000,
        65,
        55,
    ),
    snapshot(
        3,
        date(2026, 12, 31),
        125000000,
        100,
        100,
        date(2027, 4, 1),
    ),
]


rows = build_project_training_rows(snapshots)

print("\n=== GENERATED TRAINING DATASET ===\n")

for index, row in enumerate(rows, start=1):
    print(f"--- Training Row {index} ---")

    for key, value in row.items():
        print(f"{key}: {value}")

    print()