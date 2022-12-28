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
from typing import List, Optional, TypeVar
from uuid import UUID

from fastapi import Depends
from pydantic import Field

from waterdip.server.apis.models.params import RequestPagination, RequestSort
from waterdip.server.commons.models import DatasetType
from waterdip.server.db.models.datasets import BaseDatasetDB, DatasetDB
from waterdip.server.db.repositories.dataset_repository import DatasetRepository
from waterdip.server.db.repositories.model_repository import ModelVersionRepository
from waterdip.server.errors.base_errors import EntityNotFoundError


class ServiceBaseDataset(BaseDatasetDB):
    pass


ServiceDataset = TypeVar("ServiceDataset", bound=ServiceBaseDataset)


class ServiceBatchDataset(ServiceBaseDataset):
    dataset_type: DatasetType = Field(default=DatasetType.BATCH, const=True)


class ServiceEventDataset(ServiceBaseDataset):
    dataset_type: DatasetType = Field(default=DatasetType.EVENT, const=True)


class DatasetService:
    _INSTANCE: "DatasetService" = None

    @classmethod
    def get_instance(
        cls,
        repository: DatasetRepository = Depends(DatasetRepository.get_instance),
        model_version_repository: ModelVersionRepository = Depends(
            ModelVersionRepository.get_instance
        ),
    ):
        if not cls._INSTANCE:
            cls._INSTANCE = cls(
                repository=repository, model_version_repository=model_version_repository
            )
        return cls._INSTANCE

    def __init__(
        self,
        repository: DatasetRepository,
        model_version_repository: ModelVersionRepository,
    ):
        self._repository = repository
        self._model_version_repository = model_version_repository

    def list_dataset(
        self,
        model_version_id: UUID,
        sort_request: Optional[RequestSort] = None,
        pagination: Optional[RequestPagination] = None,
    ):
        filters = (
            {"model_version_id": str(model_version_id)}
            if model_version_id is not None
            else {}
        )

        dataset_list: List[DatasetDB] = self._repository.find_datasets(
            filters=filters,
            sort=[(sort_request.get_sort_field, sort_request.get_sort_order)]
            if sort_request and sort_request.sort
            else [("created_at", -1)],
            skip=(pagination.page - 1) * pagination.limit if pagination else 0,
            limit=pagination.limit if pagination else 10,
        )
        count_dataset = self._repository.count_dataset(filters=filters)

        return dataset_list, count_dataset

    def create_batch_dataset(self, dataset: ServiceBatchDataset) -> ServiceBatchDataset:
        model_version = self._model_version_repository.find_by_id(
            dataset.model_version_id
        )

        if model_version is None:
            raise EntityNotFoundError(
                name=str(dataset.model_version_id), type="Model Version"
            )

        return self._repository.create_dataset(dataset=dataset)

    def create_event_dataset(self, dataset: ServiceEventDataset) -> ServiceEventDataset:
        model_version = self._model_version_repository.find_by_id(
            dataset.model_version_id
        )

        if model_version is None:
            raise EntityNotFoundError(
                name=str(dataset.model_version_id), type="Model Version"
            )

        return self._repository.create_dataset(dataset=dataset)

    def find_event_dataset_by_model_version_id(
        self, model_version_id: UUID
    ) -> DatasetDB:
        filters = {"model_version_id": str(model_version_id), "dataset_type": "EVENT"}

        dataset_list: List[DatasetDB] = self._repository.find_datasets(filters=filters)

        if len(dataset_list) == 0:
            raise EntityNotFoundError(name=str(model_version_id), type="Event Dataset")

        return dataset_list[0]

    def find_dataset_by_id(self, dataset_id: UUID) -> DatasetDB:
        filters = {"dataset_id": str(dataset_id)}
        dataset_list: List[DatasetDB] = self._repository.find_datasets(filters=filters)

        if len(dataset_list) == 0:
            raise EntityNotFoundError(name=str(dataset_id), type="Dataset")

        return dataset_list[0]
