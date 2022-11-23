#  Copyright 2022-present, the Waterdip Labs Pvt. Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import datetime
import json

import pytest
from fastapi.testclient import TestClient

from tests.testing_helpers import MODEL_VERSION_ID_V1


@pytest.mark.usefixtures("test_client")
class TestLogDataset:
    def test_should_log_batch_dataset(self, test_client: TestClient):

        request_body = {
            "model_version_id": str(MODEL_VERSION_ID_V1),
            "environment": "TEST",
            "rows": [
                {"features": {"f1": 10, "f2": "red"}, "predictions": {"p1": 0}},
                {"features": {"f1": 100, "f2": "yellow"}, "predictions": {"p1": 1}},
            ],
        }
        response = test_client.post(url="/api/v1/log.dataset", json=request_body)

        assert response.status_code == 200


@pytest.mark.usefixtures("test_client")
class TestLogEvents:
    def test_should_log_events(self, test_client: TestClient):
        request_body = {
            "model_version_id": str(MODEL_VERSION_ID_V1),
            "timestamp": "2021-09-20 17:20:00",
            "events": [
                {
                    "features": {"f1": 11, "f2": "red"},
                    "predictions": {"p1": 1},
                    "actuals": {"p1": 1},
                },
                {"features": {"f1": 9, "f2": "pink"}, "predictions": {"p1": 0}},
            ],
        }

        response = test_client.post(url="/api/v1/log.events", json=request_body)

        assert response.status_code == 200
        assert response.json()["total"] == 2
