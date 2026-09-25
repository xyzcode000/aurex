import pandas as pd
import json
from pathlib import Path


# ============================================================
# AUREX 2.0
# STEP 12 - ML OUTPUT CONTRACT
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "output"

PREDICTION_FILE = OUTPUT_DIR / "aurex_predictions.csv"
WARNING_FILE = OUTPUT_DIR / "early_warnings.csv"
FACTOR_FILE = OUTPUT_DIR / "project_contributing_factors.csv"

CONTRACT_JSON = OUTPUT_DIR / "aurex_ml_contract.json"
SAMPLE_JSON = OUTPUT_DIR / "aurex_sample_response.json"


# ============================================================
# LOAD FILE SAFELY
# ============================================================

def load_file(path):

    if not path.exists():

        print(f"File not found: {path}")
        return pd.DataFrame()

    return pd.read_csv(path)


# ============================================================
# BUILD CONTRACT
# ============================================================

def build_contract():

    contract = {

        "system": "AUREX 2.0",

        "purpose":
            "Predictive analytics, project risk and early warning",

        "data_status":
            "Synthetic demonstration dataset",

        "prediction_outputs": {

            "cost": {
                "field": "predicted_cost_overrun_percent",
                "type": "number",
                "unit": "percent"
            },

            "time": {
                "field": "predicted_delay_days",
                "type": "number",
                "unit": "days"
            },

            "risk": {
                "field": "predicted_risk_level",
                "type": "string",
                "allowed_values": [
                    "LOW",
                    "MEDIUM",
                    "HIGH"
                ]
            }
        },

        "early_warning": {

            "warning_type": {
                "type": "string"
            },

            "severity": {
                "type": "string",
                "allowed_values": [
                    "LOW",
                    "MEDIUM",
                    "HIGH"
                ]
            },

            "reason": {
                "type": "string"
            },

            "evidence": {
                "type": "string"
            }
        },

        "explainability": {

            "global": {
                "description":
                    "Model-level feature importance"
            },

            "project_level": {
                "description":
                    "Evidence-based contributing factors for each project"
            }
        },

        "prediction_horizon": {

            "cost": "Future project outcome",

            "time": "Future project completion / delay",

            "risk": "Future project risk"
        },

        "important_note":
            "Predictions are generated from synthetic data and must not be represented as predictions trained on real government project data."
    }

    return contract


# ============================================================
# BUILD SAMPLE RESPONSE
# ============================================================

def build_sample_response():

    predictions = load_file(
        PREDICTION_FILE
    )

    warnings = load_file(
        WARNING_FILE
    )

    factors = load_file(
        FACTOR_FILE
    )

    if predictions.empty:

        return {
            "project_id": None,
            "prediction": {},
            "early_warning": {},
            "explanation": {}
        }

    row = predictions.iloc[0]

    project_id = row.get(
        "project_id"
    )

    # --------------------------------------------------------
    # Warning
    # --------------------------------------------------------

    warning = {}

    if not warnings.empty:

        project_warnings = warnings[
            warnings["project_id"] == project_id
        ]

        if not project_warnings.empty:

            w = project_warnings.iloc[0]

            warning = {
                "warning_type":
                    w.get("warning_type"),

                "severity":
                    w.get("severity"),

                "reason":
                    w.get("reason"),

                "evidence":
                    w.get("evidence")
            }

    # --------------------------------------------------------
    # Factors
    # --------------------------------------------------------

    explanation = {}

    if not factors.empty:

        project_factors = factors[
            factors["project_id"] == project_id
        ]

        if not project_factors.empty:

            f = project_factors.iloc[0]

            explanation = {

                "contributing_factors":
                    f.get(
                        "contributing_factors"
                    ),

                "factor_count":
                    int(
                        f.get(
                            "factor_count",
                            0
                        )
                    )
            }

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    prediction = {

        "cost_overrun_percent":
            row.get(
                "predicted_cost_overrun_percent"
            ),

        "delay_days":
            row.get(
                "predicted_delay_days"
            ),

        "risk_level":
            row.get(
                "predicted_risk_level"
            )
    }

    return {

        "project_id":
            project_id,

        "prediction":
            prediction,

        "early_warning":
            warning,

        "explanation":
            explanation
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("AUREX 2.0 - ML OUTPUT CONTRACT")
    print("=" * 70)

    # --------------------------------------------------------
    # Contract
    # --------------------------------------------------------

    contract = build_contract()

    with open(
        CONTRACT_JSON,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            contract,
            file,
            indent=4
        )

    print(
        "\nContract saved:"
    )

    print(
        CONTRACT_JSON
    )

    # --------------------------------------------------------
    # Sample response
    # --------------------------------------------------------

    sample = build_sample_response()

    with open(
        SAMPLE_JSON,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            sample,
            file,
            indent=4,
            default=str
        )

    print(
        "\nSample response saved:"
    )

    print(
        SAMPLE_JSON
    )

    # --------------------------------------------------------
    # Final
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("ML OUTPUT CONTRACT COMPLETE")
    print("=" * 70)

    print("\nCreated:")

    print("1. aurex_ml_contract.json")
    print("2. aurex_sample_response.json")

    print("\nML layer is ready for backend integration.")


if __name__ == "__main__":
    main()