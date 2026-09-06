import pandas as pd

# Load project data
data = pd.read_csv("data/projects.csv")

# Calculate how far each project is behind schedule
data["progress_gap"] = data["planned_progress"] - data["actual_progress"]

# Give a simple risk level
def get_risk(gap):
    if gap >= 15:
        return "HIGH"
    elif gap >= 5:
        return "MEDIUM"
    else:
        return "LOW"

data["risk_level"] = data["progress_gap"].apply(get_risk)

# Show the result
print(data[[
    "project_id",
    "project_name",
    "planned_progress",
    "actual_progress",
    "progress_gap",
    "risk_level"
]])