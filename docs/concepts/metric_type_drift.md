# Drift Metrics

The term "data drift" describes a phenomenon whereby data gets increasingly inaccurate as it ages. Distribution drift, which is the difference between two statistical distributions. The first distribution is the historic record of known information. The second is a forecast using that historic record. Data drift can have a negative effect on forecasts and other statistical analyses.

Data drift occurs because of external factors that cause changes to the distribution of data, such as new information from experts or customers, or changes in the method used to collect data. Drift can also be caused by incorrect formulas used in statistical models.

The difference between the two distributions is data drift

## List of Drift Metrics

| **Metrics** | **Categorical**  | **Numeric**      | **Boolean**      | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|-------------|------------------|------------------|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **PSI**     | :material-check: | :material-check: | :material-check: | Population Stability Index (PSI) compares <br/>the distribution of predicted probability in scoring data with predicted probability in training data. The idea is to check “How different the current scored data is, compared to the training data”. <br/>A generic rule to decide on model retraining based on PSI — <br/> **1. PSI < 0.1** — No change. You can continue using existing model. <br/> **2. PSI >=0.1** but less than 0.2 — Slight change is required. <br/> **3. PSI >=0.2** — Significant change is required. Ideally, you should not use this model anymore, retraining is required. |

