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
import functools
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Union
from uuid import UUID

from fastapi import Depends

from waterdip.server.commons.models import ColumnDataType, ColumnMappingType
from waterdip.server.db.models.dataset_rows import (
    BaseClassificationEventRowDB,
    DataColumn,
    DatasetBatchRowDB,
    EventDataColumnDB,
)
from waterdip.server.db.models.datasets import DatasetDB
from waterdip.server.db.models.models import (
    BaseModelVersionDB,
    ModelVersionSchemaFieldDetails,
    ModelVersionSchemaInDB,
)
from waterdip.server.services.dataset_service import DatasetService, ServiceBatchDataset
from waterdip.server.services.model_service import ModelVersionService
from waterdip.server.services.row_service import (
    BatchDatasetRowService,
    EventDatasetRowService,
    ServiceClassificationEventRow,
    ServiceDatasetBatchRow,
)


@dataclass
class ServiceLogRow:
    features: Dict[str, Union[str, float, int, bool]]
    predictions: Dict[str, Union[str, float, int, bool]]


@dataclass
class ServiceLogEvent:
    features: Dict[str, Union[str, float, int, bool]]
    predictions: Dict[str, Union[str, float, int, bool]]
    actuals: Optional[Dict[str, Union[str, float, int, bool]]] = None
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None


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
        self,
        dataset_id: UUID,
        row: ServiceLogRow,
        schema: ModelVersionSchemaInDB,
        model_id: UUID,
        model_version_id: UUID,
    ) -> ServiceDatasetBatchRow:
        converted_columns: List[DataColumn] = []
        all_columns = {
            ColumnMappingType.FEATURE: row.features,
            ColumnMappingType.PREDICTION: row.predictions,
        }
        for mapping_type, columns in all_columns.items():
            for name, data in columns.items():
                schema_details: ModelVersionSchemaFieldDetails = (
                    schema.features.get(name)
                    if mapping_type == ColumnMappingType.FEATURE
                    else schema.predictions.get(name)
                )
                converted_columns.append(
                    self._data_column_converter(
                        column_name=name,
                        column_value=data,
                        field_schema=schema_details,
                        column_mapping_type=mapping_type,
                    )
                )

        return ServiceDatasetBatchRow(
            model_id=model_id,
            model_version_id=model_version_id,
            row_id=uuid.uuid4(),
            dataset_id=dataset_id,
            columns=converted_columns,
            created_at=datetime.utcnow(),
        )

    def log(
        self, model_version_id: UUID, environment: str, rows: List[ServiceLogRow]
    ) -> int:
        model_version: BaseModelVersionDB = self._model_version_service.find_by_id(
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
                dataset_id=dataset_id,
                row=row,
                schema=model_version.version_schema,
                model_id=model_version.model_id,
                model_version_id=model_version_id,
            )
            for row in rows
        ]
        return self._row_service.insert_rows(data_rows_in_db)


