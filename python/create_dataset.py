"""
The MedScope dataset has already been generated in data/raw and data/cleaned.

For interview explanation:
- Raw data represents files arriving from pharmacy systems into S3.
- Cleaned data represents validated analytics-ready tables loaded into Snowflake/Power BI.
- clean_raw_data.py shows the cleaning logic used before reporting.
- data_quality_checks.py validates keys, nulls, relationships, and cost logic.
"""

print("Dataset is included in data/raw and data/cleaned.")
print("Run python/clean_raw_data.py to clean raw files.")
print("Run python/data_quality_checks.py to validate cleaned files.")
