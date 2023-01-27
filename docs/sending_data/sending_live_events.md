# Sending Live Events

One way to publish production data is by streaming data asynchronously, which allows for greater scalability.


This process is straightforward, but it requires that each event be structured as a Python dictionary that maps field names to values.


## Event Structure

#### Event Dictionary

Below is the structure of one prediction event. It consists of `features`, `predictions`, `event_id`
and `actuals`.

```python
event = {
    "event_id": "<PREDICTION_ID>",
    "features": {},
    "predictions": {},
    "actuals": {}
}
```

#### Actuals

In some cases, your model will produce a prediction that can be evaluated based on real-world data.

For example, if your model predicted that a client will buy term insurance, and one day later the client makes a purchase,
then you can evaluate the accuracy of that prediction by comparing it to similar cases in which no purchase was made.

####  Event ID
Each prediction must have a unique ID. This can be used later to log the actual value of the prediction.
Event ID should be unique.

If you do not care about actual logging send UUID4 as an `event_id`. For example: `str(uuid.uuid4())`


## Sending Prediction Events
To log the prediction event of your model, you can use the `/v1/log.events` API.
User can send multiple events in one POST API.

```python
import httpx
import uuid

HOST = "<backend_host> by default https://127.0.0.1:4422"

events = [
    {
        "event_id": str(uuid.uuid4()),
        "features": {
            "cap-shape": "x",
            "cap-surface": "s",
            "cap-color": "y",
            "bruises": "t",
            "odor": "l",
            "gill-attachment": "f",
            "gill-spacing": "c"
        },
        "predictions": {
            "class": "p"
        }
    }
]

async with httpx.AsyncClient() as client:
    response = await client.post(f"{HOST}/v1/log.events", data=events)
```