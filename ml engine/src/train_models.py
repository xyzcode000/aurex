import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier


# ============================================================
# AUREX 2.0
# MACHINE LEARNING MODEL TRAINING
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SPLIT_DIR = (
    PROJECT_ROOT
    / "data"
    / "splits"
)

MODEL_DIR = (
    PROJECT_ROOT
    / "output"
    / "models"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# TARGETS
# ============================================================

COST_TARGET = (
    "target_future_cost_overrun_percent_vs_original"
)

TIME_TARGET = (
    "target_future_delay_days"
)

RISK_TARGET = (
    "target_future_risk_level"
)


# ============================================================
# COLUMNS THAT MUST NOT BE USED AS FEATURES
# ============================================================

EXCLUDED_COLUMNS = {
    "project_id",
    "project_name",
    "observation_date",
    "split",

    # Known future information
    "actual_end_date",

    # Targets
    "target_future_cost_overrun_percent_vs_original",
    "target_future_cost_overrun_percent_vs_current",
    "target_cost_overrun_flag",
    "target_future_delay_days",
    "target_future_time_overrun_percent",
    "target_time_overrun_flag",
    "target_future_risk_score",
    "target_future_risk_level",
    "target_early_warning_flag_90d",

    # Outcome information
    "outcome_after_cutoff",
}


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    print("\n[1] Loading project-aware datasets...")

    train_file = SPLIT_DIR / "train.csv"
    validation_file = SPLIT_DIR / "validation.csv"
    test_file = SPLIT_DIR / "test.csv"

    if not train_file.exists():

        raise FileNotFoundError(
            "train.csv not found. "
            "Run project_split.py first."
        )

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

    return train, validation, test


# ============================================================
# BUILD FEATURES
# ============================================================

def get_feature_columns(df, target):

    excluded = set(
        EXCLUDED_COLUMNS
    )

    excluded.add(target)

    feature_columns = []

    for column in df.columns:

        if column in excluded:
            continue

        # Never use target-like columns
        if column.startswith("target_"):
            continue

        feature_columns.append(
            column
        )

    return feature_columns


# ============================================================
# BUILD PREPROCESSOR
# ============================================================

def build_preprocessor(
    X
):

    numeric_columns = (
        X.select_dtypes(
            include=["number"]
        )
        .columns
        .tolist()
    )

    categorical_columns = (
        X.select_dtypes(
            include=["object", "category"]
        )
        .columns
        .tolist()
    )

    print(
        f"Numeric features     : "
        f"{len(numeric_columns)}"
    )

    print(
        f"Categorical features : "
        f"{len(categorical_columns)}"
    )

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                )
            )
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ]
    )

    transformers = []

    if numeric_columns:

        transformers.append(
            (
                "numeric",
                numeric_pipeline,
                numeric_columns
            )
        )

    if categorical_columns:

        transformers.append(
            (
                "categorical",
                categorical_pipeline,
                categorical_columns
            )
        )

    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder="drop"
    )

    return preprocessor


# ============================================================
# TRAIN REGRESSION MODEL
# ============================================================

