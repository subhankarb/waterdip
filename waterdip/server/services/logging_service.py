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

from waterdip.core.commons.models import ColumnDataType, ColumnMappingType
from waterdip.server.db.models.dataset_rows import (
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
    features: Dict[str, Union[str, float, int, bool, None]]
    predictions: Dict[str, Union[str, float, int, bool, None]]


@dataclass
class ServiceLogEvent:
    features: Dict[str, Union[str, float, int, bool, None]]
    predictions: Dict[str, Union[str, float, int, bool, None]]
    actuals: Optional[Dict[str, Union[str, float, int, bool, None]]] = None
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None


class BatchLoggingService:
    """
    Batch Logging service prepare the batch logged data to be persisted in DB

    """

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
        """
        Converts API logged column to db DataColumn
        If column type is CATEGORICAL then column value added to value_categorical key
        If column type is NUMERIC then column value added to value_numeric key

        """
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
        """
        Converts API logged row to db Dataset Row.
        The method takes ServiceLogRow as inout and converts each column using _data_column_converter
        """
        converted_columns: List[DataColumn] = []
        all_columns = {
            ColumnMappingType.FEATURE: row.features,
            ColumnMappingType.PREDICTION: row.predictions,
        }
        for mapping_type, columns in all_columns.items():
            for name, data in columns.items():
                # get schema details based on the column name
                schema_details: ModelVersionSchemaFieldDetails = (
                    schema.features.get(name)
                    if mapping_type == ColumnMappingType.FEATURE
                    else schema.predictions.get(name)
                )
                # Converts the column
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
        """
        log method creates a new dataset and converts log rows to db compatible rows.

        Parameters
        ----------
        model_version_id : UUID, optional
            Model Version ID
        environment: str
            Name of the Environment
        rows: List[ServiceLogRow]
            Logged rows
        Returns
        -------
        Number of rows inserted: int
        """
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
    def _convert_event_column(
        column_name: str,
        column_value: Union[str, float, int, bool, None],
        field_schema: ModelVersionSchemaFieldDetails,
        column_mapping_type: ColumnMappingType,
    ) -> EventDataColumnDB:
        """
        Converts API logged event column to db data format
        If column type is CATEGORICAL then column value added to value_categorical key
        If column type is NUMERIC then column value added to value_numeric key
        """
        if field_schema.data_type == ColumnDataType.CATEGORICAL:
            _column = EventDataColumnDB(
                name=column_name,
                value_categorical=str(column_value)
                if column_value is not None
                else None,
                data_type=field_schema.data_type,
                mapping_type=column_mapping_type,
            )
            return _column
        elif field_schema.data_type == ColumnDataType.NUMERIC:
            _column = EventDataColumnDB(
                name=column_name,
                value_numeric=float(column_value) if column_value is not None else None,
                data_type=field_schema.data_type,
                mapping_type=column_mapping_type,
            )
            return _column

    def _convert_features(
        self,
        features: Dict[str, Union[str, float, int, bool, None]],
        version_schema: ModelVersionSchemaInDB,
    ):
        """
        Re-format only feature columns to DB data format
        """
        converted_columns: List[EventDataColumnDB] = []
        for feature_name, feature_data in features.items():
            schema_details: ModelVersionSchemaFieldDetails = (
                version_schema.features.get(feature_name)
            )
            converted_columns.append(
                self._convert_event_column(
                    feature_name,
                    feature_data,
                    schema_details,
                    ColumnMappingType.FEATURE,
                )
            )
        return converted_columns

    def _convert_classification_predictions(
        self,
        predictions: Dict[str, Union[str, float, int, bool, None]],
        version_schema: ModelVersionSchemaInDB,
    ):
        """
        Re-format only prediction columns to DB data format
        Prediction_cf list gets created. It holds the target column data.
        The item of the list get inserted at the index number provided by the model schema
        """
        converted_columns: List[EventDataColumnDB] = []
        prediction_cf: List = [None] * len(version_schema.predictions.keys())
        for prediction_name, prediction_data in predictions.items():
            schema_details: ModelVersionSchemaFieldDetails = (
                version_schema.predictions.get(prediction_name)
            )
            converted_columns.append(
                self._convert_event_column(
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
        """
        Re-format actual columns to DB data format
        actual_cf list gets created. It holds the actual column data.
        The item of the list get inserted at the index number provided by the model schema.
        The index number is the link between prediction value and the actual
        value for multiclass multilabel classification

        For example:
        prediction_cf = ["yellow", "false"]
        actual_cf = ["red", "false"]
        Both the items in the 0th position represents 1st label.
        Item in the 1st position represents 2nd label.

        """
        converted_columns: List[EventDataColumnDB] = []
        actual_cf: List = [None] * len(version_schema.predictions.keys())
        is_match = None

        for actual_name, actual_data in actuals.items():
            schema_details: ModelVersionSchemaFieldDetails = (
                version_schema.predictions.get(actual_name)
            )
            converted_columns.append(
                self._convert_event_column(
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
        """ """
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

    @staticmethod
    def _event_timestamp(event: ServiceLogEvent, log_timestamp: datetime = None):
        """
        The timestamp hierarchy:
            1. Time provided with each event gets the highest priority
            2. Time provided with the event log gets next priority
            3. If no time is provided, then current UTC time will be generated
        """
        if event.timestamp is not None:
            timestamp = event.timestamp
        elif log_timestamp is not None:
            timestamp = log_timestamp
        else:
            timestamp = datetime.utcnow()

        return timestamp

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
                timestamp=self._event_timestamp(event, log_timestamp),
                version_schema=model_version.version_schema,
            )
            events_row_db.append(event_db)

        return self._row_service.insert_rows(rows=events_row_db)
