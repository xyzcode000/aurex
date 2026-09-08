import pandas as pd

# Load project data
data = pd.read_csv("data/projects.csv")


# ==========================================
# 1. CALCULATE PROJECT DEVIATIONS
# ==========================================

# Difference between planned and actual progress
data["progress_gap"] = (
    data["planned_progress"] - data["actual_progress"]
)


# Calculate cost overrun percentage
data["cost_overrun_pct"] = (
    (data["revised_cost"] - data["approved_cost"])
    / data["approved_cost"]
) * 100


# ==========================================
# 2. DETECT ANOMALIES
# ==========================================

def detect_anomaly(row):

    # Large progress delay
    if row["progress_gap"] >= 20:
        return "ANOMALY"

    # High cost overrun
    elif row["cost_overrun_pct"] >= 20:
        return "ANOMALY"

    else:
        return "NORMAL"


# Apply anomaly detection
data["anomaly_status"] = data.apply(
    detect_anomaly,
    axis=1
)


# ==========================================
# 3. SHOW RESULTS
# ==========================================

print("\n========== ANOMALY DETECTION ==========\n")

print(
    data[
        [
            "project_id",
            "project_name",
            "planned_progress",
            "actual_progress",
            "progress_gap",
            "approved_cost",
            "revised_cost",
            "cost_overrun_pct",
            "anomaly_status"
        ]
    ]
)