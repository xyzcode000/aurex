import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# AUREX 2.0
# STATISTICAL BASELINE MODELS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SPLIT_DIR = (
    PROJECT_ROOT
    / "data"
    / "splits"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "output"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "baseline_results.csv"
)


# ============================================================
# TARGET DEFINITIONS
# ============================================================

REGRESSION_TARGETS = [
    "target_future_cost_overrun_percent_vs_original",
    "target_future_cost_overrun_percent_vs_current",
    "target_future_delay_days",
    "target_future_time_overrun_percent",
    "target_future_risk_score",
]


CLASSIFICATION_TARGETS = [
    "target_cost_overrun_flag",
    "target_time_overrun_flag",
    "target_future_risk_level",
    "target_early_warning_flag_90d",
]


# ============================================================
# REGRESSION METRICS
# ============================================================

def regression_metrics(
    actual,
    predicted
):

    actual = np.asarray(
        actual,
        dtype=float
    )

    predicted = np.asarray(
        predicted,
        dtype=float
    )

    valid = (
        np.isfinite(actual)
        & np.isfinite(predicted)
    )

    actual = actual[valid]
    predicted = predicted[valid]

    if len(actual) == 0:

        return {
            "mae": np.nan,
            "rmse": np.nan,
            "r2": np.nan
        }

    mae = np.mean(
        np.abs(
            actual - predicted
        )
    )

    rmse = np.sqrt(
        np.mean(
            (actual - predicted) ** 2
        )
    )

    denominator = np.sum(
        (actual - np.mean(actual)) ** 2
    )

    if denominator == 0:

        r2 = np.nan

    else:

        r2 = (
            1
            - (
                np.sum(
                    (actual - predicted) ** 2
                )
                / denominator
            )
        )

    return {
        "mae": mae,
        "rmse": rmse,
        "r2": r2
    }


# ============================================================
# CLASSIFICATION METRICS
# ============================================================

