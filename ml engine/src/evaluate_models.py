import pandas as pd
import numpy as np

from pathlib import Path

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# ============================================================
# AUREX 2.0
# MODEL EVALUATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_DIR = (
    PROJECT_ROOT
    / "output"
    / "models"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "output"
)

BASELINE_FILE = (
    OUTPUT_DIR
    / "baseline_results.csv"
)

EVALUATION_FILE = (
    OUTPUT_DIR
    / "model_evaluation_results.csv"
)


# ============================================================
# MODEL DEFINITIONS
# ============================================================

REGRESSION_MODELS = {
    "cost_overrun_model": "Cost Overrun",
    "time_overrun_model": "Time / Delay"
}

CLASSIFICATION_MODELS = {
    "project_risk_model": "Project Risk"
}


# ============================================================
# REGRESSION EVALUATION
# ============================================================

def evaluate_regression(
    model_name,
    display_name
):

    print("\n" + "=" * 70)
    print(
        f"EVALUATING: {display_name}"
    )
    print("=" * 70)

    validation_file = (
        MODEL_DIR
        / f"{model_name}_validation_predictions.csv"
    )

    test_file = (
        MODEL_DIR
        / f"{model_name}_test_predictions.csv"
    )

    if not validation_file.exists():

        print(
            f"WARNING: Validation file not found:"
        )

        print(validation_file)

        return []

    if not test_file.exists():

        print(
            f"WARNING: Test file not found:"
        )

        print(test_file)

        return []

    validation = pd.read_csv(
        validation_file
    )

    test = pd.read_csv(
        test_file
    )

    results = []

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    actual_validation = (
        validation["actual"]
    )

    prediction_validation = (
        validation["prediction"]
    )

    validation_mae = (
        mean_absolute_error(
            actual_validation,
            prediction_validation
        )
    )

    validation_rmse = np.sqrt(
        mean_squared_error(
            actual_validation,
            prediction_validation
        )
    )

    validation_r2 = (
        r2_score(
            actual_validation,
            prediction_validation
        )
    )

    # --------------------------------------------------------
    # Test
    # --------------------------------------------------------

    actual_test = (
        test["actual"]
    )

    prediction_test = (
        test["prediction"]
    )

    test_mae = (
        mean_absolute_error(
            actual_test,
            prediction_test
        )
    )

    test_rmse = np.sqrt(
        mean_squared_error(
            actual_test,
            prediction_test
        )
    )

    test_r2 = (
        r2_score(
            actual_test,
            prediction_test
        )
    )

    # --------------------------------------------------------
    # Print
    # --------------------------------------------------------

    print("\nValidation Results")

    print(
        f"MAE  : {validation_mae:.4f}"
    )

    print(
        f"RMSE : {validation_rmse:.4f}"
    )

    print(
        f"R²   : {validation_r2:.4f}"
    )

    print("\nTest Results")

    print(
        f"MAE  : {test_mae:.4f}"
    )

    print(
        f"RMSE : {test_rmse:.4f}"
    )

    print(
        f"R²   : {test_r2:.4f}"
    )

    results.append({
        "model": model_name,
        "task": "regression",
        "target": display_name,

        "validation_mae":
            validation_mae,

        "validation_rmse":
            validation_rmse,

        "validation_r2":
            validation_r2,

        "test_mae":
            test_mae,

        "test_rmse":
            test_rmse,

        "test_r2":
            test_r2,

        "validation_accuracy":
            np.nan,

        "validation_precision":
            np.nan,

        "validation_recall":
            np.nan,

        "validation_f1":
            np.nan,

        "test_accuracy":
            np.nan,

        "test_precision":
            np.nan,

        "test_recall":
            np.nan,

        "test_f1":
            np.nan
    })

    return results


# ============================================================
# CLASSIFICATION EVALUATION
# ============================================================

