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
import uuid

import pytest
from pydantic import ValidationError

from waterdip.server.apis.models.params import RequestSort
from waterdip.server.commons.models import DatasetType
from waterdip.server.db.models.alerts import AlertDB, BaseAlertDB
from waterdip.server.db.models.datasets import BaseDatasetDB
from waterdip.server.db.mongodb import (
    MONGO_COLLECTION_ALERTS,
    MONGO_COLLECTION_MODEL_VERSIONS,
    MONGO_COLLECTION_MODELS,
    MongodbBackend,
)
from waterdip.server.db.repositories.alert_repository import AlertRepository
from waterdip.server.db.repositories.dataset_repository import DatasetRepository
from waterdip.server.services.alert_service import AlertService
from waterdip.server.services.dataset_service import DatasetService


@pytest.mark.usefixtures("mock_mongo_backend")
class TestAlertService:
    def test_should_get_alerts(self, mocker, mock_mongo_backend: MongodbBackend):

        model_ids = [uuid.uuid4(), uuid.uuid4()]

        mocker.patch(
            "waterdip.server.db.repositories.alert_repository.AlertRepository.agg_alerts",
            return_value=[
                {
                    "_id": str(model_ids[0]),
                    "alerts": [
                        {"monitor_type": "DATA_QUALITY", "count": 1},
                        {"monitor_type": "DRIFT", "count": 1},
                    ],
                },
                {
                    "_id": str(model_ids[1]),
                    "alerts": [
                        {"monitor_type": "DRIFT", "count": 2},
                        {"monitor_type": "PERFORMANCE", "count": 1},
                    ],
                },
            ],
        )
        alert_service = AlertService.get_instance(
            AlertRepository.get_instance(mongodb=mock_mongo_backend)
        )
        alerts = alert_service.get_alerts(
            model_ids=[str(model_id) for model_id in model_ids]
        )

        assert alerts[str(model_ids[0])]["DRIFT"] == 1
        assert alerts[str(model_ids[0])]["DATA_QUALITY"] == 1
        assert alerts[str(model_ids[1])]["DRIFT"] == 2
        assert alerts[str(model_ids[1])]["PERFORMANCE"] == 1
