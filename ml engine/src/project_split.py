import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# AUREX 2.0
# PROJECT-AWARE TRAIN / VALIDATION / TEST SPLIT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "model_ready_dataset.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "splits"
)


# ============================================================
# SETTINGS
# ============================================================

RANDOM_SEED = 42

TRAIN_PROJECTS = 154
VALIDATION_PROJECTS = 33
TEST_PROJECTS = 33


def main():

    print("=" * 70)
    print("AUREX 2.0 - PROJECT-AWARE DATA SPLIT")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Load model-ready dataset
    # --------------------------------------------------------

    print("\n[1] Loading model-ready dataset...")

    if not INPUT_FILE.exists():

        print("ERROR: model_ready_dataset.csv not found.")
        print(INPUT_FILE)
        print(
            "\nFirst run:"
        )
        print(
            "python src/feature_engineering.py"
        )
        return

    df = pd.read_csv(INPUT_FILE)

    print(
        f"Rows    : {len(df):,}"
    )

    print(
        f"Columns : {len(df.columns):,}"
    )

    # --------------------------------------------------------
    # 2. Check project_id
    # --------------------------------------------------------

    print("\n[2] Checking project IDs...")

    if "project_id" not in df.columns:

        print(
            "ERROR: project_id column is missing."
        )

        return

    project_ids = (
        df["project_id"]
        .dropna()
        .unique()
    )

    project_ids = np.array(
        project_ids
    )

    total_projects = len(project_ids)

    print(
        f"Unique projects: "
        f"{total_projects}"
    )

    # --------------------------------------------------------
    # 3. Validate requested split
    # --------------------------------------------------------

    requested_projects = (
        TRAIN_PROJECTS
        + VALIDATION_PROJECTS
        + TEST_PROJECTS
    )

    if total_projects != requested_projects:

        print(
            "\nWARNING:"
        )

        print(
            f"Dataset contains {total_projects} "
            f"projects."
        )

        print(
            f"Requested split requires "
            f"{requested_projects} projects."
        )

        print(
            "The script will calculate the split "
            "proportionally."
        )

        train_count = round(
            total_projects * 0.70
        )

        validation_count = round(
            total_projects * 0.15
        )

        test_count = (
            total_projects
            - train_count
            - validation_count
        )

    else:

        train_count = TRAIN_PROJECTS
        validation_count = VALIDATION_PROJECTS
        test_count = TEST_PROJECTS

    # --------------------------------------------------------
    # 4. Reproducible project shuffle
    # --------------------------------------------------------

    print(
        "\n[3] Creating reproducible "
        "project-level split..."
    )

    rng = np.random.default_rng(
        RANDOM_SEED
    )

    shuffled_projects = (
        project_ids.copy()
    )

    rng.shuffle(
        shuffled_projects
    )

    # --------------------------------------------------------
    # 5. Assign projects
    # --------------------------------------------------------

    train_projects = (
        shuffled_projects[
            :train_count
        ]
    )

    validation_projects = (
        shuffled_projects[
            train_count:
            train_count + validation_count
        ]
    )

    test_projects = (
        shuffled_projects[
            train_count + validation_count:
        ]
    )

    # --------------------------------------------------------
    # 6. Create split column
    # --------------------------------------------------------

    print(
        "\n[4] Assigning observations..."
    )

    train_set = set(
        train_projects
    )

    validation_set = set(
        validation_projects
    )

    test_set = set(
        test_projects
    )

    def assign_split(project_id):

        if project_id in train_set:
            return "train"

        if project_id in validation_set:
            return "validation"

        if project_id in test_set:
            return "test"

        return "unknown"

    df["split"] = (
        df["project_id"]
        .apply(assign_split)
    )

    # --------------------------------------------------------
    # 7. Check unknown projects
    # --------------------------------------------------------

    unknown_count = (
        df["split"]
        .eq("unknown")
        .sum()
    )

    if unknown_count > 0:

        print(
            f"ERROR: {unknown_count:,} "
            "rows have unknown split."
        )

        return

    # --------------------------------------------------------
    # 8. Create individual datasets
    # --------------------------------------------------------

    train_df = df[
        df["split"] == "train"
    ].copy()

    validation_df = df[
        df["split"] == "validation"
    ].copy()

    test_df = df[
        df["split"] == "test"
    ].copy()

    # --------------------------------------------------------
    # 9. Verify project purity
    # --------------------------------------------------------

    print(
        "\n[5] Checking project purity..."
    )

    train_project_set = set(
        train_df["project_id"].unique()
    )

    validation_project_set = set(
        validation_df["project_id"].unique()
    )

    test_project_set = set(
        test_df["project_id"].unique()
    )

    train_validation_overlap = (
        train_project_set
        & validation_project_set
    )

    train_test_overlap = (
        train_project_set
        & test_project_set
    )

    validation_test_overlap = (
        validation_project_set
        & test_project_set
    )

    print(
        "Train ↔ Validation overlap:",
        len(train_validation_overlap)
    )

    print(
        "Train ↔ Test overlap:",
        len(train_test_overlap)
    )

    print(
        "Validation ↔ Test overlap:",
        len(validation_test_overlap)
    )

    if (
        len(train_validation_overlap) > 0
        or len(train_test_overlap) > 0
        or len(validation_test_overlap) > 0
    ):

        print(
            "\nERROR: Project leakage detected."
        )

        return

    print(
        "PROJECT PURITY CHECK: PASSED"
    )

    # --------------------------------------------------------
    # 10. Create output directory
    # --------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # 11. Save datasets
    # --------------------------------------------------------

    print(
        "\n[6] Saving split datasets..."
    )

    train_file = (
        OUTPUT_DIR
        / "train.csv"
    )

    validation_file = (
        OUTPUT_DIR
        / "validation.csv"
    )

    test_file = (
        OUTPUT_DIR
        / "test.csv"
    )

    all_split_file = (
        OUTPUT_DIR
        / "all_data_with_split.csv"
    )

    train_df.to_csv(
        train_file,
        index=False
    )

    validation_df.to_csv(
        validation_file,
        index=False
    )

    test_df.to_csv(
        test_file,
        index=False
    )

    df.to_csv(
        all_split_file,
        index=False
    )

    # --------------------------------------------------------
    # 12. Final report
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("PROJECT-AWARE SPLIT COMPLETE")
    print("=" * 70)

    print("\nPROJECT COUNTS")

    print(
        f"Train      : "
        f"{len(train_project_set)}"
    )

    print(
        f"Validation : "
        f"{len(validation_project_set)}"
    )

    print(
        f"Test       : "
        f"{len(test_project_set)}"
    )

    print("\nROW COUNTS")

    print(
        f"Train      : "
        f"{len(train_df):,}"
    )

    print(
        f"Validation : "
        f"{len(validation_df):,}"
    )

    print(
        f"Test       : "
        f"{len(test_df):,}"
    )

    print(
        f"Total      : "
        f"{len(df):,}"
    )

    print("\nOUTPUT FILES")

    print(train_file)
    print(validation_file)
    print(test_file)
    print(all_split_file)

    print("\nSPLIT RULE")

    print(
        "Projects are split first, then all "
        "observations belonging to each project "
        "stay in the same split."
    )

    print(
        "\nRandom seed:"
        f" {RANDOM_SEED}"
    )

    print(
        "\nNext step:"
    )

    print(
        "Build statistical baseline models."
    )


if __name__ == "__main__":
    main()