"""
HR Attrition Analysis
Portfolio project using Python, Pandas, NumPy and Matplotlib.

Run from the project root:
    python python/hr_attrition_analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA_PATH = "../data/hr_attrition_clean.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("HR ATTRITION ANALYSIS")
print("=" * 60)

print(f"Records: {len(df):,}")
print(f"Variables: {df.shape[1]}")
print("\nMissing values by column:")
print(df.isna().sum().sort_values(ascending=False).head(10))

# Attrition overview
attrition_summary = (
    df["Attrition"]
    .value_counts()
    .rename_axis("Attrition")
    .reset_index(name="Employees")
)
attrition_summary["Percentage"] = (
    attrition_summary["Employees"] / len(df) * 100
).round(1)

print("\nAttrition summary:")
print(attrition_summary)

# Department analysis
department_kpi = (
    df.groupby("Department")
      .agg(
          Employees=("Employee_ID", "count"),
          Attrition_Rate=("Attrition", lambda x: (x == "Yes").mean() * 100),
          Avg_Income=("Monthly_Income", "mean"),
          Avg_Satisfaction=("Job_Satisfaction", "mean"),
          Overtime_Rate=("Overtime", lambda x: (x == "Yes").mean() * 100),
      )
      .reset_index()
)
department_kpi["Attrition_Rate"] = department_kpi["Attrition_Rate"].round(1)
department_kpi["Avg_Income"] = department_kpi["Avg_Income"].round(0)
department_kpi["Avg_Satisfaction"] = department_kpi["Avg_Satisfaction"].round(2)
department_kpi["Overtime_Rate"] = department_kpi["Overtime_Rate"].round(1)

print("\nDepartment KPIs:")
print(department_kpi.sort_values("Attrition_Rate", ascending=False))

# Salary-band analysis
salary_kpi = (
    df.groupby("Salary_Band", observed=True)
      .agg(
          Employees=("Employee_ID", "count"),
          Attrition_Rate=("Attrition", lambda x: (x == "Yes").mean() * 100),
          Avg_Income=("Monthly_Income", "mean"),
      )
      .reset_index()
)
salary_kpi["Attrition_Rate"] = salary_kpi["Attrition_Rate"].round(1)

print("\nSalary-band analysis:")
print(salary_kpi)

# Potential driver analysis
for col in ["Overtime", "Business_Travel", "Job_Satisfaction", "Work_Life_Balance"]:
    print(f"\nAttrition by {col}:")
    result = (
        df.groupby(col, dropna=False)["Attrition"]
          .apply(lambda x: (x == "Yes").mean() * 100)
          .round(1)
          .sort_values(ascending=False)
    )
    print(result)

# Simple feature engineering
df["Tenure_Band"] = pd.cut(
    df["Years_At_Company"],
    bins=[-1, 2, 5, 10, np.inf],
    labels=["0-2 Years", "3-5 Years", "6-10 Years", "10+ Years"],
)

print("\nAttrition by tenure band:")
print(
    df.groupby("Tenure_Band", observed=True)["Attrition"]
      .apply(lambda x: (x == "Yes").mean() * 100)
      .round(1)
)

# Charts
dept_plot = department_kpi.sort_values("Attrition_Rate", ascending=True)
plt.figure(figsize=(9, 5))
plt.barh(dept_plot["Department"], dept_plot["Attrition_Rate"])
plt.title("Attrition Rate by Department")
plt.xlabel("Attrition Rate (%)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
overtime = df.groupby("Overtime")["Attrition"].apply(lambda x: (x == "Yes").mean() * 100)
plt.bar(overtime.index, overtime.values)
plt.title("Attrition Rate by Overtime")
plt.ylabel("Attrition Rate (%)")
plt.tight_layout()
plt.show()

print("\nAnalysis complete.")
