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
from datetime import datetime, timedelta

import pytest

from tests.testing_helpers import MongodbBackendTesting
from waterdip.core.commons.models import MonitorType
from waterdip.server.db.models.alerts import BaseAlertDB
from waterdip.server.db.mongodb import MongodbBackend
from waterdip.server.db.repositories.alert_repository import AlertRepository
from waterdip.server.services.alert_service import AlertService


@pytest.mark.usefixtures("mock_mongo_backend")
class TestAlertService:
    @classmethod
    def setup_class(cls):
        cls.mock_mongo_backend = MongodbBackendTesting.get_instance()
        cls.alert_repo = AlertRepository.get_instance(mongodb=cls.mock_mongo_backend)
        cls.alert_service = AlertService.get_instance(repository=cls.alert_repo)
        cls.model_id = uuid.uuid4()
        cls.alerts = [
            BaseAlertDB(
                monitor_type=MonitorType.DRIFT,
                model_id=cls.model_id,
                alert_id=uuid.uuid4(),
                monitor_id=uuid.uuid4(),
                created_at=datetime.utcnow() - timedelta(days=0),
            ),
            BaseAlertDB(
                monitor_type=MonitorType.DRIFT,
                model_id=cls.model_id,
                alert_id=uuid.uuid4(),
                monitor_id=uuid.uuid4(),
                created_at=datetime.utcnow() - timedelta(days=1),
            ),
            BaseAlertDB(
                monitor_type=MonitorType.PERFORMANCE,
                model_id=cls.model_id,
                alert_id=uuid.uuid4(),
                monitor_id=uuid.uuid4(),
                created_at=datetime.utcnow() - timedelta(days=2),
            ),
            BaseAlertDB(
                monitor_type=MonitorType.DATA_QUALITY,
                model_id=cls.model_id,
                alert_id=uuid.uuid4(),
                monitor_id=uuid.uuid4(),
                created_at=datetime.utcnow() - timedelta(days=3),
            ),
            BaseAlertDB(
                monitor_type=MonitorType.DRIFT,
                model_id=cls.model_id,
                alert_id=uuid.uuid4(),
                monitor_id=uuid.uuid4(),
                created_at=datetime.utcnow() - timedelta(days=4),
            ),
            BaseAlertDB(
                monitor_type=MonitorType.DRIFT,
                model_id=cls.model_id,
                alert_id=uuid.uuid4(),
                monitor_id=uuid.uuid4(),
                created_at=datetime.utcnow() - timedelta(days=5),
            ),
            BaseAlertDB(
                monitor_type=MonitorType.DATA_QUALITY,
                model_id=cls.model_id,
                alert_id=uuid.uuid4(),
                monitor_id=uuid.uuid4(),
                created_at=datetime.utcnow() - timedelta(days=6),
            ),
        ]
        for alert in cls.alerts:
            cls.alert_repo.insert_alert(alert)

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

    def test_should_return_alert_week_stats(self):
        alert_week_stats = self.alert_service.alert_week_stats(str(self.model_id))
        assert alert_week_stats["alert_percentage_change"] == 16
        assert alert_week_stats["alert_trend_data"] == [0, 1, 1, 1, 1, 1, 1]

    def test_should_count_alert_by_filter(self):
        alert_filter = {"model_id": str(self.model_id)}
        count = self.alert_service.count_alert_by_filter(alert_filter)

        assert count == len(self.alerts)

    def test_should_return_latest_alerts(self):
        latest_alerts = self.alert_service.find_alerts(str(self.model_id), 2)
        assert len(latest_alerts) == 2
        assert latest_alerts[0].alert_id == latest_alerts[0].alert_id
        assert latest_alerts[0].monitor_type == MonitorType.DRIFT
        assert latest_alerts[0].created_at == latest_alerts[0].created_at
        # assert latest_alerts[0].monitor_name == latest_alerts[0].monitor_name

        assert latest_alerts[1].alert_id == latest_alerts[1].alert_id
        assert latest_alerts[1].monitor_type == MonitorType.DRIFT
        assert latest_alerts[1].created_at == latest_alerts[1].created_at
        # assert latest_alerts[1].monitor_name == latest_alerts[1].monitor_name

    @classmethod
    def teardown_class(cls):
        pass
        # cls.mock_mongo_backend.database[MONGO_COLLECTION_ALERTS].drop()
