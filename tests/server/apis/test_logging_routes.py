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

from tests.testing_helpers import MODEL_VERSION_ID_V1


@pytest.mark.usefixtures("test_client")
class TestLogDataset:
    def test_asd(self, test_client: TestClient):

        request_body = {
            "model_version_id": str(MODEL_VERSION_ID_V1),
            "environment": "TEST",
            "rows": [
                {"features": {"f1": 10}, "predictions": {"p1": 0}},
                {"features": {"f1": 100}, "predictions": {"p1": 1}},
            ],
        }
        response = test_client.post(url="/api/v1/log.dataset", json=request_body)

        assert response.status_code == 200

        print(response.json())
