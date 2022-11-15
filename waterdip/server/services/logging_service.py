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
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Union
from uuid import UUID

from fastapi import Depends

from waterdip.server.commons.models import ColumnDataType, ColumnMappingType
from waterdip.server.db.models.dataset_rows import DataColumn, DatasetBatchRowDB
from waterdip.server.db.models.models import (
    ModelVersionDB,
    ModelVersionSchemaFieldDetails,
    ModelVersionSchemaInDB,
)
from waterdip.server.services.dataset_service import DatasetService, ServiceBatchDataset
from waterdip.server.services.model_service import ModelVersionService
from waterdip.server.services.row_service import (
    BatchDatasetRowService,
    ServiceDatasetBatchRow,
)


@dataclass
class ServiceLogRow:
    features: Dict[str, Union[str, float, int, bool]]
    predictions: Dict[str, Union[str, float, int, bool]]


class BatchLoggingService:
    _INSTANCE: "BatchLoggingService" = None

    @classmethod
    def get_instance(
        cls,
        model_version_service: ModelVersionService = Depends(
            ModelVersionService.get_instance
        ),
        dataset_service: DatasetService = Depends(DatasetService.get_instance),
        row_service: BatchDatasetRowService = Depends(
            BatchDatasetRowService.get_instance
        ),
    ):
        if not cls._INSTANCE:
            cls._INSTANCE = cls(
                model_version_service=model_version_service,
                dataset_service=dataset_service,
                row_service=row_service,
            )
        return cls._INSTANCE

    def __init__(
        self,
        model_version_service: ModelVersionService,
        dataset_service: DatasetService,
        row_service: BatchDatasetRowService,
    ):
        self._model_version_service = model_version_service
        self._dataset_service = dataset_service
        self._row_service = row_service

    @staticmethod
    def _data_column_converter(
        column_name: str,
        column_value: Union[str, float, int, bool],
        field_schema: ModelVersionSchemaFieldDetails,
        column_mapping_type: ColumnMappingType,
    ) -> DataColumn:
        if field_schema.data_type == ColumnDataType.CATEGORICAL:
            _column = DataColumn(
                name=column_name,
                value_categorical=str(column_value),
                data_type=field_schema.data_type,
                mapping_type=column_mapping_type,
            )
            return _column
        elif field_schema.data_type == ColumnDataType.NUMERIC:
            _column = DataColumn(
                name=column_name,
                value_numeric=float(column_value),
                data_type=field_schema.data_type,
                mapping_type=column_mapping_type,
            )
            return _column

    def _log_row_to_batch_row_db_converter(
        self, dataset_id: UUID, row: ServiceLogRow, schema: ModelVersionSchemaInDB
    ) -> ServiceDatasetBatchRow:
        columns: List[DataColumn] = []
        for feature_name, feature_data in row.features.items():
            schema_details: ModelVersionSchemaFieldDetails = schema.features.get(
                feature_name
            )
            columns.append(
                self._data_column_converter(
                    column_name=feature_name,
                    column_value=feature_data,
                    field_schema=schema_details,
                    column_mapping_type=ColumnMappingType.FEATURE,
                )
            )
        for prediction_name, prediction_data in row.predictions.items():
            schema_details: ModelVersionSchemaFieldDetails = schema.predictions.get(
                prediction_name
            )
            columns.append(
                self._data_column_converter(
                    column_name=prediction_name,
                    column_value=prediction_data,
                    field_schema=schema_details,
                    column_mapping_type=ColumnMappingType.FEATURE,
                )
            )
        return ServiceDatasetBatchRow(
            row_id=uuid.uuid4(),
            dataset_id=dataset_id,
            columns=columns,
            created_at=datetime.utcnow(),
        )

    def log(
        self, model_version_id: UUID, environment: str, rows: List[ServiceLogRow]
    ) -> int:
        model_version: ModelVersionDB = self._model_version_service.find_by_id(
            model_version_id=model_version_id
        )
        dataset_id = uuid.uuid4()
        dataset = ServiceBatchDataset(
            dataset_id=dataset_id,
            dataset_name=f"{model_version.model_version}_{environment}",
            created_at=datetime.utcnow(),
            model_id=model_version.model_id,
            model_version_id=model_version_id,
            environment=environment,
        )

        self._dataset_service.create_batch_dataset(dataset=dataset)
        data_rows_in_db: List[DatasetBatchRowDB] = [
            self._log_row_to_batch_row_db_converter(
                dataset_id=dataset_id, row=row, schema=model_version.version_schema
            )
            for row in rows
        ]
        return self._row_service.insert_rows(data_rows_in_db)
