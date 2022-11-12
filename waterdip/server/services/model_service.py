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
from typing import Optional
from uuid import UUID

from fastapi import Depends

from waterdip.server.db.models.models import ModelDB, ModelVersionDB
from waterdip.server.db.repositories.model_repository import (
    ModelRepository,
    ModelVersionRepository,
)
from waterdip.server.errors.base_errors import EntityNotFoundError


class ModelService:

    _INSTANCE: "ModelService" = None

    @classmethod
    def get_instance(
        cls,
        repository: ModelRepository = Depends(ModelRepository.get_instance),
    ):
        if not cls._INSTANCE:
            cls._INSTANCE = cls(repository=repository)
        return cls._INSTANCE

    def __init__(self, repository: ModelRepository):
        self._repository = repository

    def register_model(self, model_name: str) -> ModelDB:
        generated_model_id = uuid.uuid4()
        model_db = BaseModelDB(model_id=generated_model_id, model_name=model_name)

        return self._repository.register_model(model_db)


class ModelVersionService:

    _INSTANCE: "ModelVersionService" = None

    @classmethod
    def get_instance(
        cls,
        repository: ModelVersionRepository = Depends(
            ModelVersionRepository.get_instance
        ),
    ):
        if not cls._INSTANCE:
            cls._INSTANCE = cls(repository=repository)
        return cls._INSTANCE

    def __init__(self, repository: ModelVersionRepository):
        self._repository = repository

    def find_by_id(self, model_version_id: UUID) -> Optional[ModelVersionDB]:
        found_model_version = self._repository.find_by_id(
            model_version_id=model_version_id
        )

        if not found_model_version:
            raise EntityNotFoundError(name=str(model_version_id), type="Model Version")

        return found_model_version
