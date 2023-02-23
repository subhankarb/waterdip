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
from uuid import UUID

from tests.testing_helper_metrics_data import (
    METRICS_MODEL_VERSION_V1_SCHEMA,
    metrics_batch_data_rows,
    metrics_event_rows,
)
from tests.testing_helpers import MongodbBackendTesting, clean_model_data
from waterdip.core.commons.models import DatasetType, Environment, TimeRange
from waterdip.core.metrics.drift_psi import PSIMetrics
from waterdip.server.db.models.dataset_rows import (
    BaseDatasetBatchRowDB,
    BaseEventRowDB,
    DataColumn,
    EventDataColumnDB,
)
from waterdip.server.db.models.datasets import BaseDatasetDB
from waterdip.server.db.models.models import (
    BaseModelDB,
    BaseModelVersionDB,
    ModelVersionSchemaInDB,
)
from waterdip.server.db.mongodb import (
    MONGO_COLLECTION_BATCH_ROWS,
    MONGO_COLLECTION_DATASETS,
    MONGO_COLLECTION_EVENT_ROWS,
    MONGO_COLLECTION_MODEL_VERSIONS,
    MONGO_COLLECTION_MODELS,
)

PSI_TEST_MODEL_ID = "1d195bf6-7a1f-4a33-b7b1-37a603aadd44"
PSI_TEST_MODEL_VERSION_ID = "1d195bf6-7a1f-4a33-b7b1-37a603aadd44"
PSI_TEST_MODEL_VERSION_NAME = "v1"
DATASET_BATCH_ID_V3_1 = "1d195bf6-7a1f-4a33-b7b1-37a603aadd44"
DATASET_EVENT_ID_V1 = "1d195bf6-7a1f-4a33-b7b1-37a603aadd44"

model = BaseModelDB(model_id=UUID(PSI_TEST_MODEL_ID), model_name="test_classification")
model_version = BaseModelVersionDB(
    model_version_id=UUID(PSI_TEST_MODEL_VERSION_ID),
    model_version=PSI_TEST_MODEL_VERSION_NAME,
    model_id=UUID(PSI_TEST_MODEL_ID),
    created_at=datetime(year=2023, month=2, day=10),
    version_schema=ModelVersionSchemaInDB(**METRICS_MODEL_VERSION_V1_SCHEMA),
)
batch_dataset = BaseDatasetDB(
    dataset_id=UUID(DATASET_BATCH_ID_V3_1),
    model_id=UUID(PSI_TEST_MODEL_ID),
    model_version_id=UUID(PSI_TEST_MODEL_VERSION_ID),
    dataset_type=DatasetType.BATCH,
    environment=Environment.TRAINING,
    created_at=datetime(year=2023, month=2, day=10),
)
event_dataset = BaseDatasetDB(
    dataset_id=UUID(DATASET_EVENT_ID_V1),
    model_id=UUID(PSI_TEST_MODEL_ID),
    model_version_id=UUID(PSI_TEST_MODEL_VERSION_ID),
    dataset_type=DatasetType.EVENT,
    environment=Environment.PRODUCTION,
    created_at=datetime(year=2023, month=2, day=10),
)

database = MongodbBackendTesting.get_instance().database
event_collection = database[MONGO_COLLECTION_EVENT_ROWS]
batch_collection = database[MONGO_COLLECTION_BATCH_ROWS]

numeric_columns = ["length", "height"]
categorical_columns = ["cap-shape", "cap-surface", "cap-color", "bruises"]


def setup_module(mocker):
    database[MONGO_COLLECTION_MODELS].insert_many(documents=[model.dict()])
    database[MONGO_COLLECTION_MODEL_VERSIONS].insert_many(
        documents=[model_version.dict()]
    )
    database[MONGO_COLLECTION_DATASETS].insert_many(
        documents=[dataset.dict() for dataset in [batch_dataset, event_dataset]]
    )

    rows, events = [], []
    for i in range(0, len(metrics_batch_data_rows)):
        row = BaseDatasetBatchRowDB(
            model_id=UUID(PSI_TEST_MODEL_ID),
            model_version_id=UUID(PSI_TEST_MODEL_VERSION_ID),
            row_id=uuid.uuid4(),
            dataset_id=UUID(DATASET_BATCH_ID_V3_1),
            columns=[DataColumn(**column) for column in metrics_batch_data_rows[i]],
        )
        rows.append(row)
    for i in range(0, len(metrics_event_rows)):
        event = BaseEventRowDB(
            model_id=UUID(PSI_TEST_MODEL_ID),
            model_version_id=UUID(PSI_TEST_MODEL_VERSION_ID),
            row_id=uuid.uuid4(),
            dataset_id=UUID(DATASET_EVENT_ID_V1),
            columns=[
                EventDataColumnDB(**column)
                for column in metrics_event_rows[i]["columns"]
            ],
            created_at=metrics_event_rows[i]["created_at"],
        )
        events.append(event)
    database[MONGO_COLLECTION_BATCH_ROWS].insert_many(
        documents=[row.dict() for row in rows]
    )
    database[MONGO_COLLECTION_EVENT_ROWS].insert_many(
        documents=[event.dict() for event in events]
    )


def teardown_module():
    clean_model_data(database, model.model_id)


class TestDriftPSIMetrics:
    cls_name = "waterdip.core.metrics.data_metrics.NumericNestedCountDateHistogram.aggregation_result"
    cls_name_1 = (
        "waterdip.core.metrics.data_metrics.NumericCountHistogram.aggregation_result"
    )
    numeric_count_date_histogram_mock_data = {
        "18-12-2022": {"length": {"bins": ["0", "2"], "count": [1.0, 1.0]}},
        "19-12-2022": {"length": {"bins": ["1", "3"], "count": [1.0, 1.0]}},
        "20-12-2022": {"length": {"bins": ["5", "7"], "count": [1.0, 1.0]}},
        "21-12-2022": {"length": {"bins": ["5", "7"], "count": [1.0, 1.0]}},
        "22-12-2022": {"length": {"bins": ["5", "7"], "count": [1.0, 1.0]}},
    }
    numeric_count_histogram_mock_data = {
        "length": {"bins": ["0", "2"], "count": [1.0, 2.0]}
    }

    def test_psi_metrics(self, mocker):
        """
        Doing a patch here as MongoMock does not support $bucketAuto
        """
        mocker.patch(
            self.cls_name, return_value=self.numeric_count_date_histogram_mock_data
        )

        mocker.patch(
            self.cls_name_1,
            return_value=self.numeric_count_histogram_mock_data,
        )
        psi = PSIMetrics(
            collection=event_collection,
            dataset_id=UUID(DATASET_EVENT_ID_V1),
            baseline_dataset_id=UUID(DATASET_BATCH_ID_V3_1),
            baseline_collection=batch_collection,
        )

        psi_result = psi.aggregation_result(
            numeric_columns=numeric_columns,
            categorical_columns=categorical_columns,
            time_range=TimeRange(
                start_time=datetime(year=2022, month=12, day=18),
                end_time=datetime(year=2022, month=12, day=22),
            ),
        )

        assert len(psi_result) == 5