def train_regression_model(
    train,
    validation,
    test,
    target,
    model_name
):

    print("\n" + "=" * 70)

    print(
        f"TRAINING REGRESSION MODEL: "
        f"{model_name}"
    )

    print("=" * 70)

    # --------------------------------------------------------
    # Remove rows without target
    # --------------------------------------------------------

    train = train[
        train[target].notna()
    ].copy()

    validation = validation[
        validation[target].notna()
    ].copy()

    test = test[
        test[target].notna()
    ].copy()

    # --------------------------------------------------------
    # Features
    # --------------------------------------------------------

    feature_columns = get_feature_columns(
        train,
        target
    )

    X_train = train[
        feature_columns
    ]

    y_train = train[
        target
    ]

    X_validation = validation[
        feature_columns
    ]

    y_validation = validation[
        target
    ]

    X_test = test[
        feature_columns
    ]

    y_test = test[
        target
    ]

    print(
        f"Training rows : "
        f"{len(X_train):,}"
    )

    print(
        f"Features      : "
        f"{len(feature_columns)}"
    )

    # --------------------------------------------------------
    # Preprocessor
    # --------------------------------------------------------

    preprocessor = build_preprocessor(
        X_train
    )

    # --------------------------------------------------------
    # Random Forest
    # --------------------------------------------------------

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=12,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=-1
    )

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                model
            )
        ]
    )

    # --------------------------------------------------------
    # Train
    # --------------------------------------------------------

    print(
        "\nTraining model..."
    )

    pipeline.fit(
        X_train,
        y_train
    )

    print(
        "Training complete."
    )

    # --------------------------------------------------------
    # Predictions
    # --------------------------------------------------------

    validation_prediction = (
        pipeline.predict(
            X_validation
        )
    )

    test_prediction = (
        pipeline.predict(
            X_test
        )
    )

    # --------------------------------------------------------
    # Save predictions
    # --------------------------------------------------------

    validation_output = validation[
        [
            "project_id",
            "observation_date"
        ]
    ].copy()

    validation_output[
        "actual"
    ] = y_validation.values

    validation_output[
        "prediction"
    ] = validation_prediction

    validation_output[
        "model"
    ] = model_name

    test_output = test[
        [
            "project_id",
            "observation_date"
        ]
    ].copy()

    test_output[
        "actual"
    ] = y_test.values

    test_output[
        "prediction"
    ] = test_prediction

    test_output[
        "model"
    ] = model_name

    validation_output.to_csv(
        MODEL_DIR
        / f"{model_name}_validation_predictions.csv",
        index=False
    )

    test_output.to_csv(
        MODEL_DIR
        / f"{model_name}_test_predictions.csv",
        index=False
    )

    # --------------------------------------------------------
    # Save model
    # --------------------------------------------------------

    model_file = (
        MODEL_DIR
        / f"{model_name}.joblib"
    )

    joblib.dump(
        pipeline,
        model_file
    )

    print(
        f"Model saved:"
    )

    print(model_file)

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print(
        f"Validation predictions saved."
    )

    print(
        f"Test predictions saved."
    )

    return pipeline


# ============================================================
# TRAIN CLASSIFICATION MODEL
# ============================================================

