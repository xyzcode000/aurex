import pandas as pd
from pathlib import Path


# ============================================================
# AUREX 2.0 - DATA AUDIT
# ============================================================

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "master_project_snapshots.csv"


def main():
    print("=" * 70)
    print("AUREX 2.0 - DATA AUDIT")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Load dataset
    # --------------------------------------------------------
    print("\n[1] Loading dataset...")

    if not DATA_FILE.exists():
        print(f"ERROR: Dataset not found:")
        print(DATA_FILE)
        return

    df = pd.read_csv(DATA_FILE)

    print("Dataset loaded successfully.")

    # --------------------------------------------------------
    # 2. Basic dataset information
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("[2] BASIC DATASET INFORMATION")
    print("=" * 70)

    print(f"Rows       : {df.shape[0]:,}")
    print(f"Columns    : {df.shape[1]:,}")

    if "project_id" in df.columns:
        print(f"Projects   : {df['project_id'].nunique():,}")

    # --------------------------------------------------------
    # 3. Date information
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("[3] DATE INFORMATION")
    print("=" * 70)

    if "observation_date" in df.columns:

        df["observation_date"] = pd.to_datetime(
            df["observation_date"],
            errors="coerce"
        )

        invalid_dates = df["observation_date"].isna().sum()

        print(f"Invalid dates : {invalid_dates:,}")

        if df["observation_date"].notna().any():
            print(
                "Start date   :",
                df["observation_date"].min().date()
            )

            print(
                "End date     :",
                df["observation_date"].max().date()
            )

    else:
        print("WARNING: observation_date column not found.")

    # --------------------------------------------------------
    # 4. Observations per project
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("[4] OBSERVATIONS PER PROJECT")
    print("=" * 70)

    if "project_id" in df.columns:

        observations = df.groupby("project_id").size()

        print(f"Minimum observations : {observations.min()}")
        print(f"Median observations  : {observations.median():.0f}")
        print(f"Maximum observations : {observations.max()}")

    # --------------------------------------------------------
    # 5. Column names
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("[5] ALL COLUMNS")
    print("=" * 70)

    for number, column in enumerate(df.columns, start=1):
        print(f"{number:2}. {column}")

    # --------------------------------------------------------
    # 6. Target columns
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("[6] TARGET COLUMNS")
    print("=" * 70)

    target_columns = [
        column
        for column in df.columns
        if column.startswith("target_")
    ]

    print(f"Number of target columns: {len(target_columns)}")

    for column in target_columns:
        print(f"- {column}")

    # --------------------------------------------------------
    # 7. Missing values
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("[7] MISSING VALUES")
    print("=" * 70)

    missing = df.isna().sum()

    missing = missing[missing > 0].sort_values(
        ascending=False
    )

    if len(missing) == 0:
        print("No missing values found.")
    else:
        for column, count in missing.items():
            percentage = count / len(df) * 100

            print(
                f"{column:<55} "
                f"{count:>6,} "
                f"({percentage:>6.2f}%)"
            )

    # --------------------------------------------------------
    # 8. Duplicate project/date observations
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("[8] DUPLICATE PROJECT + DATE CHECK")
    print("=" * 70)

    if "project_id" in df.columns and "observation_date" in df.columns:

        duplicates = df.duplicated(
            subset=["project_id", "observation_date"]
        ).sum()

        print(
            f"Duplicate project/date rows: {duplicates:,}"
        )

    # --------------------------------------------------------
    # 9. Data types
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("[9] DATA TYPES")
    print("=" * 70)

    print(df.dtypes.to_string())

    # --------------------------------------------------------
    # 10. Cost overrun target
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("[10] COST OVERRUN TARGET")
    print("=" * 70)

    column = "target_cost_overrun_flag"

    if column in df.columns:

        print(
            df[column]
            .value_counts(dropna=False)
            .sort_index()
            .to_string()
        )

        print("\nPercentage:")
        print(
            (
                df[column]
                .value_counts(normalize=True, dropna=False)
                .sort_index()
                * 100
            ).round(2).to_string()
        )

    else:
        print(f"{column} not found.")

    # --------------------------------------------------------
    # 11. Time overrun target
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("[11] TIME OVERRUN TARGET")
    print("=" * 70)

    column = "target_time_overrun_flag"

    if column in df.columns:

        print(
            df[column]
            .value_counts(dropna=False)
            .sort_index()
            .to_string()
        )

        print("\nPercentage:")
        print(
            (
                df[column]
                .value_counts(normalize=True, dropna=False)
                .sort_index()
                * 100
            ).round(2).to_string()
        )

    else:
        print(f"{column} not found.")

    # --------------------------------------------------------
    # 12. Early warning target
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("[12] EARLY WARNING TARGET")
    print("=" * 70)

    column = "target_early_warning_flag_90d"

    if column in df.columns:

        print(
            df[column]
            .value_counts(dropna=False)
            .sort_index()
            .to_string()
        )

        print("\nPercentage:")
        print(
            (
                df[column]
                .value_counts(normalize=True, dropna=False)
                .sort_index()
                * 100
            ).round(2).to_string()
        )

    else:
        print(f"{column} not found.")

    # --------------------------------------------------------
    # 13. Risk level target
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("[13] FUTURE RISK LEVEL")
    print("=" * 70)

    column = "target_future_risk_level"

    if column in df.columns:

        print(
            df[column]
            .value_counts(dropna=False)
            .to_string()
        )

    else:
        print(f"{column} not found.")

    # --------------------------------------------------------
    # 14. Recommended project-aware split
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("[14] PROJECT-AWARE SPLIT")
    print("=" * 70)

    split_columns = [
        column
        for column in df.columns
        if "recommended_split_project_aware" in column
    ]

    if split_columns:

        for column in split_columns:
            print(f"\n{column}")
            print(df[column].value_counts(dropna=False).to_string())

    else:
        print(
            "No recommended project-aware split column found."
        )

    # --------------------------------------------------------
    # 15. Numerical summary
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("[15] NUMERICAL SUMMARY")
    print("=" * 70)

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns

    print(
        df[numerical_columns]
        .describe()
        .T
        .to_string()
    )

    # --------------------------------------------------------
    # 16. Final summary
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("DATA AUDIT COMPLETE")
    print("=" * 70)

    print(f"Rows              : {len(df):,}")
    print(f"Columns           : {len(df.columns):,}")

    if "project_id" in df.columns:
        print(
            f"Unique projects   : "
            f"{df['project_id'].nunique():,}"
        )

    print(
        f"Target columns    : "
        f"{len(target_columns)}"
    )

    print("\nNext step:")
    print("Data cleaning and leakage-safe preparation.")


if __name__ == "__main__":
    main()