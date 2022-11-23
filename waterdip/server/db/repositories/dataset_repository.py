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

from typing import Dict, List

from fastapi import Depends

from waterdip.server.db.models.datasets import BaseDatasetDB, DatasetDB
from waterdip.server.db.mongodb import MONGO_COLLECTION_DATASETS, MongodbBackend


class DatasetRepository:

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

    def create_dataset(self, dataset: DatasetDB) -> DatasetDB:
        inserted_dataset = self._mongo.database[MONGO_COLLECTION_DATASETS].insert_one(
            document=dataset.dict()
        )
        created_dataset = self._mongo.database[MONGO_COLLECTION_DATASETS].find_one(
            {"_id": inserted_dataset.inserted_id}
        )
        return BaseDatasetDB(**created_dataset)

    def find_datasets(
        self,
        filters: Dict,
        sort: List = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[DatasetDB]:
        result = (
            self._mongo.database[MONGO_COLLECTION_DATASETS]
            .find(filters)
            .limit(limit)
            .skip(skip)
        )
        if sort:
            result = result.sort(sort)

        return [BaseDatasetDB(**dataset) for dataset in result]

    def count_dataset(self, filters: Dict) -> int:
        total = self._mongo.database[MONGO_COLLECTION_DATASETS].count_documents(
            filter=filters
        )
        return total
