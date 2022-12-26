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

import pytest

from tests.testing_helpers import MongodbBackendTesting
from waterdip.server.commons.models import (
    DataQualityMetric,
    DriftMetric,
    MonitorType,
    PerformanceMetric,
)
from waterdip.server.db.models.models import ModelBaseline
from waterdip.server.db.models.monitors import (
    BaseMonitorDB,
    DataQualityBaseMonitorCondition,
    DriftBaseMonitorCondition,
    MonitorDimensions,
    MonitorIdentification,
    MonitorThreshold,
    PerformanceBaseMonitorCondition,
)
from waterdip.server.db.mongodb import MONGO_COLLECTION_MONITORS
from waterdip.server.db.repositories.monitor_repository import MonitorRepository


@pytest.mark.usefixtures("mock_mongo_backend")
class TestMonitorRepository:
    monitor_threshold = MonitorThreshold(threshold="lt", value=1.0)
    monitor_identification = MonitorIdentification(
        model_version_id=uuid.uuid4(), model_id=uuid.uuid4()
    )

    def test_should_insert_data_quality_monitor(
        self, mock_mongo_backend: MongodbBackendTesting
    ):
        monitor_repo = MonitorRepository(mongodb=mock_mongo_backend)

        data_quality_condition = DataQualityBaseMonitorCondition(
            threshold=self.monitor_threshold,
            evaluation_window="10d",
            evaluation_metric=DataQualityMetric.EMPTY_VALUE,
            dimensions=MonitorDimensions(features=["f1"]),
        )

        monitor_id, monitor_name = uuid.uuid4(), "data_quality_monitor"
        data_quality_monitor = BaseMonitorDB(
            monitor_id=monitor_id,
            monitor_name="data_quality_monitor",
            monitor_identification=self.monitor_identification,
            monitor_condition=data_quality_condition,
            monitor_type=MonitorType.DATA_QUALITY,
        )
        monitor_repo.insert_monitor(data_quality_monitor)

        created_monitor_version_in_db = mock_mongo_backend.database[
            MONGO_COLLECTION_MONITORS
        ].find_one(filter={"monitor_id": str(monitor_id)})

        assert created_monitor_version_in_db["monitor_name"] == monitor_name

    def test_should_insert_model_pref_monitor(
        self, mock_mongo_backend: MongodbBackendTesting
    ):
        monitor_repo = MonitorRepository(mongodb=mock_mongo_backend)

        perf_condition = PerformanceBaseMonitorCondition(
            threshold=self.monitor_threshold, evaluation_metric=PerformanceMetric.F1
        )
        monitor_id, monitor_name = uuid.uuid4(), "perf_monitor"
        perf_monitor = BaseMonitorDB(
            monitor_id=monitor_id,
            monitor_name=monitor_name,
            monitor_identification=self.monitor_identification,
            monitor_condition=perf_condition,
            monitor_type=MonitorType.PERFORMANCE,
        )
        res = monitor_repo.insert_monitor(perf_monitor)

        created_monitor_version_in_db = mock_mongo_backend.database[
            MONGO_COLLECTION_MONITORS
        ].find_one(filter={"monitor_id": str(monitor_id)})

        assert created_monitor_version_in_db["monitor_name"] == monitor_name
        assert res.monitor_name == monitor_name

    def test_should_insert_model_drift_monitor(
        self, mock_mongo_backend: MongodbBackendTesting
    ):
        monitor_repo = MonitorRepository(mongodb=mock_mongo_backend)

        drift_condition = DriftBaseMonitorCondition(
            threshold=self.monitor_threshold,
            evaluation_metric=DriftMetric.PSI,
            dimensions=MonitorDimensions(features=["f1"]),
            baseline=ModelBaseline(),
        )
        monitor_id, monitor_name = uuid.uuid4(), "drift_monitor"
        drift_monitor = BaseMonitorDB(
            monitor_id=monitor_id,
            monitor_name=monitor_name,
            monitor_identification=self.monitor_identification,
            monitor_condition=drift_condition,
            monitor_type=MonitorType.DRIFT,
        )
        res = monitor_repo.insert_monitor(drift_monitor)

        created_monitor_version_in_db = mock_mongo_backend.database[
            MONGO_COLLECTION_MONITORS
        ].find_one(filter={"monitor_id": str(monitor_id)})

        assert created_monitor_version_in_db["monitor_name"] == monitor_name
        assert res.monitor_name == monitor_name
