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

from tests.testing_helpers import MongodbBackendTesting
from waterdip.core.commons.models import MonitorType
from waterdip.server.db.models.alerts import AlertDB, BaseAlertDB
from waterdip.server.db.mongodb import (
    MONGO_COLLECTION_ALERTS,
    MONGO_COLLECTION_MODEL_VERSIONS,
    MONGO_COLLECTION_MODELS,
    MongodbBackend,
)
from waterdip.server.db.repositories.alert_repository import AlertRepository


@pytest.mark.usefixtures("mock_mongo_backend")
class TestAlertRepository:
    @classmethod
    def setup_class(cls):
        cls.mock_mongo_backend = MongodbBackendTesting.get_instance()
        cls.alert_repository = AlertRepository(mongodb=cls.mock_mongo_backend)
        cls.model_ids = [uuid.uuid4(), uuid.uuid4()]
        cls.alerts = [
            BaseAlertDB(
                monitor_type=MonitorType.DRIFT,
                model_id=cls.model_ids[0],
                alert_id=uuid.uuid4(),
                monitor_id=uuid.uuid4(),
                model_version="model_version_1",
                created_at=datetime.datetime.utcnow(),
            ),
            BaseAlertDB(
                monitor_type=MonitorType.PERFORMANCE,
                model_id=cls.model_ids[1],
                alert_id=uuid.uuid4(),
                monitor_id=uuid.uuid4(),
                model_version="model_version_1",
                created_at=datetime.datetime.utcnow(),
            ),
            BaseAlertDB(
                monitor_type=MonitorType.DATA_QUALITY,
                model_id=cls.model_ids[0],
                alert_id=uuid.uuid4(),
                monitor_id=uuid.uuid4(),
                model_version="model_version_1",
                created_at=datetime.datetime.utcnow(),
            ),
            BaseAlertDB(
                monitor_type=MonitorType.DRIFT,
                model_id=cls.model_ids[1],
                alert_id=uuid.uuid4(),
                monitor_id=uuid.uuid4(),
                model_version="model_version_1",
                created_at=datetime.datetime.utcnow(),
            ),
            BaseAlertDB(
                monitor_type=MonitorType.DRIFT,
                model_id=cls.model_ids[1],
                alert_id=uuid.uuid4(),
                monitor_id=uuid.uuid4(),
                model_version="model_version_2",
                created_at=datetime.datetime.utcnow(),
            ),
            BaseAlertDB(
                monitor_type=MonitorType.DATA_QUALITY,
                model_id=uuid.uuid4(),
                alert_id=uuid.uuid4(),
                monitor_id=uuid.uuid4(),
                model_version="model_version_2",
                created_at=datetime.datetime.utcnow(),
            ),
        ]
        cls.mock_mongo_backend.database[MONGO_COLLECTION_ALERTS].insert_many(
            [alert.dict() for alert in cls.alerts]
        )

    def test_should_count_alerts_by_monitor_type_per_model(
        self, mock_mongo_backend: MongodbBackend
    ):
        agg_pipeline = [
            {
                "$match": {
                    "model_id": {"$in": [str(model_id) for model_id in self.model_ids]}
                }
            },
            {
                "$group": {
                    "_id": {"model_id": "$model_id", "monitor_type": "$monitor_type"},
                    "count": {"$sum": 1},
                }
            },
            {
                "$group": {
                    "_id": "$_id.model_id",
                    "alerts": {
                        "$push": {
                            "monitor_type": "$_id.monitor_type",
                            "count": "$count",
                        }
                    },
                }
            },
        ]
        alerts_count = list(self.alert_repository.agg_alerts(agg_pipeline=agg_pipeline))

        for alert in alerts_count:
            if alert["_id"] == str(self.model_ids[0]):
                if alert["alerts"][0]["monitor_type"] == MonitorType.DRIFT:
                    assert alert["alerts"][0]["count"] == 1
                if alert["alerts"][1]["monitor_type"] == MonitorType.DATA_QUALITY:
                    assert alert["alerts"][1]["count"] == 1
            if alert["_id"] == str(self.model_ids[1]):
                if alert["alerts"][0]["monitor_type"] == MonitorType.DRIFT:
                    assert alert["alerts"][0]["count"] == 2
                if alert["alerts"][1]["monitor_type"] == MonitorType.PERFORMANCE:
                    assert alert["alerts"][1]["count"] == 1

    @classmethod
    def teardown_class(cls):
        cls.mock_mongo_backend.database[MONGO_COLLECTION_ALERTS].drop()
        cls.mock_mongo_backend.database[MONGO_COLLECTION_MODELS].drop()
        cls.mock_mongo_backend.database[MONGO_COLLECTION_MODEL_VERSIONS].drop()
