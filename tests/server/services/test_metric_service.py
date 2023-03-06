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
from uuid import uuid4

import pytest
from fastapi import Depends, HTTPException
from pydantic import ValidationError

from tests.testing_helpers import (
    MODEL_ID,
    MODEL_ID_2,
    MODEL_ID_3,
    MODEL_ID_4,
    MODEL_ID_5,
    MODEL_VERSION_ID_V1,
    MODEL_VERSION_ID_V2,
    MODEL_VERSION_ID_V3,
    MODEL_VERSION_ID_V4,
    MODEL_VERSION_ID_V5,
    MongodbBackendTesting,
)
from waterdip.core.commons.models import (
    ColumnDataType,
    Environment,
    FixedTimeWindow,
    TimeRange,
)
from waterdip.server.db.models.dataset_rows import BaseEventRowDB, EventDataColumnDB
from waterdip.server.db.models.datasets import BaseDatasetDB
from waterdip.server.db.models.models import (
    BaseModelDB,
    BaseModelVersionDB,
    ModelBaseline,
    ModelBaselineTimeWindow,
    ModelBaselineTimeWindowType,
    ModelVersionSchemaFieldDetails,
    ModelVersionSchemaInDB,
)
from waterdip.server.apis.models.metrics import (
    PSIMetricResponse,
    PSIFeatureBreakdown
)
from waterdip.server.db.mongodb import (
    MONGO_COLLECTION_MODEL_VERSIONS,
    MONGO_COLLECTION_MODELS,
)
from waterdip.server.db.repositories.dataset_repository import DatasetRepository
from waterdip.server.db.repositories.dataset_row_repository import (
    BatchDatasetRowRepository,
    EventDatasetRowRepository,
)
from waterdip.server.db.repositories.model_repository import (
    ModelRepository,
    ModelVersionRepository,
)
from waterdip.server.errors.base_errors import EntityNotFoundError
from waterdip.server.services.dataset_service import DatasetService
from waterdip.server.services.metrics_service import (
    ClassificationPerformance,
    PSIMetricService,
)
from waterdip.server.services.model_service import ModelService, ModelVersionService

model = {
    "model_id": MODEL_ID,
    "model_name": "test_model",
    "positive_class": {
        "name": "test_positive_class",
    },
}
model_without_positive_class = {
    "model_id": MODEL_ID_2,
    "model_name": "test_model_without_positive_class",
    "positive_class": None,
}
model_with_moving_time_window = BaseModelDB(
    model_id=uuid.UUID(MODEL_ID_3),
    model_name="test_model",
    positive_class={
        "name": "test_positive_class",
    },
    baseline=ModelBaseline(),
)
model_with_fixed_time_window = BaseModelDB(
    model_id=uuid.UUID(MODEL_ID_4),
    model_name="test_model",
    positive_class={
        "name": "test_positive_class",
    },
    baseline=ModelBaseline(
        time_window=ModelBaselineTimeWindow(
            time_window_type=ModelBaselineTimeWindowType.FIXED_TIME_WINDOW,
            fixed_time_window=FixedTimeWindow(
                start_time=datetime.utcnow() - timedelta(days=7),
                end_time=datetime.utcnow(),
            ),
        )
    ),
)
model_with_dataset_env = BaseModelDB(
    model_id=uuid.UUID(MODEL_ID_5),
    model_name="test_model",
    positive_class={
        "name": "test_positive_class",
    },
    baseline=ModelBaseline(dataset_env=Environment.TRAINING),
)
model_version = {
    "model_version_id": MODEL_VERSION_ID_V1,
    "model_id": MODEL_ID,
    "name": "test_model_version",
    "version": 1,
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
}
model_version_2 = {
    "model_version_id": MODEL_VERSION_ID_V2,
    "model_id": MODEL_ID_2,
    "name": "test_model_version_2",
    "version": 1,
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
}
model_version_3 = BaseModelVersionDB(
    model_version_id=uuid.UUID(MODEL_VERSION_ID_V3),
    model_id=uuid.UUID(MODEL_ID_3),
    name="test_model_version_2",
    version=1,
    created_at=datetime.now(),
    updated_at=datetime.now(),
    version_schema=ModelVersionSchemaInDB(
        features={
            "f1": ModelVersionSchemaFieldDetails(
                data_type=ColumnDataType.CATEGORICAL,
            ),
        },
        predictions={
            "p1": ModelVersionSchemaFieldDetails(
                data_type=ColumnDataType.CATEGORICAL,
            ),
        },
    ),
)
model_version_4 = BaseModelVersionDB(
    model_version_id=uuid.UUID(MODEL_VERSION_ID_V4),
    model_id=uuid.UUID(MODEL_ID_4),
    name="test_model_version_2",
    version=1,
    created_at=datetime.now(),
    updated_at=datetime.now(),
    version_schema=ModelVersionSchemaInDB(
        features={
            "f1": ModelVersionSchemaFieldDetails(
                data_type=ColumnDataType.CATEGORICAL,
            ),
        },
        predictions={
            "p1": ModelVersionSchemaFieldDetails(
                data_type=ColumnDataType.CATEGORICAL,
            ),
        },
    ),
)
model_version_5 = BaseModelVersionDB(
    model_version_id=uuid.UUID(MODEL_VERSION_ID_V5),
    model_id=uuid.UUID(MODEL_ID_5),
    name="test_model_version_2",
    version=1,
    created_at=datetime.now(),
    updated_at=datetime.now(),
    version_schema=ModelVersionSchemaInDB(
        features={
            "f1": ModelVersionSchemaFieldDetails(
                data_type=ColumnDataType.CATEGORICAL,
            ),
        },
        predictions={
            "p1": ModelVersionSchemaFieldDetails(
                data_type=ColumnDataType.CATEGORICAL,
            ),
        },
    ),
)


