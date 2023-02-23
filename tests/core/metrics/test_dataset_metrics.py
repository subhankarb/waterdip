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

from tests.testing_helpers import (
    DATASET_EVENT_ID_V2,
    MODEL_ID,
    MODEL_VERSION_ID_V2,
    MongodbBackendTesting,
)
from waterdip.core.commons.models import DatasetType, Environment, TimeRange
from waterdip.core.metrics.data_metrics import (
    CardinalityCategorical,
    CategoricalCountHistogram,
    CountEmptyHistogram,
    NumericBasicMetrics,
    NumericCountHistogram,
    NumericNestedCountDateHistogram,
)
from waterdip.server.db.models.dataset_rows import (
    BaseDatasetBatchRowDB,
    BaseEventRowDB,
    DataColumn,
    EventDataColumnDB,
)
from waterdip.server.db.models.datasets import BaseDatasetDB
from waterdip.server.db.mongodb import (
    MONGO_COLLECTION_BATCH_ROWS,
    MONGO_COLLECTION_DATASETS,
    MONGO_COLLECTION_EVENT_ROWS,
    MONGO_COLLECTION_MODEL_VERSIONS,
)

DATASET_BATCH_ID_V2_3 = "1d195bf6-7a1f-4a33-b7b1-37a603aadd33"

batch_dataset = BaseDatasetDB(
    dataset_id=UUID(DATASET_BATCH_ID_V2_3),
    model_id=UUID(MODEL_ID),
    model_version_id=UUID(MODEL_VERSION_ID_V2),
    dataset_type=DatasetType.BATCH,
    dataset_name="V2_validation",
    environment=Environment.VALIDATION,
    created_at=datetime(year=2022, month=11, day=17),
)
database = MongodbBackendTesting.get_instance().database

