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
import json
from typing import Dict, List
from uuid import UUID

from fastapi import Depends, HTTPException

from waterdip.core.commons.models import (
    ColumnDataType,
    DatasetType,
    Histogram,
    TimeRange,
)
from waterdip.core.metrics.classification_metrics import (
    ClassificationDateHistogramDBMetrics,
)
from waterdip.core.metrics.data_metrics import (
    CardinalityCategorical,
    CategoricalCountHistogram,
    CountEmptyHistogram,
    NumericBasicMetrics,
    NumericCountHistogram,
)
from waterdip.server.apis.models.metrics import (
    CategoricalColumnStats,
    DatasetMetricsResponse,
    NumericColumnStats,
)
from waterdip.server.commons.config import settings
from waterdip.server.db.models.models import ModelVersionSchemaInDB
from waterdip.server.db.repositories.dataset_row_repository import (
    BatchDatasetRowRepository,
    EventDatasetRowRepository,
)
from waterdip.server.services.dataset_service import DatasetService
from waterdip.server.services.model_service import ModelService, ModelVersionService


class DatasetMetricsService:
    _INSTANCE: "DatasetMetricsService" = None

    @classmethod
    def get_instance(
        cls,
        event_repo: EventDatasetRowRepository = Depends(
            EventDatasetRowRepository.get_instance
        ),
        batch_repo: BatchDatasetRowRepository = Depends(
            BatchDatasetRowRepository.get_instance
        ),
        dataset_service: DatasetService = Depends(DatasetService.get_instance),
        model_version_service: ModelVersionService = Depends(
            ModelVersionService.get_instance
        ),
    ):
        if not cls._INSTANCE:
            cls._INSTANCE = cls(
                event_repo=event_repo,
                batch_repo=batch_repo,
                dataset_service=dataset_service,
                model_version_service=model_version_service,
            )
        return cls._INSTANCE

    def __init__(
        self,
        event_repo: EventDatasetRowRepository,
        batch_repo: BatchDatasetRowRepository,
        dataset_service: DatasetService,
        model_version_service: ModelVersionService,
    ):
        self._event_repo = event_repo
        self._batch_repo = batch_repo
        self._dataset_service = dataset_service
        self._model_version_service = model_version_service

    def numeric_basic_metrics(
        self, dataset_id: UUID, dataset_type: DatasetType, time_range: TimeRange = None
    ) -> Dict[str, Dict]:
        if dataset_type == DatasetType.BATCH:
            basic_metrics = NumericBasicMetrics(
                collection=self._batch_repo.collection,
                dataset_id=dataset_id,
            )
            columns = basic_metrics.aggregation_result(
                std_dev_disable=settings.is_testing
            )
        else:
            basic_metrics = NumericBasicMetrics(
                collection=self._event_repo.collection, dataset_id=dataset_id
            )
            columns = basic_metrics.aggregation_result(
                time_range=time_range, std_dev_disable=settings.is_testing
            )

        return columns

    def empty_histogram(
        self, dataset_id: UUID, dataset_type: DatasetType, time_range: TimeRange = None
    ) -> Dict[str, Dict]:
        if dataset_type == DatasetType.BATCH:
            hist_empty = CountEmptyHistogram(
                collection=self._batch_repo.collection, dataset_id=dataset_id
            )
            columns = hist_empty.aggregation_result()
        else:
            hist_empty = CountEmptyHistogram(
                collection=self._event_repo.collection, dataset_id=dataset_id
            )
            columns = hist_empty.aggregation_result(time_range=time_range)

        column_empty_histogram: Dict[str, Dict] = {}

        for column_name, empty_value in columns.items():
            column_empty_histogram[column_name] = {
                "missing_total": empty_value["empty_count"],
                "missing_percentage": empty_value["empty_percentage"],
            }
        return column_empty_histogram

    def numeric_count_histogram(
        self,
        dataset_id: UUID,
        dataset_type: DatasetType,
        numeric_columns: list,
        time_range: TimeRange = None,
    ) -> Dict[str, Histogram]:
        column_histograms: Dict[str, Histogram] = {}
        if len(numeric_columns) > 0:
            if dataset_type == DatasetType.BATCH:
                hist_categorical = NumericCountHistogram(
                    collection=self._batch_repo.collection, dataset_id=dataset_id
                )
                columns = hist_categorical.aggregation_result(
                    numeric_columns=numeric_columns
                )
            else:
                hist_categorical = NumericCountHistogram(
                    collection=self._event_repo.collection, dataset_id=dataset_id
                )
                columns = hist_categorical.aggregation_result(
                    time_range=time_range, numeric_columns=numeric_columns
                )

            for column_name, hist_value in columns.items():
                column_histograms[column_name] = Histogram(
                    bins=hist_value["bins"], val=hist_value["count"]
                )
        return column_histograms

    def categorical_count_histogram(
        self, dataset_id: UUID, dataset_type: DatasetType, time_range: TimeRange = None
    ) -> Dict[str, Histogram]:
        if dataset_type == DatasetType.BATCH:
            hist_categorical = CategoricalCountHistogram(
                collection=self._batch_repo.collection, dataset_id=dataset_id
            )
            columns = hist_categorical.aggregation_result()
        else:
            hist_categorical = CategoricalCountHistogram(
                collection=self._event_repo.collection, dataset_id=dataset_id
            )
            columns = hist_categorical.aggregation_result(time_range=time_range)

        column_histograms: Dict[str, Histogram] = {}

        for column_name, hist_value in columns.items():
            column_histograms[column_name] = Histogram(
                bins=hist_value["bins"], val=hist_value["count"]
            )

        return column_histograms

    def categorical_cardinality(
        self, dataset_id: UUID, dataset_type: DatasetType, time_range: TimeRange = None
    ) -> Dict[str, Dict]:
        if dataset_type == DatasetType.BATCH:
            cardinality = CardinalityCategorical(
                collection=self._batch_repo.collection, dataset_id=dataset_id
            )
            columns = cardinality.aggregation_result()
        else:
            cardinality = CardinalityCategorical(
                collection=self._event_repo.collection, dataset_id=dataset_id
            )
            columns = cardinality.aggregation_result(time_range=time_range)

        column_cardinality: Dict[str, Dict] = {}

        for column_name, cardinal_values in columns.items():
            column_cardinality[column_name] = {
                "unique": cardinal_values["unique_values"],
                "top": cardinal_values["top_value"],
            }
        return column_cardinality

    @staticmethod
    def _get_all_columns(version_schema: ModelVersionSchemaInDB):
        columns = {"CATEGORICAL": {}, "NUMERIC": {}}
        for name, value in version_schema.features.items():
            if value.data_type == ColumnDataType.CATEGORICAL:
                columns["CATEGORICAL"][name] = "features"
            if value.data_type == ColumnDataType.NUMERIC:
                columns["NUMERIC"][name] = "features"
        for name, value in version_schema.predictions.items():
            if value.data_type == ColumnDataType.CATEGORICAL:
                columns["CATEGORICAL"][name] = "predictions"
            if value.data_type == ColumnDataType.NUMERIC:
                columns["NUMERIC"][name] = "predictions"

        return columns

    def combined_metrics(
        self,
        model_id: UUID,
        model_version_id: UUID,
        dataset_id: UUID,
        time_range: TimeRange,
    ) -> DatasetMetricsResponse:
        dataset = self._dataset_service.find_dataset_by_id(dataset_id)

        model_version = self._model_version_service.find_by_id(
            model_version_id=model_version_id
        )

        columns = self._get_all_columns(version_schema=model_version.version_schema)
        params = {
            "dataset_id": dataset_id,
            "time_range": time_range,
            "dataset_type": dataset.dataset_type,
        }
        categorical_count_histogram = self.categorical_count_histogram(**params)
        numeric_count_histogram = self.numeric_count_histogram(
            **{**params, "numeric_columns": columns["NUMERIC"].keys()}
        )

        empty_histogram = self.empty_histogram(**params)
        categorical_cardinality = self.categorical_cardinality(**params)
        numeric_basic_metrics = self.numeric_basic_metrics(**params)

        cat_columns_stats: List[CategoricalColumnStats] = []
        numeric_columns_stats: List[NumericColumnStats] = []

        for categorical_column, mapping in columns["CATEGORICAL"].items():
            count_histogram = categorical_count_histogram.get(categorical_column, None)
            cardinality = categorical_cardinality.get(categorical_column, {})
            empty_values = empty_histogram.get(categorical_column, {})

            cat_column_stats = CategoricalColumnStats(
                column_name=categorical_column,
                histogram=count_histogram,
                unique=cardinality.get("unique", None),
                top=cardinality.get("top", None),
                missing_total=empty_values.get("missing_total", None),
                missing_percentage=empty_values.get("missing_percentage", None),
            )
            cat_columns_stats.append(cat_column_stats)

        for numeric_column, mapping in columns["NUMERIC"].items():
            count_histogram = numeric_count_histogram.get(numeric_column, None)
            empty_values = empty_histogram.get(numeric_column, {})
            numeric_basic_metrics_column = numeric_basic_metrics.get(numeric_column, {})
            numeric_column_stats = NumericColumnStats(
                column_name=numeric_column,
                missing_total=empty_values.get("missing_total", None),
                missing_percentage=empty_values.get("missing_percentage", None),
                mean=numeric_basic_metrics_column.get("avg", None),
                std_dev=numeric_basic_metrics_column.get("std_dev", None),
                variance=numeric_basic_metrics_column.get("variance", None),
                zeros=numeric_basic_metrics_column.get("zeros", 0),
                total=numeric_basic_metrics_column.get("total", None),
                min=numeric_basic_metrics_column.get("min", None),
                max=numeric_basic_metrics_column.get("max", None),
                histogram=count_histogram,
            )
            numeric_columns_stats.append(numeric_column_stats)

        return DatasetMetricsResponse(
            categorical_column_stats=cat_columns_stats,
            numeric_column_stats=numeric_columns_stats,
        )