@pytest.mark.usefixtures("mock_mongo_backend")
class TestMetricService:
    @classmethod
    def setup_class(self):
        self.mock_mongo_backend = MongodbBackendTesting.get_instance()

        self.classification_metric_service = ClassificationPerformance.get_instance(
            model_service=ModelService.get_instance(
                ModelRepository.get_instance(self.mock_mongo_backend)
            ),
            dataset_service=DatasetService.get_instance(
                DatasetRepository.get_instance(self.mock_mongo_backend)
            ),
            event_repo=EventDatasetRowRepository.get_instance(
                self.mock_mongo_backend),
        )
        self.psi_metric_service = PSIMetricService.get_instance(
            model_service=ModelService.get_instance(
                ModelRepository.get_instance(self.mock_mongo_backend)
            ),
            model_version_service=ModelVersionService.get_instance(
                ModelVersionRepository.get_instance(self.mock_mongo_backend)
            ),
            dataset_service=DatasetService.get_instance(
                DatasetRepository.get_instance(self.mock_mongo_backend)
            ),
            event_repo=EventDatasetRowRepository.get_instance(
                self.mock_mongo_backend),
            batch_repo=BatchDatasetRowRepository.get_instance(
                self.mock_mongo_backend),
        )

        self.mock_mongo_backend.database[MONGO_COLLECTION_MODELS].insert_many(
            [
                model,
                model_without_positive_class,
                model_with_fixed_time_window.dict(),
                model_with_moving_time_window.dict(),
                model_with_dataset_env.dict(),
            ]
        )

        self.mock_mongo_backend.database[MONGO_COLLECTION_MODEL_VERSIONS].insert_many(
            [
                model_version,
                model_version_2,
                model_version_3.dict(),
                model_version_4.dict(),
                model_version_5.dict(),
            ]
        )
        self.metricResponse = {
            "accuracy": {
                "29-01-2023": 0.5,
            },
            "true_positive": {
                "29-01-2023": 0.5,
            },
            "false_negative": {
                "29-01-2023": 0.5,
            },
            "true_negative": {
                "29-01-2023": 0.5,
            },
            "false_positive": {
                "29-01-2023": 0.5,
            },
            "precision": {
                "29-01-2023": 0.5,
            },
            "recall": {
                "29-01-2023": 0.5,
            },
            "sensitivity": {
                "29-01-2023": 0.5,
            },
            "specificity": {
                "29-01-2023": 0.5,
            },
            "f1": {
                "29-01-2023": 0.5,
            },
        }
        self.psiMetricResponse = {
            "22-02-2023": {
                "psi": 0.5,
            }
        }
        self.psiMetricServiceResponse = PSIMetricResponse(
            feat_breakdown=[PSIFeatureBreakdown(name='psi', driftscore=0.5)],
            data=[0.5],
            time_buckets=['22-02-2023'],
        )
        self.dataset = BaseEventRowDB(
            row_id=uuid.uuid4(),
            dataset_id=uuid.uuid4(),
            model_id=MODEL_ID,
            model_version_id=MODEL_VERSION_ID_V1,
            event_id="event_id",
            columns=[
                EventDataColumnDB(
                    name="column_name",
                    value="column_value",
                    value_numeric=1,
                    value_categorical="column_value",
                    data_type="CATEGORICAL",
                    mapping_type="FEATURE",
                    column_list_index=1,
                )
            ],
            created_at=datetime.now(),
        )

    def test_should_return_model_performance(self, mocker, mock_mongo_backend):
        mocker.patch(
            "waterdip.core.metrics.classification_metrics.ClassificationDateHistogramDBMetrics.aggregation_result",
            return_value=self.metricResponse,
        )
        mocker.patch(
            "waterdip.server.services.dataset_service.DatasetService.find_event_dataset_by_model_version_id",
            return_value=BaseEventRowDB(
                row_id=uuid.uuid4(),
                dataset_id=uuid.uuid4(),
                model_id=MODEL_ID,
                model_version_id=MODEL_VERSION_ID_V1,
                event_id="event_id",
                columns=[
                    EventDataColumnDB(
                        name="column_name",
                        value="column_value",
                        value_numeric=1,
                        value_categorical="column_value",
                        data_type="CATEGORICAL",
                        mapping_type="FEATURE",
                        column_list_index=1,
                    )
                ],
                created_at=datetime.now(),
            ),
        )
        model_performance = self.classification_metric_service.model_performance(
            model_id=MODEL_ID,
            model_version_id=MODEL_VERSION_ID_V1,
            time_range=TimeRange(
                start_time="2023-01-26T13:07:43.170771",
                end_time="2023-02-02T13:07:43.170771",
            ),
        )

        assert model_performance["accuracy"] == {
            "date": ["29-01-2023"], "value": [0.5]}

    def test_should_return_exception_if_positive_class_is_none(
        self, mocker, mock_mongo_backend
    ):
        mocker.patch(
            "waterdip.core.metrics.classification_metrics.ClassificationDateHistogramDBMetrics.aggregation_result",
            return_value=self.metricResponse,
        )
        mocker.patch(
            "waterdip.server.services.dataset_service.DatasetService.find_event_dataset_by_model_version_id",
            return_value=BaseEventRowDB(
                row_id=uuid.uuid4(),
                dataset_id=uuid.uuid4(),
                model_id=MODEL_ID_2,
                model_version_id=MODEL_VERSION_ID_V2,
                event_id="event_id",
                columns=[
                    EventDataColumnDB(
                        name="column_name",
                        value="column_value",
                        value_numeric=1,
                        value_categorical="column_value",
                        data_type="CATEGORICAL",
                        mapping_type="FEATURE",
                        column_list_index=1,
                    )
                ],
                created_at=datetime.now(),
            ),
        )
        with pytest.raises(HTTPException) as e:
            self.classification_metric_service.model_performance(
                model_id=MODEL_ID_2,
                model_version_id=MODEL_VERSION_ID_V2,
                time_range=TimeRange(
                    start_time="2023-01-26T13:07:43.170771",
                    end_time="2023-02-02T13:07:43.170771",
                ),
            )
        assert e.value.status_code == 400
        assert e.value.detail == "Positive class is not set for this model"

    def test_should_throw_error_if_dataset_id_is_none(self, mocker, mock_mongo_backend):
        mocker.patch(
            "waterdip.core.metrics.classification_metrics.ClassificationDateHistogramDBMetrics.aggregation_result",
            return_value=self.metricResponse,
        )
        mocker.patch(
            "waterdip.server.db.repositories.dataset_repository.DatasetRepository.find_datasets",
            return_value=[],
        )
        model_performance = None
        try:
            model_performance = self.classification_metric_service.model_performance(
                model_id=MODEL_ID,
                model_version_id=MODEL_VERSION_ID_V1,
                time_range=TimeRange(
                    start_time="2023-01-26T13:07:43.170771",
                    end_time="2023-02-02T13:07:43.170771",
                ),
            )
        except EntityNotFoundError as e:
            assert e.HTTP_STATUS == 404
            assert e.message == "Dataset not found"
        finally:
            assert model_performance is None

    def test_should_return_psi_metric_for_model_with_dataset_env(
        self, mocker, mock_mongo_backend
    ):
        mocker.patch(
            "waterdip.core.metrics.drift_psi.PSIMetrics.aggregation_result",
            return_value=self.psiMetricResponse,
        )
        mocker.patch(
            "waterdip.server.services.dataset_service.DatasetService.find_dataset_by_filter",
            return_value=BaseDatasetDB(
                dataset_id=uuid.uuid4(),
                dataset_name="dataset_name",
                dataset_type="EVENT",
                model_id=MODEL_ID_5,
                model_version_id=MODEL_VERSION_ID_V5,
                environment="TESTING",
            ),
        )
        mocker.patch(
            "waterdip.server.services.dataset_service.DatasetService.find_event_dataset_by_model_version_id",
            return_value=BaseEventRowDB(
                row_id=uuid.uuid4(),
                dataset_id=uuid.uuid4(),
                model_id=MODEL_ID_5,
                model_version_id=MODEL_VERSION_ID_V5,
                event_id="event_id",
                columns=[
                    EventDataColumnDB(
                        name="column_name",
                        value="column_value",
                        value_numeric=1,
                        value_categorical="column_value",
                        data_type="CATEGORICAL",
                        mapping_type="FEATURE",
                        column_list_index=1,
                    )
                ],
                created_at=datetime.now(),
            ),
        )
        psi_metric = self.psi_metric_service.metric_psi(
            model_id=MODEL_ID_5,
            model_version_id=MODEL_VERSION_ID_V5,
            time_range=TimeRange(
                start_time="2023-01-26T13:07:43.170771",
                end_time="2023-02-02T13:07:43.170771",
            ),
        )
        assert psi_metric == self.psiMetricServiceResponse

    def test_should_return_psi_metric_for_model_with_fixed_time_window(
        self, mocker, mock_mongo_backend
    ):
        mocker.patch(
            "waterdip.core.metrics.drift_psi.PSIMetrics.aggregation_result",
            return_value=self.psiMetricResponse,
        )
        mocker.patch(
            "waterdip.server.services.dataset_service.DatasetService.find_dataset_by_filter",
            return_value=BaseDatasetDB(
                dataset_id=uuid.uuid4(),
                dataset_name="dataset_name",
                dataset_type="EVENT",
                model_id=MODEL_ID_4,
                model_version_id=MODEL_VERSION_ID_V4,
                environment="TESTING",
            ),
        )
        mocker.patch(
            "waterdip.server.services.dataset_service.DatasetService.find_event_dataset_by_model_version_id",
            return_value=BaseEventRowDB(
                row_id=uuid.uuid4(),
                dataset_id=uuid.uuid4(),
                model_id=MODEL_ID_4,
                model_version_id=MODEL_VERSION_ID_V4,
                event_id="event_id",
                columns=[
                    EventDataColumnDB(
                        name="column_name",
                        value="column_value",
                        value_numeric=1,
                        value_categorical="column_value",
                        data_type="CATEGORICAL",
                        mapping_type="FEATURE",
                        column_list_index=1,
                    )
                ],
                created_at=datetime.now(),
            ),
        )
        psi_metric = self.psi_metric_service.metric_psi(
            model_id=MODEL_ID_4,
            model_version_id=MODEL_VERSION_ID_V4,
            time_range=TimeRange(
                start_time="2023-01-26T13:07:43.170771",
                end_time="2023-02-02T13:07:43.170771",
            ),
        )
        assert psi_metric == self.psiMetricServiceResponse

    def test_should_return_psi_metric_for_model_with_moving_time_window(
        self, mocker, mock_mongo_backend
    ):
        mocker.patch(
            "waterdip.core.metrics.drift_psi.PSIMetrics.aggregation_result",
            return_value=self.psiMetricResponse,
        )
        mocker.patch(
            "waterdip.server.services.dataset_service.DatasetService.find_dataset_by_filter",
            return_value=BaseDatasetDB(
                dataset_id=uuid.uuid4(),
                dataset_name="dataset_name",
                dataset_type="EVENT",
                model_id=MODEL_ID_3,
                model_version_id=MODEL_VERSION_ID_V3,
                environment="TESTING",
            ),
        )
        mocker.patch(
            "waterdip.server.services.dataset_service.DatasetService.find_event_dataset_by_model_version_id",
            return_value=BaseEventRowDB(
                row_id=uuid.uuid4(),
                dataset_id=uuid.uuid4(),
                model_id=MODEL_ID_3,
                model_version_id=MODEL_VERSION_ID_V3,
                event_id="event_id",
                columns=[
                    EventDataColumnDB(
                        name="column_name",
                        value="column_value",
                        value_numeric=1,
                        value_categorical="column_value",
                        data_type="CATEGORICAL",
                        mapping_type="FEATURE",
                        column_list_index=1,
                    )
                ],
                created_at=datetime.now(),
            ),
        )
        psi_metric = self.psi_metric_service.metric_psi(
            model_id=MODEL_ID_4,
            model_version_id=MODEL_VERSION_ID_V4,
            time_range=TimeRange(
                start_time="2023-01-26T13:07:43.170771",
                end_time="2023-02-02T13:07:43.170771",
            ),
        )
        assert psi_metric == self.psiMetricServiceResponse

    @classmethod
    def teardown_class(self):
        self.mock_mongo_backend.database[MONGO_COLLECTION_MODELS].delete_many({
        })
        self.mock_mongo_backend.database[MONGO_COLLECTION_MODEL_VERSIONS].delete_many(
            {}
        )
