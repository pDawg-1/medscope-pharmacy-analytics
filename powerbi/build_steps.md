# MedScope Power BI Build Steps

Final Power BI file name:
`MedScope_Snowflake_Dashboard_final.pbix`

## Page 1: Executive Overview

Goal: executive-level snapshot of prescription volume, cost, doctors, patients, and most prescribed drug.

Visuals:
- Card: Total Prescriptions
- Card: Total Drug Cost
- Card: Average Prescription Cost
- Card: Total Patients
- Card: Total Doctors
- Card: Most Prescribed Drug
- Column chart: Monthly Prescription Trend
  - Axis: `VW_MONTHLY_PRESCRIPTION_TREND[YEAR_MONTH]`
  - Value: `VW_MONTHLY_PRESCRIPTION_TREND[TOTAL_PRESCRIPTIONS]`
  - Sort by `YEAR_MONTH` ascending
- Column chart: Total Drug Cost by Drug Category
  - Axis: `VW_DRUG_COST_ANALYSIS[DRUG_CATEGORY]`
  - Value: `VW_DRUG_COST_ANALYSIS[TOTAL_DRUG_COST]`

## Page 2: Prescription & Drug Cost Analysis

Visuals:
- Bar chart: Total Cost by Medicine
- Column chart: Weighted Average Prescription Cost by Drug Category
  - Axis: `VW_DRUG_COST_ANALYSIS[DRUG_CATEGORY]`
  - Value: `[Weighted Average Prescription Cost]`
- Table: Top Expensive Prescriptions
- Stacked bar: Insurance Covered vs Patient Out-of-Pocket
- Slicer: Drug Category

Use this measure instead of summing pre-aggregated drug averages:

```DAX
Weighted Average Prescription Cost =
DIVIDE(
    SUM(VW_DRUG_COST_ANALYSIS[TOTAL_DRUG_COST]),
    SUM(VW_DRUG_COST_ANALYSIS[TOTAL_PRESCRIPTIONS]),
    0
)
```

## Page 3: Patient/Customer View

This is the main detail page.

Use slicers:
- Drug Name
- Pharmacy Name
- Patient Search
- Diagnosis

Table visual columns:
- Patient Name
- Age
- Gender
- Diagnosis
- Drug Name
- Doctor Name
- Specialty
- Pharmacy Name
- Prescription Date
- Total Cost
- Insurance Covered
- Out-of-Pocket

Set `AGE` to **Don't summarize** in the table visual.

Demo:
Select Pharmacy = CVS Pharmacy and Drug = Metformin.
You should see Dr. Sarah Lee, John Smith, Type 2 Diabetes, $75 total cost, $55 insurance, $20 out-of-pocket.

## Page 4: Doctor/Prescriber Analysis

Visuals:
- Bar chart: Prescription Count by Doctor
- Bar chart: Average Cost by Doctor
- Matrix: Diagnosis treated by Specialty
- Table: High-Cost / Unusual Prescriptions
- Slicers: Doctor, Specialty, Drug Category

## Page 5: Q&A Chatbot / Natural Language Insights

Use the Power BI Q&A visual for the current demo. Power BI reports that this visual will retire in December 2026; use the Flask chatbot as the replacement path.

Suggested questions:
- What is the total drug cost?
- What is the total prescriptions?
- What is the average prescription cost?
- What is the most prescribed drug?
- Show doctor name and total prescriptions.
- What is the total insurance covered?
