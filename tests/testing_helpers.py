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

from mongomock.database import Database
from mongomock.mongo_client import MongoClient

from tests.testing_helper_metrics_data import (
    METRICS_DATASET_BATCH_ID_V1_1,
    METRICS_DATASET_EVENT_ID_V1,
    METRICS_MODEL_ID,
    METRICS_MODEL_VERSION_ID_V1,
    METRICS_MODEL_VERSION_ID_V1_NAME,
    METRICS_MODEL_VERSION_V1_SCHEMA,
    metrics_batch_data_rows,
    metrics_event_rows,
)
from waterdip.core.commons.models import DatasetType
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
    MongodbBackend,
)

MODEL_ID = "de6af49c-e80b-4852-b8dd-3b8fdd7f98f8"
MODEL_VERSION_ID_V1 = "1e195bf6-9a3f-4a33-b7b1-37a603aadf41"
MODEL_VERSION_ID_V1_NAME = "v1"
DATASET_EVENT_ID_V1 = "1e195bf6-7a1f-4a33-b7b1-37a603aadde1"
DATASET_BATCH_ID_V1_1 = "1d195bf6-7a1f-4a33-b7b1-37a603aadd31"
DATASET_BATCH_ID_V1_2 = "1d195bf6-7a1f-4a33-b7b1-37a603aadd32"

MODEL_VERSION_ID_V2 = "2e195bf6-9a3f-4a33-b7b1-37a603aadf42"
MODEL_VERSION_ID_V2_NAME = "v2"
DATASET_EVENT_ID_V2 = "2e195bf6-7a1f-4a33-b7b1-37a603aadde2"


MODEL_VERSION_V1_SCHEMA = {
    "features": {
        "f1": {"data_type": "NUMERIC", "list_index": 0},
        "f2": {"data_type": "CATEGORICAL", "list_index": 0},
    },
    "predictions": {"p1": {"data_type": "NUMERIC", "list_index": 0}},
}

MODEL_VERSION_V2_SCHEMA = {
    "features": {
        "f3": {"data_type": "NUMERIC", "list_index": 0},
        "f4": {"data_type": "CATEGORICAL", "list_index": 0},
    },
    "predictions": {"p2": {"data_type": "CATEGORICAL", "list_index": 0}},
}


class MongodbBackendTesting(MongodbBackend):

    _INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls._INSTANCE is None:
            mongo_client = MongoClient()
            cls._INSTANCE = cls(mongo_client=mongo_client)
        return cls._INSTANCE

    def __init__(self, mongo_client: MongoClient):
        super().__init__(mongo_client, "test_wd_mongo_database")
        self._client = mongo_client
        self._database: Database = mongo_client.db
        collections = [
            MONGO_COLLECTION_MODELS,
            MONGO_COLLECTION_MODEL_VERSIONS,
            MONGO_COLLECTION_DATASETS,
            MONGO_COLLECTION_BATCH_ROWS,
            MONGO_COLLECTION_EVENT_ROWS,
        ]
        for collection in collections:
            self._database.create_collection(collection)

        setup_data(self._database)

    @property
    def client(self) -> MongoClient:
        """The pymongo client"""
        return self._client

    @property
    def database(self) -> Database:
        """The mongodb database"""
        return self._database


def setup_data(database):
    setup_model_data(database)
    setup_model_version_data(database)
    setup_dataset_data(database)
    setup_metrics_row(database)
    setup_metrics_event(database)


def setup_model_data(database):
    models = [
        BaseModelDB(model_id=UUID(MODEL_ID), model_name="test_classification"),
        BaseModelDB(model_id=UUID(METRICS_MODEL_ID), model_name="metrics_test"),
    ]

    database[MONGO_COLLECTION_MODELS].insert_many(
        documents=[model.dict() for model in models]
    )


def setup_model_version_data(database):
    versions = [
        BaseModelVersionDB(
            model_version_id=UUID(MODEL_VERSION_ID_V1),
            model_version=MODEL_VERSION_ID_V1_NAME,
            model_id=UUID(MODEL_ID),
            created_at=datetime(year=2022, month=11, day=17),
            version_schema=ModelVersionSchemaInDB(**MODEL_VERSION_V1_SCHEMA),
        ),
        BaseModelVersionDB(
            model_version_id=UUID(MODEL_VERSION_ID_V2),
            model_version=MODEL_VERSION_ID_V2_NAME,
            model_id=UUID(MODEL_ID),
            created_at=datetime(year=2022, month=11, day=18),
            version_schema=ModelVersionSchemaInDB(**MODEL_VERSION_V2_SCHEMA),
        ),
        BaseModelVersionDB(
            model_version_id=UUID(METRICS_MODEL_VERSION_ID_V1),
            model_version=METRICS_MODEL_VERSION_ID_V1_NAME,
            model_id=UUID(METRICS_MODEL_ID),
            created_at=datetime(year=2022, month=12, day=28),
            version_schema=ModelVersionSchemaInDB(**METRICS_MODEL_VERSION_V1_SCHEMA),
        ),
    ]

    database[MONGO_COLLECTION_MODEL_VERSIONS].insert_many(
        documents=[version.dict() for version in versions]
    )