event_rows = [
    {
        "created_at": datetime(year=2022, month=12, day=23),
        "columns": [
            {
                "name": "f3",
                "value_numeric": None,
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
    },
    {
        "created_at": datetime(year=2022, month=12, day=22),
        "columns": [
            {
                "name": "f3",
                "value_numeric": 2,
                "data_type": "NUMERIC",
                "mapping_type": "FEATURE",
            },
            {
                "name": "f4",
                "value_categorical": None,
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
    },
    {
        "created_at": datetime(year=2022, month=12, day=21),
        "columns": [
            {
                "name": "f3",
                "value_numeric": 0,
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
    },
    {
        "created_at": datetime(year=2022, month=12, day=20),
        "columns": [
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
    },
]

batch_data_rows = [
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
    rows, events = [], []
    for i in range(0, len(batch_data_rows)):
        row = BaseDatasetBatchRowDB(
            model_id=MODEL_ID,
            model_version_id=MODEL_VERSION_ID_V2,
            row_id=uuid.uuid4(),
            dataset_id=UUID(DATASET_BATCH_ID_V2_3),
            columns=[DataColumn(**column) for column in batch_data_rows[i]],
        )
        rows.append(row)
    for i in range(0, len(event_rows)):
        event = BaseEventRowDB(
            model_id=MODEL_ID,
            model_version_id=MODEL_VERSION_ID_V2,
            row_id=uuid.uuid4(),
            dataset_id=UUID(DATASET_EVENT_ID_V2),
            columns=[
                EventDataColumnDB(**column) for column in event_rows[i]["columns"]
            ],
            created_at=event_rows[i]["created_at"],
        )
        events.append(event)
    database[MONGO_COLLECTION_BATCH_ROWS].insert_many(
        documents=[row.dict() for row in rows]
    )
    database[MONGO_COLLECTION_EVENT_ROWS].insert_many(
        documents=[event.dict() for event in events]
    )


def teardown_module():
    database[MONGO_COLLECTION_MODEL_VERSIONS].delete_one(
        filter={"dataset_id": DATASET_BATCH_ID_V2_3}
    )
    database[MONGO_COLLECTION_BATCH_ROWS].delete_one(
        filter={"dataset_id": DATASET_BATCH_ID_V2_3}
    )


class TestHistogramCategoricalFeatures:
    def test_should_get_histogram_for_categorical_columns(self):
        hist = CategoricalCountHistogram(
            collection=database[MONGO_COLLECTION_BATCH_ROWS],
            dataset_id=UUID(DATASET_BATCH_ID_V2_3),
        )
        hist_result = hist.aggregation_result()
        f4 = hist_result["f4"]

        assert len(f4["bins"]) == 2
        assert max(f4["count"]) == 2

    def test_should_apply_date_filter(self):
        hist = CategoricalCountHistogram(
            collection=database[MONGO_COLLECTION_EVENT_ROWS],
            dataset_id=UUID(DATASET_EVENT_ID_V2),
        )
        hist_result = hist.aggregation_result(
            time_range=TimeRange(
                start_time=datetime(year=2022, month=12, day=22),
                end_time=datetime(year=2022, month=12, day=22),
            )
        )
        assert len(hist_result.items()) == 1


class TestCountEmptyHistogram:
    def test_should_return_null_columns(self):
        hist = CountEmptyHistogram(
            collection=database[MONGO_COLLECTION_EVENT_ROWS],
            dataset_id=UUID(DATASET_EVENT_ID_V2),
        )
        hist_result = hist.aggregation_result(
            time_range=TimeRange(
                start_time=datetime(year=2022, month=12, day=18),
                end_time=datetime(year=2022, month=12, day=23),
            )
        )

        assert hist_result["f3"]["empty_count"] == 1
        assert hist_result["f3"]["empty_percentage"] == 25.0
        assert hist_result["p2"]["empty_count"] == 0


class TestCardinalityCategorical:
    def test_should_return_cardinality_of_categorical_columns(self):
        cardinality = CardinalityCategorical(
            collection=database[MONGO_COLLECTION_EVENT_ROWS],
            dataset_id=UUID(DATASET_EVENT_ID_V2),
        )
        cardinality_result = cardinality.aggregation_result(
            time_range=TimeRange(
                start_time=datetime(year=2022, month=12, day=18),
                end_time=datetime(year=2022, month=12, day=23),
            )
        )
        assert cardinality_result["f4"]["top_value"] == "yellow"


class TestNumericBasicMetrics:
    def test_should_return_basic_numeric_values(self):
        numeric_basic = NumericBasicMetrics(
            collection=database[MONGO_COLLECTION_EVENT_ROWS],
            dataset_id=UUID(DATASET_EVENT_ID_V2),
        )
        numeric_basic_result = numeric_basic.aggregation_result(
            time_range=TimeRange(
                start_time=datetime(year=2022, month=12, day=18),
                end_time=datetime(year=2022, month=12, day=23),
            ),
            std_dev_disable="true",
        )
        assert numeric_basic_result["f3"]["min"] == 0
        assert numeric_basic_result["f3"]["zeros"] == 1


class TestNumericCountHistogram:
    def test_should_return_numeric_count_histogram(self, mocker):
        """
        Doing a patch here as MongoMock does not support $bucketAuto
        """
        mocker.patch(
            "waterdip.core.metrics.data_metrics.NumericCountHistogram.aggregation_result",
            return_value={"f3": {"bins": ["0", "2"], "count": [1.0, 1.0]}},
        )
        numeric_basic = NumericCountHistogram(
            collection=database[MONGO_COLLECTION_EVENT_ROWS],
            dataset_id=UUID(DATASET_EVENT_ID_V2),
        )
        numeric_basic_result = numeric_basic.aggregation_result(
            time_range=TimeRange(
                start_time=datetime(year=2022, month=12, day=18),
                end_time=datetime(year=2022, month=12, day=23),
            ),
            numeric_columns=["f3"],
        )
        assert numeric_basic_result["f3"]["bins"] == ["0", "2"]


class TestNumericNestedCountDateHistogram:
    def test_should_agg_facet_data(self):
        facets = {
            "09-02-2023:c1": [
                {"_id": {"min": 18, "max": 34}, "count": 21},
            ],
            "09-02-2023:c2": [
                {"_id": {"min": 1, "max": 7}, "count": 3},
                {"_id": {"min": 7, "max": 14}, "count": 2},
                {"_id": {"min": 14, "max": 21}, "count": 20},
                {"_id": {"min": 21, "max": 28}, "count": 22},
            ],
        }
        agg_data = NumericNestedCountDateHistogram._facet_to_date_agg(facets=facets)

        assert len(agg_data.keys()) == 1
        assert len(agg_data["09-02-2023"].keys()) == 2
        assert len(agg_data["09-02-2023"]["c1"]) == 1
        assert len(agg_data["09-02-2023"]["c2"]) == 4
        assert agg_data["09-02-2023"]["c1"][0]["count"] == 21

    def test_should_return_numeric_count_histogram_agg_result(self, mocker):
        mocker.patch(
            "waterdip.core.metrics.data_metrics.NumericNestedCountDateHistogram._get_mongo_response",
            return_value={
                "09-02-2023:c1": [
                    {"_id": {"min": 18, "max": 34}, "count": 21},
                ],
                "09-02-2023:c2": [
                    {"_id": {"min": 1, "max": 7}, "count": 3},
                    {"_id": {"min": 7, "max": 14}, "count": 2},
                    {"_id": {"min": 14, "max": 21}, "count": 20},
                    {"_id": {"min": 21, "max": 28}, "count": 22},
                ],
            },
        )
        numeric_basic = NumericNestedCountDateHistogram(
            collection=database[MONGO_COLLECTION_EVENT_ROWS],
            dataset_id=UUID(DATASET_EVENT_ID_V2),
        )
        numeric_basic_result = numeric_basic.aggregation_result(
            time_range=TimeRange(
                start_time=datetime(year=2022, month=12, day=18),
                end_time=datetime(year=2022, month=12, day=23),
            ),
            numeric_columns=["f3"],
        )

        assert list(numeric_basic_result.keys()) == ["09-02-2023"]

        assert list(numeric_basic_result["09-02-2023"].keys()) == ["c1", "c2"]

    def test_should_return_numeric_count_histogram(self, mocker):
        """
        Doing a patch here as MongoMock does not support $bucketAuto
        """
        mocker.patch(
            "waterdip.core.metrics.data_metrics.NumericNestedCountDateHistogram.aggregation_result",
            return_value={
                "18-12-2022": {"f3": {"bins": ["0", "2"], "count": [1.0, 1.0]}},
                "19-12-2022": {"f3": {"bins": ["1", "3"], "count": [1.0, 1.0]}},
                "20-12-2022": {"f3": {"bins": ["5", "7"], "count": [1.0, 1.0]}},
                "21-12-2022": {"f3": {"bins": ["5", "7"], "count": [1.0, 1.0]}},
                "22-12-2022": {"f3": {"bins": ["5", "7"], "count": [1.0, 1.0]}},
            },
        )
        numeric_basic = NumericNestedCountDateHistogram(
            collection=database[MONGO_COLLECTION_EVENT_ROWS],
            dataset_id=UUID(DATASET_EVENT_ID_V2),
        )
        numeric_basic_result = numeric_basic.aggregation_result(
            time_range=TimeRange(
                start_time=datetime(year=2022, month=12, day=18),
                end_time=datetime(year=2022, month=12, day=23),
            ),
            numeric_columns=["f3"],
        )
        assert numeric_basic_result["18-12-2022"]["f3"]["bins"] == ["0", "2"]
