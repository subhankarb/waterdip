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

from uuid import UUID

from fastapi import Depends

from waterdip.core.metrics.batch_dataset import HistogramCategoricalFeatures
from waterdip.server.db.repositories.dataset_metrics import (
    BatchDatasetMetricsRepository,
)


class BatchDatasetMetricsService:

    _INSTANCE: "BatchDatasetMetricsService" = None

    @classmethod
    def get_instance(
        cls,
        repository: BatchDatasetMetricsRepository = Depends(
            BatchDatasetMetricsRepository.get_instance
        ),
    ):
        if not cls._INSTANCE:
            cls._INSTANCE = cls(repository=repository)
        return cls._INSTANCE

    def __init__(
        self,
        repository: BatchDatasetMetricsRepository,
    ):
        self._repository = repository

    def histogram_categorical_features(self, dataset_id: UUID):
        hist_categorical = HistogramCategoricalFeatures(
            collection=self._repository.collection, dataset_id=dataset_id
        )
        return hist_categorical.aggregation_result()