def setup_dataset_data(database):
    datasets = [
        BaseDatasetDB(
            dataset_id=UUID(DATASET_BATCH_ID_V1_1),
            model_id=UUID(MODEL_ID),
            model_version_id=UUID(MODEL_VERSION_ID_V1),
            dataset_type=DatasetType.BATCH,
            dataset_name="V1_training",
            environment="training",
            created_at=datetime(year=2022, month=11, day=17),
        ),
        BaseDatasetDB(
            dataset_id=UUID(DATASET_BATCH_ID_V1_2),
            model_id=UUID(MODEL_ID),
            model_version_id=UUID(MODEL_VERSION_ID_V1),
            dataset_type=DatasetType.BATCH,
            dataset_name="V1_validation",
            environment="validation",
            created_at=datetime(year=2022, month=11, day=18),
        ),
        BaseDatasetDB(
            dataset_id=UUID(DATASET_EVENT_ID_V1),
            model_id=UUID(MODEL_ID),
            model_version_id=UUID(MODEL_VERSION_ID_V1),
            dataset_type=DatasetType.EVENT,
            dataset_name="V1_production",
            environment="production",
            created_at=datetime(year=2022, month=11, day=17),
        ),
        BaseDatasetDB(
            dataset_id=UUID(DATASET_EVENT_ID_V2),
            model_id=UUID(MODEL_ID),
            model_version_id=UUID(MODEL_VERSION_ID_V2),
            dataset_type=DatasetType.EVENT,
            dataset_name="V2_production",
            environment="production",
            created_at=datetime(year=2022, month=11, day=17),
        ),
        BaseDatasetDB(
            dataset_id=UUID(METRICS_DATASET_BATCH_ID_V1_1),
            model_id=UUID(METRICS_MODEL_ID),
            model_version_id=UUID(METRICS_MODEL_VERSION_ID_V1),
            dataset_type=DatasetType.BATCH,
            dataset_name="V1_validation",
            environment="validation",
            created_at=datetime(year=2022, month=12, day=28),
        ),
        BaseDatasetDB(
            dataset_id=UUID(METRICS_DATASET_EVENT_ID_V1),
            model_id=UUID(METRICS_MODEL_ID),
            model_version_id=UUID(METRICS_MODEL_VERSION_ID_V1),
            dataset_type=DatasetType.EVENT,
            dataset_name="V1_production",
            environment="production",
            created_at=datetime(year=2022, month=12, day=28),
        ),
    ]
    database[MONGO_COLLECTION_DATASETS].insert_many(
        documents=[dataset.dict() for dataset in datasets]
    )


def setup_metrics_row(database):
    rows = []
    for i in range(0, len(metrics_batch_data_rows)):
        row = BaseDatasetBatchRowDB(
            model_id=METRICS_MODEL_ID,
            model_version_id=METRICS_MODEL_VERSION_ID_V1,
            row_id=uuid.uuid4(),
            dataset_id=UUID(METRICS_DATASET_BATCH_ID_V1_1),
            columns=[DataColumn(**column) for column in metrics_batch_data_rows[i]],
        )
        rows.append(row)

    database[MONGO_COLLECTION_BATCH_ROWS].insert_many(
        documents=[row.dict() for row in rows]
    )


def setup_metrics_event(database):
    events = []
    for i in range(0, len(metrics_event_rows)):
        event = BaseEventRowDB(
            model_id=METRICS_MODEL_ID,
            model_version_id=METRICS_MODEL_VERSION_ID_V1,
            row_id=uuid.uuid4(),
            dataset_id=UUID(METRICS_DATASET_EVENT_ID_V1),
            columns=[
                EventDataColumnDB(**column)
                for column in metrics_event_rows[i]["columns"]
            ],
            created_at=datetime.fromisoformat(metrics_event_rows[i]["created_at"]),
        )
        events.append(event)

    database[MONGO_COLLECTION_EVENT_ROWS].insert_many(
        documents=[event.dict() for event in events]
    )


def clean_model_data(db, model_id):
    c_model = db["wd_models"]
    c_model_version = db["wd_model_versions"]
    c_dataset = db["wd_datasets"]
    c_events = db["wd_dataset_event_rows"]
    c_batch = db["wd_dataset_batch_rows"]

    c_batch.delete_many(filter={"model_id": model_id})
    c_events.delete_many(filter={"model_id": model_id})
    c_dataset.delete_many(filter={"model_id": model_id})
    c_model_version.delete_many(filter={"model_id": model_id})
    c_model.delete_many(filter={"model_id": model_id})
