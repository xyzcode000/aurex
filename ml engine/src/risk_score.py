import pandas as pd
import os


# ==========================================
# AUREX PROJECT RISK ENGINE
# ==========================================

# Load project data
data = pd.read_csv("data/projects.csv")


# ==========================================
# 1. PROGRESS ANALYSIS
# ==========================================

data["progress_gap"] = (
    data["planned_progress"]
    - data["actual_progress"]
)


# Progress risk: maximum 40 points
progress_risk = (
    data["progress_gap"] / 30 * 40
).clip(0, 40)


# ==========================================
# 2. COST ANALYSIS
# ==========================================

data["cost_overrun_pct"] = (
    (
        data["revised_cost"]
        - data["approved_cost"]
    )
    / data["approved_cost"]
) * 100


# Cost risk: maximum 30 points
cost_risk = (
    data["cost_overrun_pct"] / 20 * 30
).clip(0, 30)


# ==========================================
# 3. SPENDING ANALYSIS
# ==========================================

data["spending_pct"] = (
    data["actual_expenditure"]
    / data["revised_cost"]
) * 100


data["spending_vs_progress"] = (
    data["spending_pct"]
    - data["actual_progress"]
)


# Spending risk: maximum 30 points
spending_risk = (
    data["spending_vs_progress"] / 20 * 30
).clip(0, 30)


# ==========================================
# 4. FINAL RISK SCORE
# ==========================================

data["risk_score"] = (
    progress_risk
    + cost_risk
    + spending_risk
).round(2)


# ==========================================
# 5. RISK LEVEL
# ==========================================

def get_risk_level(score):

    if score >= 70:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    else:
        return "LOW"


data["risk_level"] = data["risk_score"].apply(
    get_risk_level
)


# ==========================================
# 6. ANOMALY DETECTION
# ==========================================

def get_anomaly_status(row):

    if row["progress_gap"] >= 20:
        return "ANOMALY"

    elif row["cost_overrun_pct"] >= 20:
        return "ANOMALY"

    elif row["spending_vs_progress"] >= 20:
        return "ANOMALY"

    else:
        return "NORMAL"


data["anomaly_status"] = data.apply(
    get_anomaly_status,
    axis=1
)


# ==========================================
# 7. RISK REASONS
# ==========================================

def get_risk_reasons(row):

    reasons = []

    if row["progress_gap"] >= 15:
        reasons.append(
            "Project is behind planned progress"
        )

    if row["cost_overrun_pct"] >= 10:
        reasons.append(
            "Project has significant cost overrun"
        )

    if row["spending_vs_progress"] >= 10:
        reasons.append(
            "Spending is high compared with physical progress"
        )

    if not reasons:
        reasons.append(
            "No major risk indicator detected"
        )

    return "; ".join(reasons)


data["risk_reasons"] = data.apply(
    get_risk_reasons,
    axis=1
)


# ==========================================
# 8. DISPLAY RESULTS
# ==========================================

print("\n")
print("==========================================")
print("        AUREX PROJECT RISK ENGINE")
print("==========================================")

for _, row in data.iterrows():

    print("\n------------------------------------------")

    print("Project ID:", row["project_id"])
    print("Project Name:", row["project_name"])
    print("Risk Score:", row["risk_score"])
    print("Risk Level:", row["risk_level"])
    print("Anomaly Status:", row["anomaly_status"])
    print("Risk Reasons:", row["risk_reasons"])

print("\n------------------------------------------")


# ==========================================
# 9. SAVE RESULTS
# ==========================================

# Create output folder automatically
os.makedirs("output", exist_ok=True)


# Select important columns
results = data[
    [
        "project_id",
        "project_name",
        "progress_gap",
        "cost_overrun_pct",
        "spending_pct",
        "spending_vs_progress",
        "risk_score",
        "risk_level",
        "anomaly_status",
        "risk_reasons"
    ]
]


# Save CSV
results.to_csv(
    "output/risk_results.csv",
    index=False
)


# Save JSON for future FastAPI backend
results.to_json(
    "output/risk_results.json",
    orient="records",
    indent=4
)


print("\n==========================================")
print("Risk results saved successfully!")
print("CSV  : output/risk_results.csv")
print("JSON : output/risk_results.json")
print("==========================================")