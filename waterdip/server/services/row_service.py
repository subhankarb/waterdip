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

from typing import List

from fastapi import Depends

from waterdip.server.db.models.dataset_rows import BaseDatasetBatchRowDB
from waterdip.server.db.repositories.dataset_row_repository import (
    BatchDatasetRowRepository,
)


class ServiceDatasetBatchRow(BaseDatasetBatchRowDB):
    pass


class BatchDatasetRowService:

    _INSTANCE: "BatchDatasetRowService" = None

    @classmethod
    def get_instance(
        cls,
        repository: BatchDatasetRowRepository = Depends(
            BatchDatasetRowRepository.get_instance
        ),
    ):
        if not cls._INSTANCE:
            cls._INSTANCE = cls(repository=repository)
        return cls._INSTANCE

    def __init__(self, repository: BatchDatasetRowRepository):
        self._repository = repository

    def insert_rows(self, rows: List[ServiceDatasetBatchRow]) -> int:
        inserted_rows = self._repository.inset_rows(rows)
        return len(inserted_rows)
