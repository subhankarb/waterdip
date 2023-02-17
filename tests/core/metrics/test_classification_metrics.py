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

from tests.testing_helpers import MongodbBackendTesting, clean_model_data
from waterdip.core.commons.models import DatasetType, Environment, TimeRange
from waterdip.core.metrics.classification_metrics import (
    ClassificationDateHistogramDBMetrics,
)
from waterdip.server.db.models.dataset_rows import (
    BaseClassificationEventRowDB,
    BaseEventRowDB,
    EventDataColumnDB,
)
from waterdip.server.db.models.datasets import BaseDatasetDB
from waterdip.server.db.models.models import (
    BaseModelDB,
    BaseModelVersionDB,
    ModelVersionSchemaInDB,
)
from waterdip.server.db.mongodb import (
    MONGO_COLLECTION_DATASETS,
    MONGO_COLLECTION_EVENT_ROWS,
    MONGO_COLLECTION_MODEL_VERSIONS,
    MONGO_COLLECTION_MODELS,
)

TEST_CLASSIFICATION_MODEL_ID = "4468c560-14d1-47e1-8d68-d4a93e9eb3ed"
TEST_CLASSIFICATION_MODEL_VERSION_ID = "a367b135-06bc-4676-99da-ca5ec4d7f0c0"
TEST_CLASSIFICATION_MODEL_DATASET_ID = "4d32217b-12e1-4458-98e8-8897b6f9823e"
TEST_CLASSIFICATION_MODEL_EVENT_DATASET_ID = "03e8eabc-9d4c-4179-9ea0-66f7d56c19d2"
TEST_CLASSIFICATION_MODEL_DATASET_NAME = "v1"
TEST_CLASSIFICATION_MODEL_VERSION_SCHEMA = {
    "features": {
        "f3": {"data_type": "NUMERIC"},
        "f4": {"data_type": "CATEGORICAL"},
    },
    "predictions": {"p2": {"data_type": "CATEGORICAL", "list_index": 0}},
}
database = MongodbBackendTesting.get_instance().database
cf_model = BaseModelDB(
    model_id=UUID(TEST_CLASSIFICATION_MODEL_ID), model_name="test_classification"
)
cf_model_version = BaseModelVersionDB(
    model_version_id=UUID(TEST_CLASSIFICATION_MODEL_VERSION_ID),
    model_version=TEST_CLASSIFICATION_MODEL_DATASET_NAME,
    model_id=UUID(TEST_CLASSIFICATION_MODEL_ID),
    created_at=datetime(year=2022, month=11, day=17),
    version_schema=ModelVersionSchemaInDB(**TEST_CLASSIFICATION_MODEL_VERSION_SCHEMA),
)
cf_batch_dataset = BaseDatasetDB(
    dataset_id=UUID(TEST_CLASSIFICATION_MODEL_DATASET_ID),
    model_id=UUID(TEST_CLASSIFICATION_MODEL_ID),
    model_version_id=UUID(TEST_CLASSIFICATION_MODEL_VERSION_ID),
    dataset_type=DatasetType.BATCH,
    dataset_name="",
    environment=Environment.TRAINING,
    created_at=datetime(year=2023, month=1, day=11),
)
cf_event_dataset = BaseDatasetDB(
    dataset_id=UUID(TEST_CLASSIFICATION_MODEL_EVENT_DATASET_ID),
    model_id=UUID(TEST_CLASSIFICATION_MODEL_ID),
    model_version_id=UUID(TEST_CLASSIFICATION_MODEL_VERSION_ID),
    dataset_type=DatasetType.EVENT,
    dataset_name="",
    environment=Environment.PRODUCTION,
    created_at=datetime(year=2023, month=1, day=11),
)

