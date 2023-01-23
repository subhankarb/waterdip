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
import uuid
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
from waterdip.server.db.models.models import BaseModelVersionDB, ModelVersionSchemaInDB
from waterdip.server.db.mongodb import MONGO_COLLECTION_MODEL_VERSIONS


@pytest.mark.usefixtures("test_client")
class TestLogDataset:
    LOCAL_MODEL_VERSION = uuid.uuid4()

    @classmethod
    def setup_class(cls):
        """setup any state specific to the execution of the given class (which
        usually contains tests).
        """

        database = MongodbBackendTesting.get_instance().database
        model_version = BaseModelVersionDB(
            model_version_id=cls.LOCAL_MODEL_VERSION,
            model_version=MODEL_VERSION_ID_V1_NAME,
            model_id=UUID(MODEL_ID),
            created_at=datetime.datetime(year=2022, month=11, day=17),
            version_schema=ModelVersionSchemaInDB(**MODEL_VERSION_V1_SCHEMA),
        )
        database[MONGO_COLLECTION_MODEL_VERSIONS].insert_many(
            documents=[model_version.dict()]
        )

    @classmethod
    def teardown_class(cls):
        """teardown any state that was previously setup with a call to
        setup_class.
        """
        database = MongodbBackendTesting.get_instance().database
        database[MONGO_COLLECTION_MODEL_VERSIONS].delete_many(
            filter={"model_version_id": str(cls.LOCAL_MODEL_VERSION)}
        )

    def test_should_log_batch_dataset(self, test_client: TestClient):

        request_body = {
            "model_version_id": str(self.LOCAL_MODEL_VERSION),
            "environment": "TRAINING",
            "rows": [
                {"features": {"f1": 10, "f2": "red"}, "predictions": {"p1": 0}},
                {"features": {"f1": 100, "f2": "yellow"}, "predictions": {"p1": 1}},
            ],
        }
        response = test_client.post(url="/v1/log.dataset", json=request_body)

        assert response.status_code == 200

    def test_should_through_error_for_multiple_dataset_for_same_env(
        self, test_client: TestClient
    ):
        database = MongodbBackendTesting.get_instance().database
        a = database["wd_dataset_batch_rows"].find(
            filter={
                "model_version_id": str(MODEL_VERSION_ID_V1),
                "environment": "VALIDATION",
            }
        )
        for a1 in a:
            print("========")
            print(a1)
        request_body = {
            "model_version_id": str(MODEL_VERSION_ID_V1),
            "environment": "VALIDATION",
            "rows": [
                {"features": {"f1": 10, "f2": "red"}, "predictions": {"p1": 0}},
                {"features": {"f1": 100, "f2": "yellow"}, "predictions": {"p1": 1}},
            ],
        }
        response = test_client.post(url="/v1/log.dataset", json=request_body)

        assert response.status_code == 200

        response = test_client.post(url="/v1/log.dataset", json=request_body)

        assert response.status_code == 500


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

        response = test_client.post(url="/v1/log.events", json=request_body)

        assert response.status_code == 200
        assert response.json()["total"] == 2
