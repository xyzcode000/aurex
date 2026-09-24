import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# AUREX 2.0
# CORRECTED PREDICTION + EARLY WARNING ENGINE
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "cleaned_master_project_snapshots.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "output"

MODEL_DIR = OUTPUT_DIR / "models"

PREDICTION_FILE = (
    OUTPUT_DIR / "aurex_predictions.csv"
)

WARNING_FILE = (
    OUTPUT_DIR / "early_warnings.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    print("Loading cleaned dataset...")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    print(
        f"Rows loaded: {len(df):,}"
    )

    print(
        f"Columns loaded: {len(df.columns)}"
    )

    return df


# ============================================================
# GET LATEST SNAPSHOT FOR EACH PROJECT
# ============================================================

def get_latest_projects(df):

    print("\nSelecting latest snapshot for each project...")

    df["observation_date"] = pd.to_datetime(
        df["observation_date"],
        errors="coerce"
    )

    latest = (
        df.sort_values(
            ["project_id", "observation_date"]
        )
        .groupby(
            "project_id",
            as_index=False
        )
        .tail(1)
        .copy()
    )

    latest = latest.drop_duplicates(
        subset=["project_id"]
    )

    latest = latest.reset_index(
        drop=True
    )

    print(
        f"Latest projects: {len(latest)}"
    )

    return latest


# ============================================================
# FIND PREDICTION COLUMN
# ============================================================

def find_prediction_column(df):

    possible_columns = [
        "prediction",
        "predicted",
        "predicted_value",
        "predicted_class",
        "prediction_value",
        "prediction_class"
    ]

    for column in possible_columns:

        if column in df.columns:
            return column

    return None


# ============================================================
# LOAD MODEL PREDICTIONS SAFELY
# ============================================================

def load_prediction_file(
    filename,
    output_name
):

    path = MODEL_DIR / filename

    if not path.exists():

        print(
            f"Not found: {filename}"
        )

        return None

    data = pd.read_csv(path)

    print(
        f"Loaded: {filename}"
    )

    if "project_id" not in data.columns:

        print(
            "Skipping: project_id not found."
        )

        return None

    prediction_column = (
        find_prediction_column(data)
    )

    if prediction_column is None:

        print(
            "Skipping: prediction column not found."
        )

        return None

    # --------------------------------------------------------
    # Keep ONLY one prediction per project.
    # This prevents merge explosions.
    # --------------------------------------------------------

    data = data[
        [
            "project_id",
            prediction_column
        ]
    ].copy()

    data = data.drop_duplicates(
        subset=["project_id"],
        keep="last"
    )

    data = data.rename(
        columns={
            prediction_column:
                output_name
        }
    )

    print(
        f"Unique project predictions: {len(data)}"
    )

    return data


# ============================================================
# BUILD PROJECT PREDICTION TABLE
# ============================================================

def build_prediction_table(latest):

    print("\nBuilding prediction table...")

    columns_to_keep = [
        "project_id",
        "project_name",
        "state",
        "sector",
        "agency",
        "observation_date",
        "original_cost_crore",
        "revised_cost_crore",
        "approved_duration_days",
        "planned_progress_percent",
        "actual_progress_percent",
        "actual_expenditure_crore"
    ]

    available = [
        c
        for c in columns_to_keep
        if c in latest.columns
    ]

    predictions = latest[
        available
    ].copy()

    return predictions


# ============================================================
# ADD PREDICTIONS
# ============================================================

def add_prediction(
    predictions,
    prediction_data
):

    if prediction_data is None:
        return predictions

    predictions = predictions.merge(
        prediction_data,
        on="project_id",
        how="left",
        validate="one_to_one"
    )

    return predictions


# ============================================================
# CREATE EARLY WARNINGS
# ============================================================

