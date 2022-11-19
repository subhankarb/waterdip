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

from typing import Optional
from uuid import UUID

from fastapi import Depends

from waterdip.server.db.models.models import (
    BaseModelDB,
    BaseModelVersionDB,
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

    def find_by_id(self, model_version_id: UUID) -> Optional[BaseModelVersionDB]:
        result = self._mongo.database[MONGO_COLLECTION_MODEL_VERSIONS].find_one(
            {"model_version_id": str(model_version_id)}
        )

        if not result:
            return None

        return BaseModelVersionDB(**result)
