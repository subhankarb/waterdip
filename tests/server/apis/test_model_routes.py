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

from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from tests.testing_helpers import (
    MODEL_ID,
    MODEL_VERSION_ID_V1,
    MODEL_VERSION_ID_V1_NAME,
    MODEL_VERSION_V1_SCHEMA,
    MongodbBackendTesting,
)
from waterdip.server.db.mongodb import (
    MONGO_COLLECTION_MODEL_VERSIONS,
    MONGO_COLLECTION_MODELS,
)


@pytest.mark.usefixtures("test_client")
class TestRegisterModel:
    def test_should_register_model(self, test_client: TestClient):
        model_name = "test_model_p1"
        response = test_client.post(
            url="/v1/model.register", json={"model_name": model_name}
        )
        response_data = response.json()
        model_uuid_version = UUID(response_data["model_id"]).version

        assert response.status_code == 200
        assert response_data["model_name"] == model_name

        assert model_uuid_version == 4

        collection = MongodbBackendTesting.get_instance().database[
            MONGO_COLLECTION_MODELS
        ]

        result = collection.find(filter={"model_name": model_name})

        assert len(list(result)) == 1


@pytest.mark.usefixtures("test_client")
class TestRegisterModelVersion:
    def test_should_generate_model_version(self, test_client: TestClient):

        model_version = "test_version"
        request_body = {
            "model_id": MODEL_ID,
            "model_version": model_version,
            "task_type": "BINARY",
            "version_schema": {
                "features": {"f1": "NUMERIC"},
                "predictions": {"p1": "NUMERIC"},
            },
        }
        response = test_client.post(url="/v1/model.version.register", json=request_body)

        assert response.status_code == 200

        collection = MongodbBackendTesting.get_instance().database[
            MONGO_COLLECTION_MODEL_VERSIONS
        ]
        result = collection.find(
            filter={"model_id": MODEL_ID, "model_version": model_version}
        )

        assert len(list(result)) == 1
        collection.delete_one(
            filter={"model_id": MODEL_ID, "model_version": model_version}
        )


@pytest.mark.usefixtures("test_client")
class TestModelVersionInfo:
    def test_should_return_model_version_info(self, test_client: TestClient):

        response = test_client.get(
            url=f"/v1/model.version.info?model_version_id={MODEL_VERSION_ID_V1}"
        )
        assert response.status_code == 200

        response_data = response.json()
        model_version = response_data["model_version"]

        assert model_version["model_version"] == MODEL_VERSION_ID_V1_NAME
        assert model_version["model_version_id"] == MODEL_VERSION_ID_V1
        assert model_version["version_schema"] == MODEL_VERSION_V1_SCHEMA


@pytest.mark.usefixtures("test_client")
class TestModelInfo:
    def test_should_return_model_info(self, test_client: TestClient):

        response = test_client.get(url=f"/v1/model.info?model_id={MODEL_ID}")
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["model_id"] == MODEL_ID

        assert len(response_data["model_versions"]) == 2
