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

from tests.testing_helpers import MongodbBackendTesting
from waterdip.core.commons.models import DataQualityMetric
from waterdip.core.metrics.data_metrics import CountEmptyHistogram
from waterdip.core.monitors.evaluators.data_quality import EmptyValueEvaluator
from waterdip.core.monitors.models import (
    DataQualityBaseMonitorCondition,
    MonitorDimensions,
    MonitorThreshold,
)


class TestEmptyValueEvaluator:
    def test_should_generate_empty_violations(self, mocker):
        mocker.patch(
            "waterdip.core.metrics.data_metrics.CountEmptyHistogram.aggregation_result",
            return_value={
                "f1": {"empty_count": 51, "empty_percentage": 5.1, "total_count": 1000},
                "f2": {"empty_count": 21, "empty_percentage": 5.1, "total_count": 1000},
            },
        )

        condition = DataQualityBaseMonitorCondition(
            threshold=MonitorThreshold(threshold="gt", value=10),
            evaluation_metric=DataQualityMetric.EMPTY_VALUE,
            dimensions=MonitorDimensions(features=["f1", "f2"]),
        )
        metric = CountEmptyHistogram(
            collection=MongodbBackendTesting.get_instance().database[
                "event_collection"
            ],
            dataset_id=uuid.uuid4(),
        )

        evaluator = EmptyValueEvaluator(monitor_condition=condition, metric=metric)

        violations = evaluator.evaluate()

        assert len(violations) == 2

    def test_should_check_none_value_if_dimension_mismatch(self, mocker):
        mocker.patch(
            "waterdip.core.metrics.data_metrics.CountEmptyHistogram.aggregation_result",
            return_value={
                "f1": {"empty_count": 9, "empty_percentage": 5.1, "total_count": 1000},
            },
        )

        condition = DataQualityBaseMonitorCondition(
            threshold=MonitorThreshold(threshold="lt", value=10),
            evaluation_metric=DataQualityMetric.EMPTY_VALUE,
            dimensions=MonitorDimensions(features=["f1", "f2"]),
        )
        metric = CountEmptyHistogram(
            collection=MongodbBackendTesting.get_instance().database[
                "event_collection"
            ],
            dataset_id=uuid.uuid4(),
        )

        evaluator = EmptyValueEvaluator(monitor_condition=condition, metric=metric)

        violations = evaluator.evaluate()

        assert len(violations) == 1
