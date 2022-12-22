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

import pytest
from fastapi.testclient import TestClient

from tests.testing_helpers import MODEL_ID, MODEL_VERSION_ID_V1, MongodbBackendTesting
from waterdip.server.db.mongodb import MONGO_COLLECTION_MONITORS


@pytest.mark.usefixtures("test_client")
class TestMonitorCreate:
    def test_should_create_data_quality_monitor(self, test_client: TestClient):
        monitor_name = "test_model_data_quality_monitor"

        data = {
            "monitor_name": monitor_name,
            "monitor_type": "DATA_QUALITY",
            "monitor_identification": {
                "model_id": MODEL_ID,
                "model_version_id": MODEL_VERSION_ID_V1,
            },
            "monitor_condition": {
                "evaluation_metric": "MISSING_VALUE",
                "dimensions": {"features": ["f1", "f2"]},
                "threshold": {"threshold": "gt", "value": 20},
                "evaluation_window": "3d",
            },
        }

        response = test_client.post(url="/v1/monitor.create", json=data)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["monitor_name"] == monitor_name

        collection = MongodbBackendTesting.get_instance().database[
            MONGO_COLLECTION_MONITORS
        ]

        result = collection.find(filter={"monitor_name": monitor_name})

        assert len(list(result)) == 1
        collection.delete_one(filter={"monitor_name": monitor_name})

    def test_should_create_performance_monitor(self, test_client: TestClient):
        monitor_name = "test_model_perf_monitor"

        data = {
            "monitor_name": monitor_name,
            "monitor_type": "MODEL_PERFORMANCE",
            "monitor_identification": {
                "model_id": MODEL_ID,
                "model_version_id": MODEL_VERSION_ID_V1,
            },
            "monitor_condition": {
                "evaluation_metric": "PRECISION",
                "threshold": {"threshold": "lt", "value": 0.5},
                "evaluation_window": "3d",
            },
        }

        response = test_client.post(url="/v1/monitor.create", json=data)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["monitor_name"] == monitor_name

        collection = MongodbBackendTesting.get_instance().database[
            MONGO_COLLECTION_MONITORS
        ]

        result = collection.find(filter={"monitor_name": monitor_name})

        assert len(list(result)) == 1
        collection.delete_one(filter={"monitor_name": monitor_name})

    def test_should_drift_monitor(self, test_client: TestClient):
        monitor_name = "test_model_drift_monitor"

        data = {
            "monitor_name": monitor_name,
            "monitor_type": "DRIFT",
            "monitor_identification": {
                "model_id": MODEL_ID,
                "model_version_id": MODEL_VERSION_ID_V1,
            },
            "monitor_condition": {
                "evaluation_metric": "PSI",
                "dimensions": {"features": ["f1"]},
                "threshold": {"threshold": "lt", "value": 0.5},
                "baseline": {
                    "time_window": {
                        "aggregation_period": "1d",
                        "skip_period": "1d",
                        "time_period": "15d",
                    }
                },
                "evaluation_window": "3d",
            },
        }

        response = test_client.post(url="/v1/monitor.create", json=data)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["monitor_name"] == monitor_name

        collection = MongodbBackendTesting.get_instance().database[
            MONGO_COLLECTION_MONITORS
        ]

        result = collection.find(filter={"monitor_name": monitor_name})

        assert len(list(result)) == 1
        collection.delete_one(filter={"monitor_name": monitor_name})
