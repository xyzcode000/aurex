import pandas as pd

# Load project data
data = pd.read_csv("data/projects.csv")


# ==========================================
# 1. PROJECT PROGRESS ANALYSIS
# ==========================================

data["progress_gap"] = (
    data["planned_progress"] - data["actual_progress"]
)


# ==========================================
# 2. COST ANALYSIS
# ==========================================

data["cost_overrun_pct"] = (
    (data["revised_cost"] - data["approved_cost"])
    / data["approved_cost"]
) * 100


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


# ==========================================
# 4. SHOW ANALYSIS
# ==========================================

print("\n========== PROJECT RISK ANALYSIS ==========\n")

print(
    data[
        [
            "project_id",
            "project_name",
            "progress_gap",
            "cost_overrun_pct",
            "spending_pct",
            "spending_vs_progress"
        ]
    ].to_string(index=False)
)