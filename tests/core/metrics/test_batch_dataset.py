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

from tests.testing_helpers import MODEL_ID, MODEL_VERSION_ID_V2, MongodbBackendTesting
from waterdip.core.metrics.batch_dataset import HistogramCategoricalFeatures
from waterdip.server.commons.models import DatasetType
from waterdip.server.db.models.dataset_rows import BaseDatasetBatchRowDB, DataColumn
from waterdip.server.db.models.datasets import BaseDatasetDB
from waterdip.server.db.mongodb import (
    MONGO_COLLECTION_BATCH_ROWS,
    MONGO_COLLECTION_DATASETS,
    MONGO_COLLECTION_MODEL_VERSIONS,
)

DATASET_BATCH_ID_V2_3 = "1d195bf6-7a1f-4a33-b7b1-37a603aadd33"

batch_dataset = BaseDatasetDB(
    dataset_id=UUID(DATASET_BATCH_ID_V2_3),
    model_id=UUID(MODEL_ID),
    model_version_id=UUID(MODEL_VERSION_ID_V2),
    dataset_type=DatasetType.BATCH,
    dataset_name="V2_validation",
    environment="validation",
    created_at=datetime(year=2022, month=11, day=17),
)
database = MongodbBackendTesting.get_instance().database


data_rows = [
    [
        {
            "name": "f3",
            "value_numeric": 1,
            "data_type": "NUMERIC",
            "mapping_type": "FEATURE",
        },
        {
            "name": "f4",
            "value_categorical": "red",
            "data_type": "CATEGORICAL",
            "mapping_type": "FEATURE",
        },
        {
            "name": "p2",
            "value_categorical": "true",
            "data_type": "CATEGORICAL",
            "mapping_type": "PREDICTION",
        },
    ],
    [
        {
            "name": "f3",
            "value_numeric": 2,
            "data_type": "NUMERIC",
            "mapping_type": "FEATURE",
        },
        {
            "name": "f4",
            "value_categorical": "yellow",
            "data_type": "CATEGORICAL",
            "mapping_type": "FEATURE",
        },
        {
            "name": "p2",
            "value_categorical": "false",
            "data_type": "CATEGORICAL",
            "mapping_type": "PREDICTION",
        },
    ],
    [
        {
            "name": "f3",
            "value_numeric": 30,
            "data_type": "NUMERIC",
            "mapping_type": "FEATURE",
        },
        {
            "name": "f4",
            "value_categorical": "yellow",
            "data_type": "CATEGORICAL",
            "mapping_type": "FEATURE",
        },
        {
            "name": "p2",
            "value_categorical": "false",
            "data_type": "CATEGORICAL",
            "mapping_type": "PREDICTION",
        },
    ],
]


def setup_module():
    database[MONGO_COLLECTION_DATASETS].insert_many(documents=[batch_dataset.dict()])
    rows = []
    for i in range(0, len(data_rows)):
        row = BaseDatasetBatchRowDB(
            model_id = uuid.uuid4(),
            model_version_id = uuid.uuid4(),
            row_id=uuid.uuid4(),
            dataset_id=UUID(DATASET_BATCH_ID_V2_3),
            columns=[DataColumn(**column) for column in data_rows[i]],
        )
        rows.append(row)
    database[MONGO_COLLECTION_BATCH_ROWS].insert_many(
        documents=[row.dict() for row in rows]
    )


def teardown_module():
    print("tearing module test_batch_dataset..")
    database[MONGO_COLLECTION_MODEL_VERSIONS].delete_one(
        filter={"dataset_id": DATASET_BATCH_ID_V2_3}
    )
    database[MONGO_COLLECTION_BATCH_ROWS].delete_one(
        filter={"dataset_id": DATASET_BATCH_ID_V2_3}
    )


class TestHistogramCategoricalFeatures:
    def test_should_get_histogram_for_categorical_columns(self):
        hist = HistogramCategoricalFeatures(
            collection=database[MONGO_COLLECTION_BATCH_ROWS],
            dataset_id=UUID(DATASET_BATCH_ID_V2_3),
        )
        hist_result = hist.aggregation_result()
        f4 = hist_result["f4"]

        assert len(f4["bins"]) == 2
        assert max(f4["count"]) == 2
