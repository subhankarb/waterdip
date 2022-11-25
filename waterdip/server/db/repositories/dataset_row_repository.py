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

#   Copyright 2022-present, the Waterdip Labs Pvt. Ltd.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from typing import List

from fastapi import Depends

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

    def inset_rows(self, rows: List[BaseEventRowDB]):
        created_rows = self._mongo.database[MONGO_COLLECTION_EVENT_ROWS].insert_many(
            [row.dict() for row in rows]
        )
        return created_rows.inserted_ids


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
