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

from typing import Dict, List, Optional
from uuid import UUID

import pymongo
from fastapi import Depends

from waterdip.server.db.models.models import (
    BaseModelDB,
    BaseModelVersionDB,
    ModelBaseline,
    ModelDB,
    ModelVersionDB,
)
from waterdip.server.db.mongodb import (
    MONGO_COLLECTION_MODEL_VERSIONS,
    MONGO_COLLECTION_MODELS,
    MongodbBackend,
)


class ModelRepository:
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

    def register_model(self, model: BaseModelDB) -> ModelDB:
        inserted_model = self._mongo.database[MONGO_COLLECTION_MODELS].insert_one(
            document=model.dict()
        )

        created_model = self._mongo.database[MONGO_COLLECTION_MODELS].find_one(
            {"_id": inserted_model.inserted_id}
        )

        return BaseModelDB(**created_model)

    def find_models(
        self,
        filters: Dict,
        sort: List = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[ModelDB]:
        result = (
            self._mongo.database[MONGO_COLLECTION_MODELS]
            .find(filters)
            .limit(limit)
            .skip(skip)
        )
        if sort:
            result = result.sort(sort)

        return [BaseModelDB(**model) for model in result]

    def find_by_id(self, model_id: UUID) -> Optional[ModelDB]:
        result = self._mongo.database[MONGO_COLLECTION_MODELS].find_one(
            {"model_id": str(model_id)}
        )

        if not result:
            return None
        return BaseModelDB(**result)

    def count_models(self, filters: Dict) -> int:
        total = self._mongo.database[MONGO_COLLECTION_MODELS].count_documents(
            filter=filters
        )
        return total

    def delete_model(self, model_id: str) -> None:
        self._mongo.database[MONGO_COLLECTION_MODELS].delete_one(
            {"model_id": str(model_id)}
        )

    def update_model(self, model_id: UUID, updates: Dict) -> ModelDB:
        self._mongo.database[MONGO_COLLECTION_MODELS].update_one(
            {"model_id": str(model_id)},
            {"$set": updates},
        )
        updated_model = self._mongo.database[MONGO_COLLECTION_MODELS].find_one(
            {"model_id": str(model_id)}
        )

        return BaseModelDB(**updated_model)


class ModelVersionRepository:
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

    def register_model_version(self, model: ModelVersionDB) -> ModelVersionDB:
        inserted_model_version = self._mongo.database[
            MONGO_COLLECTION_MODEL_VERSIONS
        ].insert_one(document=model.dict())

        created_model = self._mongo.database[MONGO_COLLECTION_MODEL_VERSIONS].find_one(
            {"_id": inserted_model_version.inserted_id}
        )

        return BaseModelVersionDB(**created_model)

    def find_by_id(self, model_version_id: UUID) -> Optional[ModelVersionDB]:
        result = self._mongo.database[MONGO_COLLECTION_MODEL_VERSIONS].find_one(
            {"model_version_id": str(model_version_id)}
        )

        if not result:
            return None

        return BaseModelVersionDB(**result)

    def find_versions(self, version_filters: Dict) -> List[ModelVersionDB]:
        versions = (
            self._mongo.database[MONGO_COLLECTION_MODEL_VERSIONS]
            .find(version_filters)
            .sort([("created_at", pymongo.DESCENDING)])
        )

        return [BaseModelVersionDB(**version) for version in versions]

    def agg_model_versions_per_model(
        self, model_ids: List[str], top_n=1
    ) -> Dict[str, List[str]]:

        pipeline = [
            {"$match": {"model_id": {"$in": model_ids}}},
            {"$sort": {"created_at": -1}},
            {"$group": {"_id": "$model_id", "docs": {"$push": "$$ROOT"}}},
            {"$project": {"versions": "$docs"}},
        ]

        agg_model_versions: Dict[str, List[str]] = dict()
        for doc in self._mongo.database[MONGO_COLLECTION_MODEL_VERSIONS].aggregate(
            pipeline=pipeline
        ):
            model_id = doc["_id"]
            model_versions = []
            for version in doc["versions"]:
                model_versions.append(
                    [
                        version["model_version_id"],
                        version["model_version"],
                    ]
                )
            agg_model_versions[model_id] = model_versions
        return agg_model_versions

    def delete_versions_by_model_id(self, model_id: str):
        self._mongo.database[MONGO_COLLECTION_MODEL_VERSIONS].delete_many(
            {"model_id": model_id}
        )
