import pandas as pd

# Load our project data
data = pd.read_csv("data/projects.csv")

# Show the data
print(data)

# Show how many projects we have
print("Number of projects:", len(data))