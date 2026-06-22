# MedScope Problem Statement

Healthcare and pharmacy organizations handle large prescription datasets across patients, doctors, pharmacies, drugs, and insurance claims. Business teams need a reliable way to monitor medication cost, prescribing behavior, pharmacy performance, insurance coverage, and patient out-of-pocket burden.

MedScope solves this by creating an end-to-end analytics pipeline using S3, Snowflake, SQL, Python, and Power BI.

## Core Business Questions

1. Which medicines are most prescribed?
2. Which medicines generate the highest total cost?
3. Which pharmacy has the highest prescription volume and cost?
4. Which doctor prescribed a selected medicine?
5. Why was a selected patient prescribed a medicine?
6. How much did insurance cover compared with patient out-of-pocket cost?
7. Which diagnosis categories create the highest prescription spend?
8. Which patients have high affordability burden?
9. Are there unusual/high-cost prescriptions?
10. Can users ask plain-English questions using a Q&A chatbot layer?

## Important Dashboard Scenario

A business user selects:
- Pharmacy = CVS Pharmacy
- Drug = Metformin

The dashboard returns:
- Patient/customer
- Prescribing doctor
- Doctor specialty
- Diagnosis/reason
- Date
- Total cost
- Insurance covered
- Patient out-of-pocket cost
