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
from typing import Literal, Optional

from fastapi import Depends

from waterdip.server.apis.models.models import ModelVersionSchema
from waterdip.server.db.models.models import (
    BaseModelDB,
    BaseModelVersionDB,
    ModelDB,
    ModelVersionDB,
    ModelVersionSchemaFieldDetails,
    ModelVersionSchemaInDB,
)
from waterdip.server.db.repositories.model_repository import (
    ModelRepository,
    ModelVersionRepository,
)
from waterdip.server.errors.base_errors import EntityNotFoundError
from waterdip.server.services.dataset_service import DatasetService, ServiceEventDataset


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
        dataset_service: DatasetService = Depends(DatasetService.get_instance),
    ):
        if not cls._INSTANCE:
            cls._INSTANCE = cls(repository=repository, dataset_service=dataset_service)
        return cls._INSTANCE

    def __init__(
        self, repository: ModelVersionRepository, dataset_service: DatasetService
    ):
        self._repository = repository
        self._dataset_service = dataset_service

    def find_by_id(self, model_version_id: uuid.UUID) -> Optional[ModelVersionDB]:
        found_model_version = self._repository.find_by_id(
            model_version_id=model_version_id
        )

        if not found_model_version:
            raise EntityNotFoundError(name=str(model_version_id), type="Model Version")

        return found_model_version

    @staticmethod
    def _schema_conversion(
        version_schema: ModelVersionSchema,
        schema_type: Literal["features", "predictions"] = "features",
    ):
        schema, index = {}, 0
        schema_value_dict = (
            version_schema.features
            if schema_type == "features"
            else version_schema.predictions
        )
        for k, v in schema_value_dict.items():
            schema[k] = ModelVersionSchemaFieldDetails(
                data_type=v.value, list_index=index
            )
            index = index + 1
        return schema

    def register_model_version(
        self,
        model_id: uuid.UUID,
        model_version: str,
        version_schema: ModelVersionSchema,
    ) -> ModelVersionDB:

        model_version_id, serving_dataset_id = uuid.uuid4(), uuid.uuid4()

        event_dataset = ServiceEventDataset(
            dataset_id=serving_dataset_id,
            dataset_name=f"{model_version}_serving",
            created_at=datetime.utcnow(),
            model_id=model_id,
            model_version_id=model_version_id,
            environment="PRODUCTION",
        )
        self._dataset_service.create_event_dataset(event_dataset)

        model_version_db = BaseModelVersionDB(
            model_id=model_id,
            model_version_id=model_version_id,
            model_version=model_version,
            created_at=datetime.utcnow(),
            version_schema=ModelVersionSchemaInDB(
                features=self._schema_conversion(version_schema, "features"),
                predictions=self._schema_conversion(version_schema, "predictions"),
            ),
        )

        return self._repository.register_model_version(model_version_db)