class ClassificationPerformance:
    _INSTANCE: "ClassificationPerformance" = None

    @classmethod
    def get_instance(
        cls,
        event_repo: EventDatasetRowRepository = Depends(
            EventDatasetRowRepository.get_instance
        ),
        dataset_service: DatasetService = Depends(DatasetService.get_instance),
        model_service: ModelService = Depends(ModelService.get_instance),
    ):
        if not cls._INSTANCE:
            cls._INSTANCE = cls(
                event_repo=event_repo,
                dataset_service=dataset_service,
                model_service=model_service,
            )
        return cls._INSTANCE

    def __init__(
        self,
        event_repo: EventDatasetRowRepository,
        dataset_service: DatasetService,
        model_service: ModelService,
    ):
        self._event_repo = event_repo
        self._dataset_service = dataset_service
        self._model_service = model_service

    def model_performance(
        self, model_id: UUID, model_version_id: UUID, time_range: TimeRange
    ):
        dataset_id = self._dataset_service.find_event_dataset_by_model_version_id(
            model_version_id
        ).dataset_id
        positive_class = self._model_service.find_by_id(model_id).positive_class
        if positive_class is None:
            raise HTTPException(
                status_code=400,
                detail="Positive class is not set for this model",
            )
        hist = ClassificationDateHistogramDBMetrics(
            self._event_repo.collection,
            dataset_id=dataset_id,
            positive_class=positive_class["name"],
        )

        result = hist.aggregation_result(time_range=time_range)
        response = {}
        for key, value in result.items():
            response[key] = []
            for date in value:
                response[key].append({date: value[date]})
            response[key].sort(key=lambda x: list(x.keys())[0])

        output = {}
        for key, value in response.items():
            output[key] = {
                "date": [],
                "value": [],
            }
            for date in value:
                output[key]["date"].append(list(date.keys())[0])
                output[key]["value"].append(list(date.values())[0])

        return output
