# **QuickStart**
In this document, you will learn how to create a model, upload dataset and send prediction data to Waterdip.

We are using the famous iris dataset, that is present in the scikit learn library to walk you through the various steps that are involved in getting you started and start monitoring your models.

- Import libraries and Download dataset

```python
#Import all the libraries:

import requests
import uuid
from sklearn import datasets
```

- Download the Iris dataset from sklearn
```python
iris = datasets.load_iris()
```


##**Register Model**

- To register a new model for monitoring, register_model() function is used. It takes in the name of the model as parameter.
- The function returns the model id of the new model.

```python
def register_model(model_name):
    post_url = "http://0.0.0.0:5001/v1/model.register"

    data_dict = {
        "model_name": model_name
    }

    r = requests.post(url=post_url, json=data_dict)
    return r.json()['model_id']
```


##**Register Model Version**

- This function registers a version for the existing model like version 1, version 2, etc. This increases reusability as same model can be used when there are few changes in the previous version and progress can be tracked.
- The function takes in model_id, data (for which the model is registered) as input and return model_version_id.
- Version_schema takes the names and data types of features and well as target (predictions) variables. Datatype can be NUMERICAL, CATEGORICAL or BOOLEAN. (Iris has only numerical feature values thus NUMERIC is hardcoded)

```python
def register_model_version(data, model_id):
    url = "http://0.0.0.0:5001/v1/model.version.register"

    data_dict = {
        "model_id": str(model_id),
        "model_version": "v1",
        "task_type": "MULTICLASS",
        "description": "This is iris dataset",
        "version_schema": {
            "features": {x: "NUMERIC" for x in data.feature_names},
            "predictions": {x: "NUMERIC" for x in data.target_names}
        }
    }

    r = requests.post(url=url, json=data_dict)
    return r.json()['model_version_id']
```

##**Log Training Dataset**

- Iris dataset(data) is passed as a parameter to the function log_training_data()
- Data_vals, target: a small part of dataset (for demo purpose)
- Data_dict: A dictionary that contains information about the dataset, I.e. model_version_id, and rows(events)

Note: The structure of upload_dataset, I.e. names of the keys of this dictionary must not be changed. Once the data is uploaded, it cannot be appended, updated or modified.
```python

def log_training_data(data, model_version_id):
    url = "http://0.0.0.0:5001/v1/log.dataset"

    data_dict = {
        "model_version_id": str(model_version_id),
        "dataset_name": "Training IRIS",
        "environment": "training"
    }

    rows = []

    data_vals = data.data[:1]
    target = data.target[:1]

    for doc, val in zip(data_vals, target):
        row_dict = {
            "features": {},
            "predictions": {}
        }

        for x, y in zip(data.feature_names, doc):
            row_dict['features'][x] = y

        for i, x in enumerate(data.target_names):
            if i == val:
                row_dict['predictions'][x] = 1
            else:
                row_dict['predictions'][x] = 0

        rows.append(row_dict)

    data_dict["rows"] = rows
    r = requests.post(url=url, json=data_dict)
```

##**Log events and actuals**

After we have uploaded the training dataset, we must also send the actuals data so that we can monitor the performance.

The following code  shows how to log events/actuals.
```python
def log_event(data, model_version_id):
    url = "http://0.0.0.0:5001/v1/log.event"

    data_dict = {
        "model_version_id": str(model_version_id)
    }
    events = []

    data_vals = data.data[:1]
    target = data.target[:1]

    for doc, val in zip(data_vals, target):
        row_dict = {
            "event_id": str(uuid.uuid4()),
            "features": {},
            "predictions": {},
            "actuals": {}
        }

        for x, y in zip(data.feature_names, doc):
            row_dict['features'][x] = y

        for i, x in enumerate(data.target_names):
            if i == val:
                row_dict['predictions'][x] = 1
                row_dict['actuals'][x] = 1
            else:
                row_dict['predictions'][x] = 0
                row_dict['actuals'][x] = 0

        events.append(row_dict)

    data_dict["events"] = events
    r = requests.post(url=url, json=data_dict)
```

- Log_event() takes model_version_id as parameter i.e. the version for which we want to log actuals
- Data_vals, target: a small part of dataset (for demo purpose)
- Data_dict contains model_version_id, and events dictionary that specifies the values for features, and corresponding targets and actuals.