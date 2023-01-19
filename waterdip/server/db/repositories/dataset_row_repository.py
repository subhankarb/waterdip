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

from datetime import date, datetime
from typing import Dict, List

from fastapi import Depends
from pymongo.collection import Collection

from waterdip.server.db.models.dataset_rows import BaseDatasetBatchRowDB, BaseEventRowDB
from waterdip.server.db.mongodb import (
    MONGO_COLLECTION_BATCH_ROWS,
    MONGO_COLLECTION_EVENT_ROWS,
    MongodbBackend,
)


class EventDatasetRowRepository:

    _INSTANCE: "EventDatasetRowRepository" = None

    @classmethod
    def get_instance(
        cls, mongodb: MongodbBackend = Depends(MongodbBackend.get_instance)
    ):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls(mongodb=mongodb)
        return cls._INSTANCE

    def __init__(self, mongodb: MongodbBackend):
        self._mongo = mongodb

    @property
    def collection(self) -> Collection:
        return self._mongo.database[MONGO_COLLECTION_EVENT_ROWS]

    def inset_rows(self, rows: List[BaseEventRowDB]):
        created_rows = self._mongo.database[MONGO_COLLECTION_EVENT_ROWS].insert_many(
            [row.dict() for row in rows]
        )
        return created_rows.inserted_ids

    def count_prediction_by_model_id(self, model_id: str):
        return self._mongo.database[MONGO_COLLECTION_EVENT_ROWS].count_documents(
            {"model_id": model_id}
        )

    def find_last_prediction_date(self, model_id: str):
        last_row = self._mongo.database[MONGO_COLLECTION_EVENT_ROWS].find_one(
            {"model_id": model_id}, sort=[("created_at", -1)]
        )
        return last_row["created_at"] if last_row else None

    def find_first_prediction_date(self, model_id: str) -> datetime:
        first_pred = self._mongo.database[MONGO_COLLECTION_EVENT_ROWS].find_one(
            {"model_id": model_id}, sort=[("created_at", 1)]
        )
        return first_pred["created_at"] if first_pred else None

    def agg_prediction(self, agg_prediction_pipeline: list):
        return self._mongo.database[MONGO_COLLECTION_EVENT_ROWS].aggregate(
            pipeline=agg_prediction_pipeline
        )

    def prediction_count(self, filter: Dict):
        return self._mongo.database[MONGO_COLLECTION_EVENT_ROWS].count_documents(
            filter=filter
        )

    def delete_rows_by_model_id(self, model_id: str):
        return self._mongo.database[MONGO_COLLECTION_EVENT_ROWS].delete_many(
            {"model_id": model_id}
        )


class BatchDatasetRowRepository:

    _INSTANCE = None

    @classmethod
    def get_instance(
        cls, mongodb: MongodbBackend = Depends(MongodbBackend.get_instance)
    ):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls(mongodb=mongodb)
        return cls._INSTANCE

    def __init__(self, mongodb: MongodbBackend):
        self._mongo = mongodb

    @property
    def collection(self) -> Collection:
        return self._mongo.database[MONGO_COLLECTION_BATCH_ROWS]

    def inset_row(self, row: BaseDatasetBatchRowDB):
        created_row = self._mongo.database[MONGO_COLLECTION_BATCH_ROWS].insert_one(
            row.dict()
        )
        return created_row.inserted_id

    def inset_rows(self, rows: List[BaseDatasetBatchRowDB]):
        created_rows = self._mongo.database[MONGO_COLLECTION_BATCH_ROWS].insert_many(
            [row.dict() for row in rows]
        )
        return created_rows.inserted_ids

    def agg_rows(self, agg_pipeline: List[Dict]):
        return self._mongo.database[MONGO_COLLECTION_BATCH_ROWS].aggregate(
            pipeline=agg_pipeline
        )

    def delete_rows_by_model_id(self, model_id: str):
        return self._mongo.database[MONGO_COLLECTION_BATCH_ROWS].delete_many(
            {"model_id": model_id}
        )