class EventLoggingService:
    _INSTANCE: "EventLoggingService" = None

    @classmethod
    def get_instance(
        cls,
        model_version_service: ModelVersionService = Depends(
            ModelVersionService.get_instance
        ),
        dataset_service: DatasetService = Depends(DatasetService.get_instance),
        row_service: EventDatasetRowService = Depends(
            EventDatasetRowService.get_instance
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
        row_service: EventDatasetRowService,
    ):
        self._model_version_service = model_version_service
        self._dataset_service = dataset_service
        self._row_service = row_service

    @staticmethod
    def _event_column(
        column_name: str,
        column_value: Union[str, float, int, bool],
        field_schema: ModelVersionSchemaFieldDetails,
        column_mapping_type: ColumnMappingType,
    ) -> EventDataColumnDB:
        if field_schema.data_type == ColumnDataType.CATEGORICAL:
            _column = EventDataColumnDB(
                name=column_name,
                value_categorical=str(column_value),
                column_data_type=field_schema.data_type,
                column_mapping_type=column_mapping_type,
            )
            return _column
        elif field_schema.data_type == ColumnDataType.NUMERIC:
            _column = EventDataColumnDB(
                name=column_name,
                value_numeric=float(column_value),
                column_data_type=field_schema.data_type,
                column_mapping_type=column_mapping_type,
            )
            return _column

    def _convert_features(
        self,
        features: Dict[str, Union[str, float, int, bool]],
        version_schema: ModelVersionSchemaInDB,
    ):
        converted_columns: List[EventDataColumnDB] = []
        for feature_name, feature_data in features.items():
            schema_details: ModelVersionSchemaFieldDetails = (
                version_schema.features.get(feature_name)
            )
            converted_columns.append(
                self._event_column(
                    feature_name,
                    feature_data,
                    schema_details,
                    ColumnMappingType.FEATURE,
                )
            )
        return converted_columns

    def _convert_classification_predictions(
        self,
        predictions: Dict[str, Union[str, float, int, bool]],
        version_schema: ModelVersionSchemaInDB,
    ):
        converted_columns: List[EventDataColumnDB] = []
        prediction_cf: List = [None] * len(version_schema.predictions.keys())
        for prediction_name, prediction_data in predictions.items():
            schema_details: ModelVersionSchemaFieldDetails = (
                version_schema.predictions.get(prediction_name)
            )
            converted_columns.append(
                self._event_column(
                    prediction_name,
                    prediction_data,
                    schema_details,
                    ColumnMappingType.FEATURE,
                )
            )
            prediction_cf[schema_details.list_index] = (
                str(prediction_data)
                if schema_details.data_type == ColumnDataType.CATEGORICAL
                else float(prediction_data)
            )

        return converted_columns, prediction_cf

    def _convert_classification_actuals(
        self,
        actuals: Dict[str, Union[str, float, int, bool]],
        version_schema: ModelVersionSchemaInDB,
        prediction_cf: List,
    ):
        converted_columns: List[EventDataColumnDB] = []
        actual_cf: List = [None] * len(version_schema.predictions.keys())
        is_match = None

        for actual_name, actual_data in actuals.items():
            schema_details: ModelVersionSchemaFieldDetails = (
                version_schema.predictions.get(actual_name)
            )
            converted_columns.append(
                self._event_column(
                    actual_name, actual_data, schema_details, ColumnMappingType.ACTUAL
                )
            )
            actual_cf[schema_details.list_index] = (
                str(actual_data)
                if schema_details.data_type == ColumnDataType.CATEGORICAL
                else float(actual_data)
            )

        is_match = (
            True
            if functools.reduce(
                lambda x, y: x and y,
                map(lambda p, q: p == q, prediction_cf, actual_cf),
                True,
            )
            else False
        )
        return converted_columns, actual_cf, is_match

    def _convert_classification_event(
        self,
        model_id: UUID,
        model_version_id: UUID,
        dataset_id: UUID,
        event: ServiceLogEvent,
        timestamp: datetime,
        version_schema: ModelVersionSchemaInDB,
    ) -> ServiceClassificationEventRow:
        converted_features = self._convert_features(event.features, version_schema)
        converted_predictions, prediction_cf = self._convert_classification_predictions(
            event.predictions, version_schema
        )
        converted_actuals, actual_cf, is_match = [], None, None

        if event.actuals:
            (
                converted_actuals,
                actual_cf,
                is_match,
            ) = self._convert_classification_actuals(
                event.predictions, version_schema, prediction_cf
            )

        return ServiceClassificationEventRow(
            model_id=model_id,
            model_version_id=model_version_id,
            event_id=event.event_id if event.event_id else str(uuid.uuid4()),
            row_id=uuid.uuid4(),
            dataset_id=dataset_id,
            columns=converted_features + converted_predictions + converted_actuals,
            prediction_cf=prediction_cf,
            actual_cf=actual_cf,
            created_at=timestamp,
            is_match=is_match,
        )

    def log(
        self,
        model_version_id: UUID,
        events: List[ServiceLogEvent],
        log_timestamp: datetime = None,
    ) -> int:

        model_version: BaseModelVersionDB = self._model_version_service.find_by_id(
            model_version_id=model_version_id
        )
        event_dataset: DatasetDB = (
            self._dataset_service.find_event_dataset_by_model_version_id(
                model_version_id=model_version_id
            )
        )

        events_row_db: List[ServiceClassificationEventRow] = []
        for event in events:
            event_db = self._convert_classification_event(
                model_id=model_version.model_id,
                model_version_id=model_version_id,
                dataset_id=event_dataset.dataset_id,
                event=event,
                timestamp=log_timestamp if log_timestamp else datetime.utcnow(),
                version_schema=model_version.version_schema,
            )
            events_row_db.append(event_db)

        return self._row_service.insert_rows(rows=events_row_db)
