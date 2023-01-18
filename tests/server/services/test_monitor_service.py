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

import uuid
from uuid import uuid4

import pytest
from pydantic import ValidationError

from tests.testing_helpers import MODEL_ID, MODEL_VERSION_ID_V1, MongodbBackendTesting
from waterdip.server.db.mongodb import MONGO_COLLECTION_MONITORS , MONGO_COLLECTION_ALERTS , MONGO_COLLECTION_MODELS
from waterdip.server.db.repositories.monitor_repository import MonitorRepository
from waterdip.server.services.monitor_service import MonitorService


@pytest.mark.usefixtures("mock_mongo_backend")
class TestMonitorService:
    @classmethod
    def setup_class(self):
        self.mock_mongo_backend = MongodbBackendTesting.get_instance()
        self.monitor_service = MonitorService.get_instance(
            MonitorRepository.get_instance(mongodb=self.mock_mongo_backend)
        )
        self.monitor_name = "test_model_monitor"
        data = {
            "monitor_id": str(uuid4()),
            "monitor_name": self.monitor_name,
            "monitor_type": "DRIFT",
            "monitor_identification": {
                "model_id": str(MODEL_ID),
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
        self.mock_mongo_backend.database[MONGO_COLLECTION_MONITORS].delete_many({})
        self.mock_mongo_backend.database[MONGO_COLLECTION_MONITORS].insert_one(data)
        self.MODEL_NAME = "Test Model"
        model = {
            "model_id" : MODEL_ID,
            "model_name" : self.MODEL_NAME
        }
        self.mock_mongo_backend.database[MONGO_COLLECTION_MODELS].insert_one(model)

    def test_should_return_monitor_list(self):
        response = self.monitor_service.list_monitors()

        assert response[0].monitor_name == self.monitor_name
        assert len(list(response)) == 1

    @classmethod
    def teardown_class(self):
        self.mock_mongo_backend.database[MONGO_COLLECTION_MONITORS].delete_many({})
        self.mock_mongo_backend.database[MONGO_COLLECTION_MODELS].delete_many({})
