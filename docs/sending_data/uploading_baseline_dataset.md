# Uploading Baseline Dataset

To monitor data integrity and drift issues in incoming production data,
you need a baseline dataset with which to compare it.

By default, the baseline data is the last 15 days moving window timeline of production data.
User can change the baseline to pre-production data i.e. Training, Testing or Validation dataset.
In order to do that user needs to upload the pre-production dataset.

## Uploading Datasets

!!! info

    For every Model Version user can upload maximum 3 datasets, each for these three ENVIRONMENTS
    i.e. **`TRAINING`**, **`TESTING`** and **`VALIDATION`**


### Uploading Training Dataset

!!! info "Dataset Reference"

    For this example, [Mushroom Dataset](https://www.kaggle.com/datasets/uciml/mushroom-classification)
    has been used.

To log the training or test datasets of your model, you can use the `/v1/log.dataset` API.

For example, if we have the following training set:

```python
import pandas as pd

training_features = pd.DataFrame({
    "cap-shape": ["x", "x", "b"],
    "cap-surface": ["s", "s", "s"],
    "cap-color": ["n", "y", "w"],
    "bruises": ["t", "t", "t"],
    "odor": ["p", "a", "l"],
    "gill-attachment": ["f", "f", "f"],
    "gill-spacing": ["c", "c", "c"],
})

training_predictions = pd.DataFrame({
    "class": ["p", "e", "e"],
})
```

Then we can upload the training data using below process
```python
import requests

HOST = "<backend_host> by default https://127.0.0.1:4422"
MODEL_VERSION_ID = "<<model_version_id>>"

predictions = training_predictions.to_dict(orient='index')

rows = []

for index_no, features in training_features.to_dict(orient='index').items():
    row = {
        "features": features,
        "predictions": training_predictions.iloc[index_no]["class"]
    }
    rows.append(row)

data_dict = {
    "model_version_id": MODEL_VERSION_ID,
    "environment": "TRAINING",
    "rows": rows
}

requests.post(url=f"{HOST}/v1/log.dataset", json=data_dict)

```

### Uploading Testing and Validation Dataset

For uploading Testing or validation dataset you just need to change the environment variable

For example, if we have to upload Testing dataset:

```python
data_dict = {
    "model_version_id": MODEL_VERSION_ID,
    "environment": "TESTING",
    "rows": rows
}
```

For example, if we have to upload Validation dataset:

```python
data_dict = {
    "model_version_id": MODEL_VERSION_ID,
    "environment": "VALIDATION",
    "rows": rows
}
```