import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# AUREX 2.0
# STATISTICAL BASELINE vs ML MODEL COMPARISON
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "output"

BASELINE_FILE = OUTPUT_DIR / "baseline_results.csv"
ML_FILE = OUTPUT_DIR / "model_evaluation_results.csv"

COMPARISON_FILE = OUTPUT_DIR / "baseline_vs_ml_comparison.csv"


# ============================================================
# HELPERS
# ============================================================

def find_column(df, possible_names):

    lower_columns = {
        str(column).lower(): column
        for column in df.columns
    }

    for name in possible_names:

        if name.lower() in lower_columns:
            return lower_columns[name.lower()]

    return None


def clean_text(value):

    if pd.isna(value):
        return ""

    return str(value).strip().lower()


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("AUREX 2.0 - BASELINE vs ML COMPARISON")
    print("=" * 70)

    # --------------------------------------------------------
    # Check files
    # --------------------------------------------------------

    if not BASELINE_FILE.exists():

        print("\nERROR:")
        print("Baseline results file not found:")
        print(BASELINE_FILE)
        return

    if not ML_FILE.exists():

        print("\nERROR:")
        print("ML evaluation file not found:")
        print(ML_FILE)
        return

    # --------------------------------------------------------
    # Load files
    # --------------------------------------------------------

    baseline = pd.read_csv(
        BASELINE_FILE
    )

    ml = pd.read_csv(
        ML_FILE
    )

    print("\nFiles loaded successfully.")

    print(
        f"Baseline experiments : {len(baseline)}"
    )

    print(
        f"ML evaluation rows   : {len(ml)}"
    )

    # --------------------------------------------------------
    # Show available columns
    # --------------------------------------------------------

    print("\nBaseline columns:")
    print(
        list(baseline.columns)
    )

    print("\nML evaluation columns:")
    print(
        list(ml.columns)
    )

    # --------------------------------------------------------
    # Detect important columns
    # --------------------------------------------------------

    baseline_model_col = find_column(
        baseline,
        [
            "model",
            "baseline_model",
            "method"
        ]
    )

    baseline_task_col = find_column(
        baseline,
        [
            "task",
            "problem",
            "type"
        ]
    )

    baseline_target_col = find_column(
        baseline,
        [
            "target",
            "target_name"
        ]
    )

    ml_model_col = find_column(
        ml,
        [
            "model"
        ]
    )

    ml_task_col = find_column(
        ml,
        [
            "task"
        ]
    )

    ml_target_col = find_column(
        ml,
        [
            "target"
        ]
    )

    # --------------------------------------------------------
    # Validate detected columns
    # --------------------------------------------------------

    print("\nDetected columns:")

    print(
        "Baseline model :",
        baseline_model_col
    )

    print(
        "Baseline task  :",
        baseline_task_col
    )

    print(
        "Baseline target:",
        baseline_target_col
    )

    print(
        "ML model       :",
        ml_model_col
    )

    print(
        "ML task        :",
        ml_task_col
    )

    print(
        "ML target      :",
        ml_target_col
    )

    # --------------------------------------------------------
    # If no model column exists, create one
    # --------------------------------------------------------

    if baseline_model_col is None:

        baseline["model"] = "Statistical Baseline"

        baseline_model_col = "model"

    if baseline_task_col is None:

        baseline["task"] = "unknown"

        baseline_task_col = "task"

    if baseline_target_col is None:

        baseline["target"] = "unknown"

        baseline_target_col = "target"

    if ml_model_col is None:

        print(
            "\nERROR: ML model column could not be detected."
        )

        return

    if ml_task_col is None:

        ml["task"] = "unknown"

        ml_task_col = "task"

    if ml_target_col is None:

        ml["target"] = "unknown"

        ml_target_col = "target"

    # --------------------------------------------------------
    # Normalize matching fields
    # --------------------------------------------------------

    baseline["_task_key"] = (
        baseline[baseline_task_col]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    baseline["_target_key"] = (
        baseline[baseline_target_col]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    ml["_task_key"] = (
        ml[ml_task_col]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    ml["_target_key"] = (
        ml[ml_target_col]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # --------------------------------------------------------
    # Identify metrics
    # --------------------------------------------------------

    baseline_mae = find_column(
        baseline,
        [
            "test_mae",
            "mae",
            "validation_mae"
        ]
    )

    baseline_rmse = find_column(
        baseline,
        [
            "test_rmse",
            "rmse",
            "validation_rmse"
        ]
    )

    baseline_r2 = find_column(
        baseline,
        [
            "test_r2",
            "r2",
            "validation_r2"
        ]
    )

    baseline_accuracy = find_column(
        baseline,
        [
            "test_accuracy",
            "accuracy",
            "validation_accuracy"
        ]
    )

    baseline_f1 = find_column(
        baseline,
        [
            "test_f1",
            "f1",
            "macro_f1",
            "validation_f1"
        ]
    )

    # --------------------------------------------------------
    # Build comparison
    # --------------------------------------------------------

    comparison_rows = []

    print("\n" + "=" * 70)
    print("COMPARISON")
    print("=" * 70)

    for _, ml_row in ml.iterrows():

        ml_task = ml_row["_task_key"]
        ml_target = ml_row["_target_key"]

        matching = baseline[
            (
                baseline["_task_key"]
                == ml_task
            )
            &
            (
                baseline["_target_key"]
                == ml_target
            )
        ]

        # If exact task/target match doesn't exist,
        # try matching by task only.

        if matching.empty:

            matching = baseline[
                baseline["_task_key"]
                == ml_task
            ]

        if matching.empty:

            print(
                f"\nNo matching baseline found for:"
            )

            print(
                f"ML model: {ml_row[ml_model_col]}"
            )

            print(
                f"Task: {ml_row[ml_task_col]}"
            )

            print(
                f"Target: {ml_row[ml_target_col]}"
            )

            continue

        # ----------------------------------------------------
        # Regression comparison
        # ----------------------------------------------------

        if ml_task == "regression":

            for _, base_row in matching.iterrows():

                row = {
                    "task":
                        ml_row[ml_task_col],

                    "target":
                        ml_row[ml_target_col],

                    "ml_model":
                        ml_row[ml_model_col],

                    "baseline_model":
                        base_row[baseline_model_col]
                }

                # ML metrics

                row["ml_test_mae"] = (
                    ml_row.get(
                        "test_mae",
                        np.nan
                    )
                )

                row["ml_test_rmse"] = (
                    ml_row.get(
                        "test_rmse",
                        np.nan
                    )
                )

                row["ml_test_r2"] = (
                    ml_row.get(
                        "test_r2",
                        np.nan
                    )
                )

                # Baseline metrics

                if baseline_mae:

                    row["baseline_mae"] = (
                        base_row[
                            baseline_mae
                        ]
                    )

                else:

                    row["baseline_mae"] = np.nan

                if baseline_rmse:

                    row["baseline_rmse"] = (
                        base_row[
                            baseline_rmse
                        ]
                    )

                else:

                    row["baseline_rmse"] = np.nan

                if baseline_r2:

                    row["baseline_r2"] = (
                        base_row[
                            baseline_r2
                        ]
                    )

                else:

                    row["baseline_r2"] = np.nan

                # Improvement

                if (
                    pd.notna(
                        row["baseline_mae"]
                    )
                    and
                    pd.notna(
                        row["ml_test_mae"]
                    )
                ):

                    row["mae_improvement_percent"] = (
                        (
                            row["baseline_mae"]
                            -
                            row["ml_test_mae"]
                        )
                        /
                        abs(
                            row["baseline_mae"]
                        )
                        *
                        100
                    )

                else:

                    row[
                        "mae_improvement_percent"
                    ] = np.nan

                if (
                    pd.notna(
                        row["baseline_r2"]
                    )
                    and
                    pd.notna(
                        row["ml_test_r2"]
                    )
                ):

                    row["r2_improvement"] = (
                        row["ml_test_r2"]
                        -
                        row["baseline_r2"]
                    )

                else:

                    row["r2_improvement"] = np.nan

                comparison_rows.append(
                    row
                )

        # ----------------------------------------------------
        # Classification comparison
        # ----------------------------------------------------

        else:

            for _, base_row in matching.iterrows():

                row = {
                    "task":
                        ml_row[ml_task_col],

                    "target":
                        ml_row[ml_target_col],

                    "ml_model":
                        ml_row[ml_model_col],

                    "baseline_model":
                        base_row[baseline_model_col]
                }

                row["ml_test_accuracy"] = (
                    ml_row.get(
                        "test_accuracy",
                        np.nan
                    )
                )

                row["ml_test_f1"] = (
                    ml_row.get(
                        "test_f1",
                        np.nan
                    )
                )

                if baseline_accuracy:

                    row["baseline_accuracy"] = (
                        base_row[
                            baseline_accuracy
                        ]
                    )

                else:

                    row[
                        "baseline_accuracy"
                    ] = np.nan

                if baseline_f1:

                    row["baseline_f1"] = (
                        base_row[
                            baseline_f1
                        ]
                    )

                else:

                    row[
                        "baseline_f1"
                    ] = np.nan

                if (
                    pd.notna(
                        row["baseline_accuracy"]
                    )
                    and
                    pd.notna(
                        row["ml_test_accuracy"]
                    )
                ):

                    row[
                        "accuracy_difference"
                    ] = (
                        row["ml_test_accuracy"]
                        -
                        row["baseline_accuracy"]
                    )

                else:

                    row[
                        "accuracy_difference"
                    ] = np.nan

                if (
                    pd.notna(
                        row["baseline_f1"]
                    )
                    and
                    pd.notna(
                        row["ml_test_f1"]
                    )
                ):

                    row[
                        "f1_difference"
                    ] = (
                        row["ml_test_f1"]
                        -
                        row["baseline_f1"]
                    )

                else:

                    row[
                        "f1_difference"
                    ] = np.nan

                comparison_rows.append(
                    row
                )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    comparison_df = pd.DataFrame(
        comparison_rows
    )

    comparison_df.to_csv(
        COMPARISON_FILE,
        index=False
    )

    print("\n" + "=" * 70)
    print("BASELINE vs ML COMPARISON COMPLETE")
    print("=" * 70)

    print(
        f"Comparison rows: "
        f"{len(comparison_df)}"
    )

    print(
        f"Saved to:"
    )

    print(
        COMPARISON_FILE
    )

    if not comparison_df.empty:

        print(
            "\nComparison results:"
        )

        print(
            comparison_df.to_string(
                index=False
            )
        )

    print(
        "\nNext step:"
    )

    print(
        "Build prediction and early-warning outputs."
    )


if __name__ == "__main__":
    main()