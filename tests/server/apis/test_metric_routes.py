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

from tests.testing_helper_metrics_data import (
    METRICS_DATASET_BATCH_ID_V1_1,
    METRICS_DATASET_EVENT_ID_V1,
    METRICS_MODEL_ID,
    METRICS_MODEL_VERSION_ID_V1,
)


@pytest.mark.usefixtures("test_client")
class TestDatasetMetrics:
    def test_should_register_model(self, mocker, test_client: TestClient):
        mocker.patch(
            "waterdip.core.metrics.data_metrics.NumericCountHistogram.aggregation_result",
            return_value={},
        )
        params = {
            "model_id": METRICS_MODEL_ID,
            "model_version_id": METRICS_MODEL_VERSION_ID_V1,
            "dataset_id": METRICS_DATASET_BATCH_ID_V1_1,
        }
        response = test_client.get(url="/v1/metrics.dataset", params=params)
        response_data = response.json()
        print(response_data)

    def test_should_register_model_1(self, mocker, test_client: TestClient):
        mocker.patch(
            "waterdip.core.metrics.data_metrics.NumericCountHistogram.aggregation_result",
            return_value={},
        )
        params = {
            "model_id": METRICS_MODEL_ID,
            "model_version_id": METRICS_MODEL_VERSION_ID_V1,
            "dataset_id": METRICS_DATASET_EVENT_ID_V1,
            "start_time": "2022-11-30T00:00:00",
            "end_time": "2022-12-30T00:00:00",
        }
        response = test_client.get(url="/v1/metrics.dataset", params=params)
        response_data = response.json()
        print(response_data)