event_rows = [
    {
        "created_at": datetime(year=2022, month=12, day=21),
        "columns": [
            {
                "name": "p2",
                "value_categorical": "false",
                "data_type": "CATEGORICAL",
                "mapping_type": "PREDICTION",
            },
            {
                "name": "p2",
                "value_categorical": "true",
                "data_type": "CATEGORICAL",
                "mapping_type": "ACTUAL",
            },
        ],
        "prediction_cf": ["false"],
        "actual_cf": ["true"],
        "is_match": False,
    },
    {
        "created_at": datetime(year=2022, month=12, day=22),
        "columns": [
            {
                "name": "p2",
                "value_categorical": "true",
                "data_type": "CATEGORICAL",
                "mapping_type": "PREDICTION",
            },
            {
                "name": "p2",
                "value_categorical": "true",
                "data_type": "CATEGORICAL",
                "mapping_type": "ACTUAL",
            },
        ],
        "prediction_cf": ["true"],
        "actual_cf": ["true"],
        "is_match": True,
    },
    {
        "created_at": datetime(year=2022, month=12, day=23),
        "columns": [
            {
                "name": "p2",
                "value_categorical": "true",
                "data_type": "CATEGORICAL",
                "mapping_type": "PREDICTION",
            },
            {
                "name": "p2",
                "value_categorical": "true",
                "data_type": "CATEGORICAL",
                "mapping_type": "ACTUAL",
            },
        ],
        "prediction_cf": ["true"],
        "actual_cf": ["true"],
        "is_match": True,
    },
    {
        "created_at": datetime(year=2022, month=12, day=23),
        "columns": [
            {
                "name": "p2",
                "value_categorical": "true",
                "data_type": "CATEGORICAL",
                "mapping_type": "PREDICTION",
            },
            {
                "name": "p2",
                "value_categorical": "false",
                "data_type": "CATEGORICAL",
                "mapping_type": "ACTUAL",
            },
        ],
        "prediction_cf": ["true"],
        "actual_cf": ["false"],
        "is_match": False,
    },
    {
        "created_at": datetime(year=2022, month=12, day=23),
        "columns": [
            {
                "name": "p2",
                "value_categorical": "true",
                "data_type": "CATEGORICAL",
                "mapping_type": "PREDICTION",
            },
            {
                "name": "p2",
                "value_categorical": "false",
                "data_type": "CATEGORICAL",
                "mapping_type": "ACTUAL",
            },
        ],
        "prediction_cf": ["true"],
        "actual_cf": ["false"],
        "is_match": False,
    },
]


def setup_module():
    database[MONGO_COLLECTION_MODELS].insert_one(document=cf_model.dict())
    database[MONGO_COLLECTION_MODEL_VERSIONS].insert_one(
        document=cf_model_version.dict()
    )
    database[MONGO_COLLECTION_DATASETS].insert_many(
        documents=[dataset.dict() for dataset in [cf_batch_dataset, cf_event_dataset]]
    )
    events = []
    for i in range(0, len(event_rows)):
        event = BaseClassificationEventRowDB(
            model_id=UUID(TEST_CLASSIFICATION_MODEL_ID),
            model_version_id=UUID(TEST_CLASSIFICATION_MODEL_VERSION_ID),
            row_id=uuid.uuid4(),
            dataset_id=UUID(TEST_CLASSIFICATION_MODEL_EVENT_DATASET_ID),
            columns=[
                EventDataColumnDB(**column) for column in event_rows[i]["columns"]
            ],
            created_at=event_rows[i]["created_at"],
            prediction_cf=event_rows[i]["prediction_cf"],
            actual_cf=event_rows[i]["actual_cf"],
            is_match=event_rows[i]["is_match"],
        )

        events.append(event)
    database[MONGO_COLLECTION_EVENT_ROWS].insert_many(
        documents=[event.dict() for event in events]
    )


def teardown_module():
    clean_model_data(db=database, model_id=TEST_CLASSIFICATION_MODEL_ID)


class TestClassificationDateHist:
    def test_should_return_classification_metrics(self):
        clf_date_hist = ClassificationDateHistogramDBMetrics(
            collection=database[MONGO_COLLECTION_EVENT_ROWS],
            dataset_id=UUID(TEST_CLASSIFICATION_MODEL_EVENT_DATASET_ID),
            positive_class="true",
        )
        result = clf_date_hist.aggregation_result(
            time_range=TimeRange(
                start_time=datetime(year=2022, month=12, day=23),
                end_time=datetime(year=2022, month=12, day=23),
            )
        )
        assert result["accuracy"]["23-12-2022"] == 0.33

    def test_should_return_classification_metrics_with_time_range(self):
        clf_date_hist = ClassificationDateHistogramDBMetrics(
            collection=database[MONGO_COLLECTION_EVENT_ROWS],
            dataset_id=UUID(TEST_CLASSIFICATION_MODEL_EVENT_DATASET_ID),
            positive_class="true",
        )
        result = clf_date_hist.aggregation_result(
            time_range=TimeRange(
                start_time=datetime(year=2022, month=12, day=21),
                end_time=datetime(year=2022, month=12, day=22),
            )
        )
        assert sorted(list(result["accuracy"].keys())) == ["21-12-2022", "22-12-2022"]
