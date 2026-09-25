import pandas as pd
from pathlib import Path


# ============================================================
# AUREX 2.0 - FEATURE ENGINEERING
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "cleaned_master_project_snapshots.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "model_ready_dataset.csv"
)


# ============================================================
# COLUMNS THAT MUST NEVER BE USED AS MODEL FEATURES
# ============================================================

FORBIDDEN_FEATURE_PATTERNS = [
    "target_",
    "outcome_after_cutoff",
]

FORBIDDEN_EXACT_COLUMNS = [
    "actual_end_date",
]


def is_forbidden_column(column):

    column_lower = column.lower()

    # Target/outcome columns
    for pattern in FORBIDDEN_FEATURE_PATTERNS:

        if pattern in column_lower:
            return True

    # Known future information
    if column in FORBIDDEN_EXACT_COLUMNS:
        return True

    return False


def main():

    print("=" * 70)
    print("AUREX 2.0 - FEATURE ENGINEERING")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Load cleaned dataset
    # --------------------------------------------------------

    print("\n[1] Loading cleaned dataset...")

    if not INPUT_FILE.exists():

        print("ERROR: Cleaned dataset not found.")
        print(INPUT_FILE)
        return

    df = pd.read_csv(INPUT_FILE)

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns):,}")

    # --------------------------------------------------------
    # 2. Convert date
    # --------------------------------------------------------

    print("\n[2] Processing dates...")

    if "observation_date" in df.columns:

        df["observation_date"] = pd.to_datetime(
            df["observation_date"],
            errors="coerce"
        )

        # Useful calendar features
        df["observation_year"] = (
            df["observation_date"].dt.year
        )

        df["observation_month"] = (
            df["observation_date"].dt.month
        )

        df["observation_quarter"] = (
            df["observation_date"].dt.quarter
        )

    # --------------------------------------------------------
    # 3. Create safe numeric features
    # --------------------------------------------------------

    print("\n[3] Creating derived features...")

    # Progress remaining
    if (
        "planned_progress_percent" in df.columns
        and "actual_progress_percent" in df.columns
    ):

        df["progress_remaining_percent"] = (
            100
            - df["actual_progress_percent"]
        )

    # Progress gap
    if (
        "planned_progress_percent" in df.columns
        and "actual_progress_percent" in df.columns
    ):

        df["progress_gap_engineered"] = (
            df["planned_progress_percent"]
            - df["actual_progress_percent"]
        )

    # Cost growth
    if (
        "original_cost_crore" in df.columns
        and "current_baseline_cost_crore" in df.columns
    ):

        denominator = (
            df["original_cost_crore"]
            .replace(0, pd.NA)
        )

        df["baseline_cost_growth_percent"] = (
            (
                df["current_baseline_cost_crore"]
                - df["original_cost_crore"]
            )
            / denominator
            * 100
        )

    # Expenditure vs current baseline
    if (
        "actual_expenditure_crore" in df.columns
        and "current_baseline_cost_crore" in df.columns
    ):

        denominator = (
            df["current_baseline_cost_crore"]
            .replace(0, pd.NA)
        )

        df["expenditure_vs_baseline_percent"] = (
            df["actual_expenditure_crore"]
            / denominator
            * 100
        )

    # --------------------------------------------------------
    # 4. Identify target columns
    # --------------------------------------------------------

    print("\n[4] Identifying targets...")

    target_columns = [
        column
        for column in df.columns
        if column.startswith("target_")
    ]

    print(
        f"Target columns found: "
        f"{len(target_columns)}"
    )

    for column in target_columns:

        print(f"  - {column}")

    # --------------------------------------------------------
    # 5. Identify forbidden columns
    # --------------------------------------------------------

    print("\n[5] Removing leakage-prone columns...")

    forbidden_columns = []

    for column in df.columns:

        if is_forbidden_column(column):

            forbidden_columns.append(column)

    print(
        f"Forbidden columns: "
        f"{len(forbidden_columns)}"
    )

    for column in forbidden_columns:

        print(f"  - {column}")

    # --------------------------------------------------------
    # 6. Build feature list
    # --------------------------------------------------------

    print("\n[6] Building model feature list...")

    feature_columns = []

    for column in df.columns:

        if column in forbidden_columns:
            continue

        if column == "project_id":
            continue

        if column == "project_name":
            continue

        if column == "observation_date":
            continue

        feature_columns.append(column)

    print(
        f"Candidate feature columns: "
        f"{len(feature_columns)}"
    )

    # --------------------------------------------------------
    # 7. Keep only useful numeric/categorical features
    # --------------------------------------------------------

    numeric_features = [
        column
        for column in feature_columns
        if pd.api.types.is_numeric_dtype(
            df[column]
        )
    ]

    categorical_features = [
        column
        for column in feature_columns
        if (
            df[column].dtype == "object"
            or str(df[column].dtype).startswith("category")
        )
    ]

    print(
        f"Numeric features     : "
        f"{len(numeric_features)}"
    )

    print(
        f"Categorical features : "
        f"{len(categorical_features)}"
    )

    # --------------------------------------------------------
    # 8. Print feature list
    # --------------------------------------------------------

    print("\n[7] MODEL FEATURES")

    for number, column in enumerate(
        feature_columns,
        start=1
    ):

        print(
            f"{number:3}. {column}"
        )

    # --------------------------------------------------------
    # 9. Missing-value report for features
    # --------------------------------------------------------

    print("\n[8] FEATURE MISSING VALUES")

    feature_missing = (
        df[feature_columns]
        .isna()
        .sum()
    )

    feature_missing = (
        feature_missing[
            feature_missing > 0
        ]
        .sort_values(
            ascending=False
        )
    )

    if len(feature_missing) == 0:

        print("No missing feature values.")

    else:

        for column, count in feature_missing.items():

            percentage = (
                count
                / len(df)
                * 100
            )

            print(
                f"{column:<55}"
                f"{count:>6,} "
                f"({percentage:>6.2f}%)"
            )

    # --------------------------------------------------------
    # 10. Create model-ready dataset
    # --------------------------------------------------------

    print("\n[9] Creating model-ready dataset...")

    # Keep identifiers, targets and features.
    keep_columns = []

    # Project identifier
    if "project_id" in df.columns:

        keep_columns.append("project_id")

    # Date
    if "observation_date" in df.columns:

        keep_columns.append("observation_date")

    # Features
    for column in feature_columns:

        if column not in keep_columns:

            keep_columns.append(column)

    # Targets
    for column in target_columns:

        if column not in keep_columns:

            keep_columns.append(column)

    model_df = df[
        keep_columns
    ].copy()

    # --------------------------------------------------------
    # 11. Save model-ready dataset
    # --------------------------------------------------------

    model_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        "\nSaved model-ready dataset:"
    )

    print(OUTPUT_FILE)

    # --------------------------------------------------------
    # 12. Final summary
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("FEATURE ENGINEERING COMPLETE")
    print("=" * 70)

    print(
        f"Rows              : "
        f"{len(model_df):,}"
    )

    print(
        f"Total columns     : "
        f"{len(model_df.columns):,}"
    )

    print(
        f"Model features    : "
        f"{len(feature_columns):,}"
    )

    print(
        f"Target columns    : "
        f"{len(target_columns):,}"
    )

    print(
        "\nImportant:"
    )

    print(
        "Target and known future-outcome columns "
        "were excluded from model features."
    )

    print(
        "\nNext step:"
    )

    print(
        "Build project-aware train/validation/test "
        "splits and statistical baselines."
    )


if __name__ == "__main__":
    main()