def evaluate_classification(
    model_name,
    display_name
):

    print("\n" + "=" * 70)
    print(
        f"EVALUATING: {display_name}"
    )
    print("=" * 70)

    validation_file = (
        MODEL_DIR
        / f"{model_name}_validation_predictions.csv"
    )

    test_file = (
        MODEL_DIR
        / f"{model_name}_test_predictions.csv"
    )

    if not validation_file.exists():

        print(
            "WARNING: Validation prediction file not found."
        )

        return []

    if not test_file.exists():

        print(
            "WARNING: Test prediction file not found."
        )

        return []

    validation = pd.read_csv(
        validation_file
    )

    test = pd.read_csv(
        test_file
    )

    results = []

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    actual_validation = (
        validation["actual"]
        .astype(str)
    )

    prediction_validation = (
        validation["prediction"]
        .astype(str)
    )

    validation_accuracy = (
        accuracy_score(
            actual_validation,
            prediction_validation
        )
    )

    validation_precision = (
        precision_score(
            actual_validation,
            prediction_validation,
            average="macro",
            zero_division=0
        )
    )

    validation_recall = (
        recall_score(
            actual_validation,
            prediction_validation,
            average="macro",
            zero_division=0
        )
    )

    validation_f1 = (
        f1_score(
            actual_validation,
            prediction_validation,
            average="macro",
            zero_division=0
        )
    )

    # --------------------------------------------------------
    # Test
    # --------------------------------------------------------

    actual_test = (
        test["actual"]
        .astype(str)
    )

    prediction_test = (
        test["prediction"]
        .astype(str)
    )

    test_accuracy = (
        accuracy_score(
            actual_test,
            prediction_test
        )
    )

    test_precision = (
        precision_score(
            actual_test,
            prediction_test,
            average="macro",
            zero_division=0
        )
    )

    test_recall = (
        recall_score(
            actual_test,
            prediction_test,
            average="macro",
            zero_division=0
        )
    )

    test_f1 = (
        f1_score(
            actual_test,
            prediction_test,
            average="macro",
            zero_division=0
        )
    )

    # --------------------------------------------------------
    # Print
    # --------------------------------------------------------

    print("\nValidation Results")

    print(
        f"Accuracy  : {validation_accuracy:.4f}"
    )

    print(
        f"Precision : {validation_precision:.4f}"
    )

    print(
        f"Recall    : {validation_recall:.4f}"
    )

    print(
        f"Macro F1  : {validation_f1:.4f}"
    )

    print("\nTest Results")

    print(
        f"Accuracy  : {test_accuracy:.4f}"
    )

    print(
        f"Precision : {test_precision:.4f}"
    )

    print(
        f"Recall    : {test_recall:.4f}"
    )

    print(
        f"Macro F1  : {test_f1:.4f}"
    )

    # --------------------------------------------------------
    # Confusion Matrix
    # --------------------------------------------------------

    labels = sorted(
        actual_test.unique()
    )

    matrix = confusion_matrix(
        actual_test,
        prediction_test,
        labels=labels
    )

    print("\nTest Confusion Matrix")

    print(
        "Classes:"
    )

    print(labels)

    print(matrix)

    results.append({
        "model": model_name,
        "task": "classification",
        "target": display_name,

        "validation_mae":
            np.nan,

        "validation_rmse":
            np.nan,

        "validation_r2":
            np.nan,

        "test_mae":
            np.nan,

        "test_rmse":
            np.nan,

        "test_r2":
            np.nan,

        "validation_accuracy":
            validation_accuracy,

        "validation_precision":
            validation_precision,

        "validation_recall":
            validation_recall,

        "validation_f1":
            validation_f1,

        "test_accuracy":
            test_accuracy,

        "test_precision":
            test_precision,

        "test_recall":
            test_recall,

        "test_f1":
            test_f1
    })

    return results


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("AUREX 2.0 - MODEL EVALUATION")
    print("=" * 70)

    all_results = []

    # --------------------------------------------------------
    # Regression models
    # --------------------------------------------------------

    for model_name, display_name in (
        REGRESSION_MODELS.items()
    ):

        results = evaluate_regression(
            model_name,
            display_name
        )

        all_results.extend(
            results
        )

    # --------------------------------------------------------
    # Classification model
    # --------------------------------------------------------

    for model_name, display_name in (
        CLASSIFICATION_MODELS.items()
    ):

        results = evaluate_classification(
            model_name,
            display_name
        )

        all_results.extend(
            results
        )

    # --------------------------------------------------------
    # Save evaluation results
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("SAVING EVALUATION RESULTS")
    print("=" * 70)

    evaluation_df = pd.DataFrame(
        all_results
    )

    evaluation_df.to_csv(
        EVALUATION_FILE,
        index=False
    )

    print(
        f"Saved to:"
    )

    print(EVALUATION_FILE)

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("MODEL EVALUATION COMPLETE")
    print("=" * 70)

    print(
        f"Models evaluated: "
        f"{len(evaluation_df)}"
    )

    if not evaluation_df.empty:

        print(
            "\nEvaluation Summary:"
        )

        print(
            evaluation_df[
                [
                    "model",
                    "task",
                    "target",
                    "test_mae",
                    "test_rmse",
                    "test_r2",
                    "test_accuracy",
                    "test_f1"
                ]
            ].to_string(
                index=False
            )
        )

    print(
        "\nNext step:"
    )

    print(
        "Compare ML performance with statistical baselines."
    )


if __name__ == "__main__":
    main()