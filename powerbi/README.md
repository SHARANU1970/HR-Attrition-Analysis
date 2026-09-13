# Power BI Dashboard

## Data Source
Import `../data/hr_attrition_clean.csv` into Power BI Desktop.

## Recommended Dashboard Pages

### Page 1 — HR Attrition Overview
- Total Employees
- Attrition Count
- Attrition Rate %
- Average Monthly Income
- Employees by Department
- Attrition Rate by Department
- Attrition by Salary Band
- Attrition by Overtime

### Page 2 — Attrition Drivers
- Attrition by Job Satisfaction
- Attrition by Work-Life Balance
- Attrition by Business Travel
- Attrition by Tenure
- Attrition by Distance From Home

### Suggested DAX

```DAX
Total Employees = DISTINCTCOUNT(hr_attrition_clean[Employee_ID])

Attrition Count =
CALCULATE(
    [Total Employees],
    hr_attrition_clean[Attrition] = "Yes"
)

Attrition Rate % =
DIVIDE([Attrition Count], [Total Employees])

Average Monthly Income =
AVERAGE(hr_attrition_clean[Monthly_Income])
```

## Note

The PNG files are Power BI-style portfolio dashboard previews. They are not exports from a genuine `.pbix` file. Create the actual `.pbix` in Power BI Desktop if you want to include a Power BI project file.
