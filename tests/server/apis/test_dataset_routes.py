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

from tests.testing_helpers import (
    DATASET_BATCH_ID_V1_1,
    DATASET_BATCH_ID_V1_2,
    MODEL_VERSION_ID_V1,
)


@pytest.mark.usefixtures("test_client")
class TestDatasetList:
    def test_should_return_dataset_list(self, test_client: TestClient):
        response = test_client.get(
            f"/v1/list.datasets?model_version_id={MODEL_VERSION_ID_V1}"
            f"&limit=10&page=1&sort=created_at_asc"
        ).json()

        dataset_list, meta = response["dataset_list"], response["meta"]

        assert len(dataset_list) == 3
        assert meta["total"] == 3

    def test_should_return_no_dataset_if_pagination_beyond_size(
        self, test_client: TestClient
    ):
        response = test_client.get(
            f"/v1/list.datasets?model_version_id={MODEL_VERSION_ID_V1}"
            f"&limit=10&page=100&sort=created_at_asc"
        ).json()

        dataset_list, meta = response["dataset_list"], response["meta"]

        assert len(dataset_list) == 0
        assert meta["total"] == 3

    def test_should_return_limited_dataset(self, test_client: TestClient):
        response = test_client.get(
            f"/v1/list.datasets?model_version_id={MODEL_VERSION_ID_V1}"
            f"&limit=1&page=1&sort=created_at_asc"
        ).json()

        dataset_list, meta = response["dataset_list"], response["meta"]

        assert len(dataset_list) == 1
        assert meta["total"] == 3
        assert dataset_list[0]["dataset_id"] == DATASET_BATCH_ID_V1_1

    def test_should_return_created_at_sorted_dataset_desc(
        self, test_client: TestClient
    ):
        response = test_client.get(
            f"/v1/list.datasets?model_version_id={MODEL_VERSION_ID_V1}"
            f"&limit=1&page=1&sort=created_at_desc"
        ).json()

        dataset_list, meta = response["dataset_list"], response["meta"]

        assert len(dataset_list) == 1
        assert meta["total"] == 3
        assert dataset_list[0]["dataset_id"] == DATASET_BATCH_ID_V1_2

    def test_should_return_with_default_param(self, test_client: TestClient):
        response = test_client.get(
            f"/v1/list.datasets?model_version_id={MODEL_VERSION_ID_V1}"
        ).json()

        dataset_list, meta = response["dataset_list"], response["meta"]

        assert len(dataset_list) == 3
        assert meta["total"] == 3
