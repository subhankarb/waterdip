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

import random
import uuid
from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from tests.testing_helpers import MongodbBackendTesting
from waterdip.core.commons.models import ColumnDataType, ColumnMappingType
from waterdip.server.db.models.dataset_rows import BaseEventRowDB, EventDataColumnDB
from waterdip.server.db.models.models import (
    BaseModelVersionDB,
    ModelVersionSchemaFieldDetails,
    ModelVersionSchemaInDB,
)
from waterdip.server.db.mongodb import (
    MONGO_COLLECTION_EVENT_ROWS,
    MONGO_COLLECTION_MODEL_VERSIONS,
)
from waterdip.server.db.repositories.dataset_row_repository import (
    EventDatasetRowRepository,
)
from waterdip.server.services.row_service import EventDatasetRowService


@pytest.mark.usefixtures("mock_mongo_backend")
class TestRowService:
    @classmethod
    def setup_class(self):
        self.mock_mongo_backend = MongodbBackendTesting.get_instance()
        self.row_service = EventDatasetRowService.get_instance(
            EventDatasetRowRepository.get_instance(mongodb=self.mock_mongo_backend)
        )
        self.model_version_id = uuid.uuid4()
        self.model_id = uuid.uuid4()

        self.date_bins = [
            datetime.utcnow() - timedelta(days=8),
            datetime.utcnow() - timedelta(days=7),
            datetime.utcnow() - timedelta(days=6),
            datetime.utcnow() - timedelta(days=5),
            datetime.utcnow() - timedelta(days=4),
            datetime.utcnow() - timedelta(days=3),
            datetime.utcnow() - timedelta(days=2),
            datetime.utcnow() - timedelta(days=1),
            datetime.utcnow(),
        ]
        for i in range(0, len(self.date_bins)):
            self.date_bins[i] = self.date_bins[i].replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        self.events = [
            BaseEventRowDB(
                row_id=uuid.uuid4(),
                dataset_id=uuid.uuid4(),
                model_id=self.model_id,
                model_version_id=self.model_version_id,
                event_id="event_id",
                columns=[
                    EventDataColumnDB(
                        name="column_name",
                        value="column_value",
                        value_numeric=1,
                        value_categorical="column_value",
                        data_type=ColumnDataType.CATEGORICAL,
                        mapping_type=ColumnMappingType.FEATURE,
                        column_list_index=1,
                    )
                ],
                created_at=datetime(
                    self.date_bins[i].year,
                    self.date_bins[i].month,
                    self.date_bins[i].day,
                    0,
                    0,
                    0,
                    0,
                ),
                meta={"meta_key": "meta_value"},
            )
            for i in range(0, len(self.date_bins))
        ]
        self.mock_mongo_backend.database[MONGO_COLLECTION_EVENT_ROWS].insert_many(
            [event.dict() for event in self.events]
        )
        self.mock_mongo_backend.database[MONGO_COLLECTION_MODEL_VERSIONS].insert_one(
            BaseModelVersionDB(
                model_version_id=self.model_version_id,
                model_version="model_version_name",
                model_id=self.model_id,
                version_schema=ModelVersionSchemaInDB(
                    features={
                        "f1": ModelVersionSchemaFieldDetails(
                            data_type=ColumnDataType.NUMERIC
                        )
                    },
                    predictions={
                        "p1": ModelVersionSchemaFieldDetails(
                            data_type=ColumnDataType.NUMERIC
                        )
                    },
                ),
            ).dict()
        )

    def test_should_retuturn_prediction_average(self):
        prediction_average = self.row_service.prediction_average(str(self.model_id))

        assert prediction_average["pred_average"] == 1
        assert prediction_average["pred_average_window_days"] == 8

    def test_should_return_week_prediction_stats(self):
        week_prediction_stats = self.row_service.week_prediction_stats(
            str(self.model_id)
        )

        assert week_prediction_stats["pred_yesterday"] == 1
        assert week_prediction_stats["pred_percentage_change"] == 16
        assert week_prediction_stats["pred_trend_data"] == [0, 1, 1, 1, 1, 1, 1]

    def test_should_return_preidction_histogram(self):
        prediction_histogram = self.row_service.prediction_histogram(str(self.model_id))
        assert prediction_histogram.val == [1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert prediction_histogram.date_bins == self.date_bins

    def test_should_return_prediction_histogram_version(self):
        prediction_histogram_version = self.row_service.prediction_histogram_version(
            str(self.model_id)
        )
        for prediction_histogram in prediction_histogram_version:
            for key, value in prediction_histogram.items():
                if key == str(self.model_version_id):
                    assert value.val == [1, 1, 1, 1, 1, 1, 1, 1, 1]
                    assert value.date_bins == self.date_bins

    @classmethod
    def teardown_class(self):
        self.mock_mongo_backend.database[MONGO_COLLECTION_EVENT_ROWS].delete_many({})
