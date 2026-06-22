# MedScope Power BI Build Steps

Final Power BI file name:
`MedScope_Dashboard.pbix`

## Page 1: Executive Overview

Goal: executive-level snapshot of prescription volume, cost, doctors, patients, and most prescribed drug.

Visuals:
- Card: Total Prescriptions
- Card: Total Drug Cost
- Card: Average Prescription Cost
- Card: Total Patients
- Card: Total Doctors
- Card: Most Prescribed Drug
- Line chart: Monthly Prescription Trend
- Bar chart: Total Cost by Drug Category
- Slicers: Year-Month, Drug Category, Pharmacy

## Page 2: Prescription & Drug Cost Analysis

Visuals:
- Bar chart: Total Cost by Medicine
- Bar chart: Total Cost by Drug Category
- Line chart: Monthly Prescription Trend
- Table: Top 10 Expensive Drugs
- Stacked bar: Insurance Covered vs Patient Out-of-Pocket
- Slicers: Drug Category, Manufacturer, Diagnosis

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

Use Power BI Q&A visual:
Suggested questions:
- Which drug has the highest total cost?
- Which doctor prescribed the most medicines?
- Which pharmacy has the highest total cost?
- Why was Metformin prescribed?
- What is the average out-of-pocket cost by pharmacy?
- Show prescription count by drug category.

Also add a smart narrative visual summarizing:
- Total prescription volume
- Highest-cost drug/category
- Highest-volume pharmacy
- Out-of-pocket trend