def create_early_warnings(predictions):

    print(
        "\nCreating early-warning signals..."
    )

    warnings = []

    for _, row in predictions.iterrows():

        project_id = row["project_id"]

        project_name = row.get(
            "project_name",
            ""
        )

        triggered = False

        # ----------------------------------------------------
        # COST
        # ----------------------------------------------------

        cost = row.get(
            "predicted_cost_overrun_percent",
            np.nan
        )

        if pd.notna(cost):

            if cost >= 20:

                warnings.append({
                    "project_id": project_id,
                    "project_name": project_name,
                    "warning_type": "COST_OVERRUN",
                    "severity": "HIGH",
                    "reason":
                        "Predicted cost overrun is at least 20%.",
                    "evidence":
                        f"Predicted cost overrun = {cost:.2f}%"
                })

                triggered = True

            elif cost >= 10:

                warnings.append({
                    "project_id": project_id,
                    "project_name": project_name,
                    "warning_type": "COST_OVERRUN",
                    "severity": "MEDIUM",
                    "reason":
                        "Predicted cost overrun is at least 10%.",
                    "evidence":
                        f"Predicted cost overrun = {cost:.2f}%"
                })

                triggered = True

        # ----------------------------------------------------
        # DELAY
        # ----------------------------------------------------

        delay = row.get(
            "predicted_delay_days",
            np.nan
        )

        if pd.notna(delay):

            if delay >= 180:

                warnings.append({
                    "project_id": project_id,
                    "project_name": project_name,
                    "warning_type": "SCHEDULE_DELAY",
                    "severity": "HIGH",
                    "reason":
                        "Predicted delay is at least 180 days.",
                    "evidence":
                        f"Predicted delay = {delay:.0f} days"
                })

                triggered = True

            elif delay >= 90:

                warnings.append({
                    "project_id": project_id,
                    "project_name": project_name,
                    "warning_type": "SCHEDULE_DELAY",
                    "severity": "MEDIUM",
                    "reason":
                        "Predicted delay is at least 90 days.",
                    "evidence":
                        f"Predicted delay = {delay:.0f} days"
                })

                triggered = True

        # ----------------------------------------------------
        # RISK
        # ----------------------------------------------------

        risk = row.get(
            "predicted_risk_level",
            np.nan
        )

        if pd.notna(risk):

            risk_text = str(risk).upper()

            if risk_text == "HIGH":

                warnings.append({
                    "project_id": project_id,
                    "project_name": project_name,
                    "warning_type": "PROJECT_RISK",
                    "severity": "HIGH",
                    "reason":
                        "Project risk was classified as HIGH.",
                    "evidence":
                        "Predicted risk level = HIGH"
                })

                triggered = True

            elif risk_text == "MEDIUM":

                warnings.append({
                    "project_id": project_id,
                    "project_name": project_name,
                    "warning_type": "PROJECT_RISK",
                    "severity": "MEDIUM",
                    "reason":
                        "Project risk was classified as MEDIUM.",
                    "evidence":
                        "Predicted risk level = MEDIUM"
                })

                triggered = True

        # ----------------------------------------------------
        # NO WARNING
        # ----------------------------------------------------

        if not triggered:

            warnings.append({
                "project_id": project_id,
                "project_name": project_name,
                "warning_type": "NONE",
                "severity": "LOW",
                "reason":
                    "No configured early-warning threshold was triggered.",
                "evidence":
                    "No current prediction crossed the configured thresholds."
            })

    return pd.DataFrame(warnings)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("AUREX 2.0 - PREDICTION + EARLY WARNING")
    print("=" * 70)

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    df = load_data()

    # --------------------------------------------------------
    # Latest snapshot
    # --------------------------------------------------------

    latest = get_latest_projects(df)

    # Safety check
    if len(latest) > 300:

        raise ValueError(
            "Unexpected project count. "
            "Prediction process stopped to prevent bad output."
        )

    # --------------------------------------------------------
    # Base prediction table
    # --------------------------------------------------------

    predictions = build_prediction_table(
        latest
    )

    # --------------------------------------------------------
    # Load test prediction artifacts
    # --------------------------------------------------------

    cost_predictions = load_prediction_file(
        "cost_overrun_model_test_predictions.csv",
        "predicted_cost_overrun_percent"
    )

    time_predictions = load_prediction_file(
        "time_overrun_model_test_predictions.csv",
        "predicted_delay_days"
    )

    risk_predictions = load_prediction_file(
        "project_risk_model_test_predictions.csv",
        "predicted_risk_level"
    )

    # --------------------------------------------------------
    # Merge safely
    # --------------------------------------------------------

    predictions = add_prediction(
        predictions,
        cost_predictions
    )

    predictions = add_prediction(
        predictions,
        time_predictions
    )

    predictions = add_prediction(
        predictions,
        risk_predictions
    )

    # Final safety check
    predictions = predictions.drop_duplicates(
        subset=["project_id"]
    )

    print(
        f"\nFinal projects processed: "
        f"{len(predictions)}"
    )

    # --------------------------------------------------------
    # Save predictions
    # --------------------------------------------------------

    predictions.to_csv(
        PREDICTION_FILE,
        index=False
    )

    print(
        f"\nPrediction file saved:\n"
        f"{PREDICTION_FILE}"
    )

    # --------------------------------------------------------
    # Early warnings
    # --------------------------------------------------------

    warnings = create_early_warnings(
        predictions
    )

    warnings.to_csv(
        WARNING_FILE,
        index=False
    )

    print(
        f"\nEarly-warning file saved:\n"
        f"{WARNING_FILE}"
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("PREDICTION + EARLY WARNING COMPLETE")
    print("=" * 70)

    print(
        f"Projects processed : {len(predictions)}"
    )

    print(
        f"Warning records    : {len(warnings)}"
    )

    print("\nWarning severity:")

    print(
        warnings["severity"]
        .value_counts()
        .to_string()
    )

    print(
        "\nNext step:"
    )

    print(
        "Build model explainability and contributing-factor outputs."
    )


if __name__ == "__main__":
    main()