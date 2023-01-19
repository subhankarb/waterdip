# Data Quality Metrics
ML Model health depends upon high-quality data features.
Data quality metrics help identify key quality issues such as data type mismatches, missing data, and more.

## List of Data Quality Metrics

| **Metrics**           | **Categorical**  | **Numeric**      | **Boolean**      | **Description**                                                          |
|-----------------------|------------------|------------------|------------------|--------------------------------------------------------------------------|
| **% of empty values** | :material-check: | :material-check: | :material-check: | The percent of nulls in model features                                   |
| **Missing Values**    | :material-check: |                  |                  | Count of new unique values that appear in baseline but not in production |
| **New Values**        | :material-check: |                  |                  | Count of new unique values that appear in production but not in baseline |

