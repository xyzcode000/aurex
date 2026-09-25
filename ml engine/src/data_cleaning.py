import pandas as pd
from pathlib import Path


# ============================================================
# AUREX 2.0 - DATA CLEANING
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "master_project_snapshots.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "cleaned_master_project_snapshots.csv"
)


def main():

    print("=" * 70)
    print("AUREX 2.0 - DATA CLEANING")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Load raw dataset
    # --------------------------------------------------------

    print("\n[1] Loading raw dataset...")

    if not INPUT_FILE.exists():
        print("ERROR: Raw dataset not found.")
        print(INPUT_FILE)
        return

    df = pd.read_csv(INPUT_FILE)

    print(f"Loaded {len(df):,} rows.")
    print(f"Loaded {len(df.columns):,} columns.")

    # --------------------------------------------------------
    # 2. Make a copy
    # --------------------------------------------------------

    df_clean = df.copy()

    # --------------------------------------------------------
    # 3. Remove completely empty columns
    # --------------------------------------------------------

    print("\n[2] Checking completely empty columns...")

    empty_columns = [
        column
        for column in df_clean.columns
        if df_clean[column].isna().all()
    ]

    if empty_columns:

        print("Removing completely empty columns:")

        for column in empty_columns:
            print(f"  - {column}")

        df_clean = df_clean.drop(
            columns=empty_columns
        )

    else:

        print("No completely empty columns.")

    # --------------------------------------------------------
    # 4. Convert observation date
    # --------------------------------------------------------

    print("\n[3] Processing observation_date...")

    if "observation_date" in df_clean.columns:

        df_clean["observation_date"] = pd.to_datetime(
            df_clean["observation_date"],
            errors="coerce"
        )

        invalid_dates = (
            df_clean["observation_date"].isna().sum()
        )

        print(
            f"Invalid observation dates: "
            f"{invalid_dates:,}"
        )

    # --------------------------------------------------------
    # 5. Remove exact duplicate rows
    # --------------------------------------------------------

    print("\n[4] Checking exact duplicate rows...")

    duplicate_rows = df_clean.duplicated().sum()

    print(
        f"Exact duplicate rows: "
        f"{duplicate_rows:,}"
    )

    if duplicate_rows > 0:

        df_clean = df_clean.drop_duplicates()

        print(
            f"Removed {duplicate_rows:,} duplicate rows."
        )

    # --------------------------------------------------------
    # 6. Check duplicate project/date combinations
    # --------------------------------------------------------

    print(
        "\n[5] Checking project/date duplicates..."
    )

    if (
        "project_id" in df_clean.columns
        and "observation_date" in df_clean.columns
    ):

        duplicate_project_dates = df_clean.duplicated(
            subset=[
                "project_id",
                "observation_date"
            ]
        ).sum()

        print(
            "Duplicate project/date rows: "
            f"{duplicate_project_dates:,}"
        )

        if duplicate_project_dates > 0:

            print(
                "WARNING: Project/date duplicates exist."
            )

            print(
                "Keeping the first observation "
                "for each project/date."
            )

            df_clean = df_clean.drop_duplicates(
                subset=[
                    "project_id",
                    "observation_date"
                ],
                keep="first"
            )

    # --------------------------------------------------------
    # 7. Check project IDs
    # --------------------------------------------------------

    print("\n[6] Checking project IDs...")

    if "project_id" in df_clean.columns:

        missing_project_ids = (
            df_clean["project_id"].isna().sum()
        )

        print(
            f"Missing project IDs: "
            f"{missing_project_ids:,}"
        )

        if missing_project_ids > 0:

            df_clean = df_clean[
                df_clean["project_id"].notna()
            ].copy()

    # --------------------------------------------------------
    # 8. Check numeric columns for infinite values
    # --------------------------------------------------------

    print(
        "\n[7] Checking infinite numeric values..."
    )

    numeric_columns = df_clean.select_dtypes(
        include="number"
    ).columns

    total_infinite = 0

    for column in numeric_columns:

        infinite_count = (
            df_clean[column]
            .isin([float("inf"), float("-inf")])
            .sum()
        )

        if infinite_count > 0:

            print(
                f"{column}: "
                f"{infinite_count:,} infinite values"
            )

            total_infinite += infinite_count

            df_clean[column] = (
                df_clean[column]
                .replace(
                    [float("inf"), float("-inf")],
                    pd.NA
                )
            )

    if total_infinite == 0:

        print("No infinite values found.")

    # --------------------------------------------------------
    # 9. IMPORTANT:
    # Do NOT fill missing values blindly.
    # --------------------------------------------------------

    print(
        "\n[8] Missing-value policy..."
    )

    missing_columns = (
        df_clean.isna()
        .sum()
    )

    missing_columns = (
        missing_columns[
            missing_columns > 0
        ]
        .sort_values(
            ascending=False
        )
    )

    if len(missing_columns) == 0:

        print("No missing values.")

    else:

        print(
            "Missing values will NOT be blindly "
            "replaced with zero."
        )

        print(
            "\nColumns containing missing values:"
        )

        for column, count in missing_columns.items():

            percentage = (
                count
                / len(df_clean)
                * 100
            )

            print(
                f"  {column:<55}"
                f"{count:>6,} "
                f"({percentage:>6.2f}%)"
            )

    # --------------------------------------------------------
    # 10. Basic progress validation
    # --------------------------------------------------------

    print(
        "\n[9] Checking progress values..."
    )

    progress_columns = [
        column
        for column in df_clean.columns
        if "progress" in column.lower()
        and "target_" not in column
    ]

    for column in progress_columns:

        if pd.api.types.is_numeric_dtype(
            df_clean[column]
        ):

            below_zero = (
                df_clean[column] < 0
            ).sum()

            above_hundred = (
                df_clean[column] > 100
            ).sum()

            print(
                f"{column}: "
                f"<0 = {below_zero:,}, "
                f">100 = {above_hundred:,}"
            )

    # --------------------------------------------------------
    # 11. Save cleaned dataset
    # --------------------------------------------------------

    print(
        "\n[10] Saving cleaned dataset..."
    )

    df_clean.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"Saved cleaned dataset to:"
    )

    print(OUTPUT_FILE)

    # --------------------------------------------------------
    # 12. Final summary
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("DATA CLEANING COMPLETE")
    print("=" * 70)

    print(
        f"Original rows : {len(df):,}"
    )

    print(
        f"Cleaned rows  : {len(df_clean):,}"
    )

    print(
        f"Columns       : {len(df_clean.columns):,}"
    )

    if "project_id" in df_clean.columns:

        print(
            f"Projects      : "
            f"{df_clean['project_id'].nunique():,}"
        )

    print("\nRAW DATA WAS NOT MODIFIED.")

    print(
        "\nNext step:"
    )

    print(
        "Leakage-safe feature selection "
        "and feature engineering."
    )


if __name__ == "__main__":
    main()