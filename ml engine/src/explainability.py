import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# AUREX 2.0
# STEP 11 - EXPLAINABILITY
# SciPy / sklearn independent version
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

DATA_FILE = DATA_DIR / "cleaned_master_project_snapshots.csv"

PREDICTION_FILE = OUTPUT_DIR / "aurex_predictions.csv"

FEATURE_IMPORTANCE_FILE = (
    OUTPUT_DIR / "model_feature_importance.csv"
)

FACTORS_FILE = (
    OUTPUT_DIR / "project_contributing_factors.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    print("\n[1] Loading cleaned dataset...")

    if not DATA_FILE.exists():
        print(f"ERROR: Dataset not found:")
        print(DATA_FILE)
        return pd.DataFrame()

    df = pd.read_csv(DATA_FILE)

    print(f"Rows loaded: {len(df):,}")
    print(f"Columns loaded: {len(df.columns)}")

    return df


# ============================================================
# FIND USEFUL FEATURES
# ============================================================

def find_features(df):

    excluded_words = [
        "target_",
        "future_",
        "outcome_",
        "risk_level",
        "flag"
    ]

    numeric_features = []

    for column in df.columns:

        if column == "project_id":
            continue

        if any(word in column.lower() for word in excluded_words):
            continue

        if pd.api.types.is_numeric_dtype(df[column]):

            if df[column].nunique() > 1:
                numeric_features.append(column)

    return numeric_features


# ============================================================
# GLOBAL FEATURE IMPORTANCE
# ============================================================

def create_feature_importance(df, features):

    print("\n[2] Creating global feature importance...")

    target_candidates = [
        "target_future_risk_score",
        "target_future_cost_overrun_percent_vs_original",
        "target_future_time_overrun_percent"
    ]

    target = None

    for column in target_candidates:

        if column in df.columns:

            target = column
            break

    if target is None:

        print(
            "Risk target not found. "
            "Using available numeric target."
        )

        target_columns = [
            c for c in df.columns
            if c.startswith("target_")
            and pd.api.types.is_numeric_dtype(df[c])
        ]

        if target_columns:
            target = target_columns[0]

    if target is None:

        print("No numeric target available.")
        return pd.DataFrame()

    print(f"Reference target: {target}")

    results = []

    target_series = pd.to_numeric(
        df[target],
        errors="coerce"
    )

    for feature in features:

        feature_series = pd.to_numeric(
            df[feature],
            errors="coerce"
        )

        valid = (
            feature_series.notna()
            & target_series.notna()
        )

        if valid.sum() < 10:
            continue

        x = feature_series[valid]
        y = target_series[valid]

        if x.nunique() <= 1:
            continue

        correlation = x.corr(y)

        if pd.isna(correlation):
            correlation = 0.0

        results.append({
            "feature": feature,
            "association_with_target": round(
                float(correlation),
                6
            ),
            "absolute_importance": round(
                abs(float(correlation)),
                6
            )
        })

    result = pd.DataFrame(results)

    if result.empty:
        return result

    result = result.sort_values(
        "absolute_importance",
        ascending=False
    )

    result.insert(
        0,
        "rank",
        range(1, len(result) + 1)
    )

    result.to_csv(
        FEATURE_IMPORTANCE_FILE,
        index=False
    )

    print(
        f"Feature importance saved to:\n"
        f"{FEATURE_IMPORTANCE_FILE}"
    )

    print("\nTop contributing features:")

    print(
        result.head(10).to_string(
            index=False
        )
    )

    return result


# ============================================================
# PROJECT CONTRIBUTING FACTORS
# ============================================================

def create_project_factors(
    df,
    feature_importance
):

    print(
        "\n[3] Creating project-level "
        "contributing factors..."
    )

    if feature_importance.empty:

        print(
            "No feature importance available."
        )

        return pd.DataFrame()

    if "project_id" not in df.columns:

        print(
            "project_id column not found."
        )

        return pd.DataFrame()

    # Use top features only
    top_features = (
        feature_importance
        .head(10)["feature"]
        .tolist()
    )

    records = []

    for project_id, project_df in df.groupby(
        "project_id"
    ):

        factors = []

        for feature in top_features:

            if feature not in project_df.columns:
                continue

            values = pd.to_numeric(
                project_df[feature],
                errors="coerce"
            ).dropna()

            if values.empty:
                continue

            latest_value = values.iloc[-1]

            global_mean = pd.to_numeric(
                df[feature],
                errors="coerce"
            ).mean()

            global_std = pd.to_numeric(
                df[feature],
                errors="coerce"
            ).std()

            if pd.isna(global_std) or global_std == 0:
                continue

            z_score = (
                latest_value - global_mean
            ) / global_std

            if abs(z_score) >= 1:

                direction = (
                    "above normal"
                    if z_score > 0
                    else "below normal"
                )

                factors.append(
                    f"{feature}: "
                    f"{direction}"
                )

        records.append({
            "project_id": project_id,
            "contributing_factors":
                " | ".join(factors)
                if factors
                else "No strong contributing factor detected",
            "factor_count":
                len(factors)
        })

    result = pd.DataFrame(records)

    result.to_csv(
        FACTORS_FILE,
        index=False
    )

    print(
        f"Project factors saved to:\n"
        f"{FACTORS_FILE}"
    )

    print(
        f"Projects explained: "
        f"{len(result):,}"
    )

    return result


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("AUREX 2.0 - EXPLAINABILITY")
    print("=" * 70)

    df = load_data()

    if df.empty:
        return

    features = find_features(df)

    print(
        f"\nNumeric explanatory features: "
        f"{len(features)}"
    )

    feature_importance = create_feature_importance(
        df,
        features
    )

    create_project_factors(
        df,
        feature_importance
    )

    print("\n" + "=" * 70)
    print("EXPLAINABILITY COMPLETE")
    print("=" * 70)

    print("\nCreated:")

    print(
        "1. model_feature_importance.csv"
    )

    print(
        "2. project_contributing_factors.csv"
    )

    print(
        "\nNote: This version uses "
        "data-based feature association and "
        "project-level deviation evidence."
    )


if __name__ == "__main__":
    main()