def train_classification_model(
    train,
    validation,
    test,
    target,
    model_name
):

    print("\n" + "=" * 70)

    print(
        f"TRAINING CLASSIFICATION MODEL: "
        f"{model_name}"
    )

    print("=" * 70)

    # --------------------------------------------------------
    # Remove missing target rows
    # --------------------------------------------------------

    train = train[
        train[target].notna()
    ].copy()

    validation = validation[
        validation[target].notna()
    ].copy()

    test = test[
        test[target].notna()
    ].copy()

    # --------------------------------------------------------
    # Features
    # --------------------------------------------------------

    feature_columns = get_feature_columns(
        train,
        target
    )

    X_train = train[
        feature_columns
    ]

    y_train = train[
        target
    ].astype(str)

    X_validation = validation[
        feature_columns
    ]

    y_validation = validation[
        target
    ].astype(str)

    X_test = test[
        feature_columns
    ]

    y_test = test[
        target
    ].astype(str)

    print(
        f"Training rows : "
        f"{len(X_train):,}"
    )

    print(
        f"Features      : "
        f"{len(feature_columns)}"
    )

    print(
        "\nTraining classes:"
    )

    print(
        y_train.value_counts()
    )

    # --------------------------------------------------------
    # Preprocessor
    # --------------------------------------------------------

    preprocessor = build_preprocessor(
        X_train
    )

    # --------------------------------------------------------
    # Random Forest Classifier
    # --------------------------------------------------------

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                model
            )
        ]
    )

    # --------------------------------------------------------
    # Train
    # --------------------------------------------------------

    print(
        "\nTraining model..."
    )

    pipeline.fit(
        X_train,
        y_train
    )

    print(
        "Training complete."
    )

    # --------------------------------------------------------
    # Predictions
    # --------------------------------------------------------

    validation_prediction = (
        pipeline.predict(
            X_validation
        )
    )

    test_prediction = (
        pipeline.predict(
            X_test
        )
    )

    # --------------------------------------------------------
    # Prediction probabilities
    # --------------------------------------------------------

    validation_probability = (
        pipeline.predict_proba(
            X_validation
        ).max(axis=1)
    )

    test_probability = (
        pipeline.predict_proba(
            X_test
        ).max(axis=1)
    )

    # --------------------------------------------------------
    # Save validation predictions
    # --------------------------------------------------------

    validation_output = validation[
        [
            "project_id",
            "observation_date"
        ]
    ].copy()

    validation_output[
        "actual"
    ] = y_validation.values

    validation_output[
        "prediction"
    ] = validation_prediction

    validation_output[
        "confidence"
    ] = validation_probability

    validation_output[
        "model"
    ] = model_name

    # --------------------------------------------------------
    # Save test predictions
    # --------------------------------------------------------

    test_output = test[
        [
            "project_id",
            "observation_date"
        ]
    ].copy()

    test_output[
        "actual"
    ] = y_test.values

    test_output[
        "prediction"
    ] = test_prediction

    test_output[
        "confidence"
    ] = test_probability

    test_output[
        "model"
    ] = model_name

    validation_output.to_csv(
        MODEL_DIR
        / f"{model_name}_validation_predictions.csv",
        index=False
    )

    test_output.to_csv(
        MODEL_DIR
        / f"{model_name}_test_predictions.csv",
        index=False
    )

    # --------------------------------------------------------
    # Save model
    # --------------------------------------------------------

    model_file = (
        MODEL_DIR
        / f"{model_name}.joblib"
    )

    joblib.dump(
        pipeline,
        model_file
    )

    print(
        f"Model saved:"
    )

    print(model_file)

    print(
        "Validation predictions saved."
    )

    print(
        "Test predictions saved."
    )

    return pipeline


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("AUREX 2.0 - ML MODEL TRAINING")
    print("=" * 70)

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    train, validation, test = (
        load_data()
    )

    # --------------------------------------------------------
    # Cost model
    # --------------------------------------------------------

    if COST_TARGET in train.columns:

        train_regression_model(
            train,
            validation,
            test,
            COST_TARGET,
            "cost_overrun_model"
        )

    else:

        print(
            f"\nWARNING: {COST_TARGET} "
            "not found."
        )

    # --------------------------------------------------------
    # Time model
    # --------------------------------------------------------

    if TIME_TARGET in train.columns:

        train_regression_model(
            train,
            validation,
            test,
            TIME_TARGET,
            "time_overrun_model"
        )

    else:

        print(
            f"\nWARNING: {TIME_TARGET} "
            "not found."
        )

    # --------------------------------------------------------
    # Risk model
    # --------------------------------------------------------

    if RISK_TARGET in train.columns:

        train_classification_model(
            train,
            validation,
            test,
            RISK_TARGET,
            "project_risk_model"
        )

    else:

        print(
            f"\nWARNING: {RISK_TARGET} "
            "not found."
        )

    # --------------------------------------------------------
    # Complete
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("ML MODEL TRAINING COMPLETE")
    print("=" * 70)

    print(
        "\nModels are stored in:"
    )

    print(MODEL_DIR)

    print(
        "\nModels trained:"
    )

    print(
        "1. Cost overrun prediction"
    )

    print(
        "2. Time/delay prediction"
    )

    print(
        "3. Project risk classification"
    )

    print(
        "\nNext step:"
    )

    print(
        "Evaluate the ML models against "
        "the statistical baselines."
    )


if __name__ == "__main__":
    main()