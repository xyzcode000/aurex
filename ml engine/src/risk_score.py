
import pandas as pd

# Load project data
data = pd.read_csv("data/projects.csv")

# --------------------------------
# 1. PROGRESS RISK
# --------------------------------

data["progress_gap"] = (
    data["planned_progress"] - data["actual_progress"]
)

progress_risk = (data["progress_gap"] / 30 * 40).clip(0, 40)


# --------------------------------
# 2. COST RISK
# --------------------------------

data["cost_overrun_pct"] = (
    (data["revised_cost"] - data["approved_cost"])
    / data["approved_cost"]
) * 100

cost_risk = (data["cost_overrun_pct"] / 20 * 30).clip(0, 30)


# --------------------------------
# 3. SPENDING RISK
# --------------------------------

data["spending_pct"] = (
    data["actual_expenditure"] / data["revised_cost"]
) * 100

data["spending_vs_progress"] = (
    data["spending_pct"] - data["actual_progress"]
)

spending_risk = (
    data["spending_vs_progress"] / 20 * 30
).clip(0, 30)


# --------------------------------
# 4. FINAL RISK SCORE
# --------------------------------

data["risk_score"] = (
    progress_risk
    + cost_risk
    + spending_risk
).round(2)


# --------------------------------
# 5. RISK LEVEL
# --------------------------------

def get_risk_level(score):

    if score >= 70:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    else:
        return "LOW"


data["risk_level"] = data["risk_score"].apply(get_risk_level)


# --------------------------------
# 6. SHOW RESULT
# --------------------------------

print(
    data[
        [
            "project_id",
            "project_name",
            "progress_gap",
            "cost_overrun_pct",
            "spending_vs_progress",
            "risk_score",
            "risk_level"
        ]
    ]
)