def classification_metrics(
    actual,
    predicted
):

    actual = pd.Series(
        actual
    ).astype(str)

    predicted = pd.Series(
        predicted
    ).astype(str)

    valid = (
        actual.notna()
        & predicted.notna()
    )

    actual = actual[valid]
    predicted = predicted[valid]

    if len(actual) == 0:

        return {
            "accuracy": np.nan,
            "macro_f1": np.nan
        }

    accuracy = (
        actual.values
        == predicted.values
    ).mean()

    classes = sorted(
        actual.unique()
    )

    f1_scores = []

    for class_name in classes:

        true_positive = (
            (actual == class_name)
            & (predicted == class_name)
        ).sum()

        false_positive = (
            (actual != class_name)
            & (predicted == class_name)
        ).sum()

        false_negative = (
            (actual == class_name)
            & (predicted != class_name)
        ).sum()

        if (
            true_positive
            + false_positive
        ) > 0:

            precision = (
                true_positive
                / (
                    true_positive
                    + false_positive
                )
            )

        else:

            precision = 0.0

        if (
            true_positive
            + false_negative
        ) > 0:

            recall = (
                true_positive
                / (
                    true_positive
                    + false_negative
                )
            )

        else:

            recall = 0.0

        if (
            precision + recall
        ) > 0:

            f1 = (
                2
                * precision
                * recall
                / (
                    precision
                    + recall
                )
            )

        else:

            f1 = 0.0

        f1_scores.append(f1)

    macro_f1 = np.mean(
        f1_scores
    )

    return {
        "accuracy": accuracy,
        "macro_f1": macro_f1
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("AUREX 2.0 - STATISTICAL BASELINES")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Check split files
    # --------------------------------------------------------

    print("\n[1] Loading project-aware splits...")

    train_file = (
        SPLIT_DIR
        / "train.csv"
    )

    validation_file = (
        SPLIT_DIR
        / "validation.csv"
    )

    test_file = (
        SPLIT_DIR
        / "test.csv"
    )

    if not train_file.exists():

        print(
            "ERROR: train.csv was not found."
        )

        print(
            "\nRun this first:"
        )

        print(
            "python src/project_split.py"
        )

        return

    train = pd.read_csv(
        train_file
    )

    validation = pd.read_csv(
        validation_file
    )

    test = pd.read_csv(
        test_file
    )

    print(
        f"Train rows      : {len(train):,}"
    )

    print(
        f"Validation rows : {len(validation):,}"
    )

    print(
        f"Test rows       : {len(test):,}"
    )

    # --------------------------------------------------------
    # 2. Prepare output
    # --------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    results = []

    # ========================================================
    # 3. REGRESSION BASELINES
    # ========================================================

    print("\n" + "=" * 70)
    print("REGRESSION BASELINES")
    print("=" * 70)

    for target in REGRESSION_TARGETS:

        if target not in train.columns:

            print(
                f"\nSkipping {target} "
                "(column not found)."
            )

            continue

        print(
            f"\nTarget: {target}"
        )

        # Remove missing target rows
        train_target = train[
            train[target].notna()
        ][target]

        validation_target = validation[
            validation[target].notna()
        ][target]

        test_target = test[
            test[target].notna()
        ][target]

        if len(train_target) == 0:

            print(
                "No training values available."
            )

            continue

        # ----------------------------------------------------
        # Mean baseline
        # ----------------------------------------------------

        mean_value = train_target.mean()

        validation_mean_prediction = np.full(
            len(validation_target),
            mean_value
        )

        test_mean_prediction = np.full(
            len(test_target),
            mean_value
        )

        validation_metrics = regression_metrics(
            validation_target,
            validation_mean_prediction
        )

        test_metrics = regression_metrics(
            test_target,
            test_mean_prediction
        )

        results.append({
            "target": target,
            "task": "regression",
            "baseline": "training_mean",
            "validation_mae": validation_metrics["mae"],
            "validation_rmse": validation_metrics["rmse"],
            "validation_r2": validation_metrics["r2"],
            "test_mae": test_metrics["mae"],
            "test_rmse": test_metrics["rmse"],
            "test_r2": test_metrics["r2"],
            "training_reference_value": mean_value
        })

        print(
            f"Mean baseline: "
            f"{mean_value:.4f}"
        )

        print(
            f"Validation MAE: "
            f"{validation_metrics['mae']:.4f}"
        )

        print(
            f"Test MAE: "
            f"{test_metrics['mae']:.4f}"
        )

        # ----------------------------------------------------
        # Median baseline
        # ----------------------------------------------------

        median_value = train_target.median()

        validation_median_prediction = np.full(
            len(validation_target),
            median_value
        )

        test_median_prediction = np.full(
            len(test_target),
            median_value
        )

        validation_metrics = regression_metrics(
            validation_target,
            validation_median_prediction
        )

        test_metrics = regression_metrics(
            test_target,
            test_median_prediction
        )

        results.append({
            "target": target,
            "task": "regression",
            "baseline": "training_median",
            "validation_mae": validation_metrics["mae"],
            "validation_rmse": validation_metrics["rmse"],
            "validation_r2": validation_metrics["r2"],
            "test_mae": test_metrics["mae"],
            "test_rmse": test_metrics["rmse"],
            "test_r2": test_metrics["r2"],
            "training_reference_value": median_value
        })

        print(
            f"Median baseline: "
            f"{median_value:.4f}"
        )

        print(
            f"Validation MAE: "
            f"{validation_metrics['mae']:.4f}"
        )

        print(
            f"Test MAE: "
            f"{test_metrics['mae']:.4f}"
        )

    # ========================================================
    # 4. CLASSIFICATION BASELINES
    # ========================================================

    print("\n" + "=" * 70)
    print("CLASSIFICATION BASELINES")
    print("=" * 70)

    for target in CLASSIFICATION_TARGETS:

        if target not in train.columns:

            print(
                f"\nSkipping {target} "
                "(column not found)."
            )

            continue

        print(
            f"\nTarget: {target}"
        )

        train_target = train[
            train[target].notna()
        ][target]

        validation_target = validation[
            validation[target].notna()
        ][target]

        test_target = test[
            test[target].notna()
        ][target]

        if len(train_target) == 0:

            print(
                "No training values available."
            )

            continue

        # ----------------------------------------------------
        # Find majority class
        # ----------------------------------------------------

        majority_class = (
            train_target
            .value_counts()
            .index[0]
        )

        validation_prediction = np.full(
            len(validation_target),
            majority_class,
            dtype=object
        )

        test_prediction = np.full(
            len(test_target),
            majority_class,
            dtype=object
        )

        validation_metrics = classification_metrics(
            validation_target,
            validation_prediction
        )

        test_metrics = classification_metrics(
            test_target,
            test_prediction
        )

        results.append({
            "target": target,
            "task": "classification",
            "baseline": "training_majority_class",
            "validation_mae": np.nan,
            "validation_rmse": np.nan,
            "validation_r2": np.nan,
            "test_mae": np.nan,
            "test_rmse": np.nan,
            "test_r2": np.nan,
            "validation_accuracy": validation_metrics["accuracy"],
            "validation_macro_f1": validation_metrics["macro_f1"],
            "test_accuracy": test_metrics["accuracy"],
            "test_macro_f1": test_metrics["macro_f1"],
            "training_reference_value": majority_class
        })

        print(
            f"Majority class: "
            f"{majority_class}"
        )

        print(
            f"Validation accuracy: "
            f"{validation_metrics['accuracy']:.4f}"
        )

        print(
            f"Validation macro F1: "
            f"{validation_metrics['macro_f1']:.4f}"
        )

        print(
            f"Test accuracy: "
            f"{test_metrics['accuracy']:.4f}"
        )

        print(
            f"Test macro F1: "
            f"{test_metrics['macro_f1']:.4f}"
        )

    # --------------------------------------------------------
    # 5. Save results
    # --------------------------------------------------------

    print(
        "\n[3] Saving baseline results..."
    )

    results_df = pd.DataFrame(
        results
    )

    results_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # --------------------------------------------------------
    # 6. Final summary
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("STATISTICAL BASELINES COMPLETE")
    print("=" * 70)

    print(
        f"Baseline experiments: "
        f"{len(results_df)}"
    )

    print(
        f"Results saved to:"
    )

    print(OUTPUT_FILE)

    print(
        "\nThese baselines are benchmarks."
    )

    print(
        "The upcoming ML models must be "
        "compared against them."
    )

    print(
        "\nNext step:"
    )

    print(
        "Train machine-learning prediction models."
    )


if __name__ == "__main__":
    main()