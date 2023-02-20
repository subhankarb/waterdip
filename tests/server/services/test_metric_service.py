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
from datetime import datetime
from uuid import uuid4

import pytest
from fastapi import Depends, HTTPException
from pydantic import ValidationError

from tests.testing_helpers import (
    MODEL_ID,
    MODEL_ID_2,
    MODEL_VERSION_ID_V1,
    MODEL_VERSION_ID_V2,
    MongodbBackendTesting,
)
from waterdip.core.commons.models import TimeRange
from waterdip.server.apis.models.metrics import PerfomanceMetricResponse
from waterdip.server.db.models.dataset_rows import BaseEventRowDB, EventDataColumnDB
from waterdip.server.db.mongodb import (
    MONGO_COLLECTION_MODEL_VERSIONS,
    MONGO_COLLECTION_MODELS,
)
from waterdip.server.db.repositories.dataset_repository import DatasetRepository
from waterdip.server.db.repositories.dataset_row_repository import (
    EventDatasetRowRepository,
)
from waterdip.server.db.repositories.model_repository import ModelRepository
from waterdip.server.errors.base_errors import EntityNotFoundError
from waterdip.server.services.dataset_service import DatasetService
from waterdip.server.services.metrics_service import ClassificationPerformance
from waterdip.server.services.model_service import ModelService


@pytest.mark.usefixtures("mock_mongo_backend")
class TestMetricService:
    @classmethod
    def setup_class(self):
        self.mock_mongo_backend = MongodbBackendTesting.get_instance()

        self.metric_service = ClassificationPerformance.get_instance(
            model_service=ModelService.get_instance(
                ModelRepository.get_instance(self.mock_mongo_backend)
            ),
            dataset_service=DatasetService.get_instance(
                DatasetRepository.get_instance(self.mock_mongo_backend)
            ),
            event_repo=EventDatasetRowRepository.get_instance(self.mock_mongo_backend),
        )

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

        self.mock_mongo_backend.database[MONGO_COLLECTION_MODELS].insert_many(
            [model, model_without_positive_class]
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

        self.mock_mongo_backend.database[MONGO_COLLECTION_MODEL_VERSIONS].insert_many(
            [model_version, model_version_2]
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
        model_performance = self.metric_service.model_performance(
            model_id=MODEL_ID,
            model_version_id=MODEL_VERSION_ID_V1,
            time_range=TimeRange(
                start_time="2023-01-26T13:07:43.170771",
                end_time="2023-02-02T13:07:43.170771",
            ),
        )

        assert model_performance["accuracy"] == {"date": ["29-01-2023"], "value": [0.5]}

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
            self.metric_service.model_performance(
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
            model_performance = self.metric_service.model_performance(
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

    @classmethod
    def teardown_class(self):
        self.mock_mongo_backend.database[MONGO_COLLECTION_MODELS].delete_many({})
        self.mock_mongo_backend.database[MONGO_COLLECTION_MODEL_VERSIONS].delete_many(
            {}
        )
