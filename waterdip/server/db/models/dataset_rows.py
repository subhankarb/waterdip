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

from datetime import datetime
from typing import Dict, List, Optional, TypeVar, Union
from uuid import UUID

from pydantic import BaseModel

from waterdip.server.commons.models import ColumnDataType, ColumnMappingType


class DataColumn(BaseModel):
    name: str
    value_numeric: Optional[Union[int, float]]
    value_categorical: Optional[str]
    data_type: ColumnDataType
    mapping_type: Optional[ColumnMappingType]


class BaseDatasetBatchRowDB(BaseModel):
    row_id: UUID
    dataset_id: UUID
    columns: List[DataColumn]
    created_at: Optional[datetime]
    meta: Optional[Dict]

    def dict(self, *args, **kwargs) -> "DictStrAny":
        row = super().dict(*args, **kwargs)
        row["dataset_id"] = str(row["dataset_id"])
        row["row_id"] = str(row["row_id"])
        return row


DatasetBatchRowDB = TypeVar("DatasetBatchRowDB", bound=BaseDatasetBatchRowDB)


class EventDataColumnDB(BaseModel):
    name: str
    value: Optional[Union[str, int, float]]
    value_numeric: Optional[Union[int, float]]
    value_categorical: Optional[str]
    column_data_type: ColumnDataType  # Column Type Categorical or Numerical
    column_mapping_type: ColumnMappingType
    column_list_index: Optional[int]


class BaseEventRowDB(BaseModel):
    row_id: UUID
    dataset_id: UUID
    event_id: Optional[str]
    columns: List[EventDataColumnDB]
    created_at: datetime
    meta: Optional[Dict]

    def dict(self, *args, **kwargs) -> "DictStrAny":
        row = super().dict(*args, **kwargs)
        row["row_id"] = str(row["row_id"])
        row["dataset_id"] = str(row["dataset_id"])
        return row


class BaseClassificationEventRowDB(BaseEventRowDB):
    prediction_cf: Optional[List[Union[str, int, float]]]
    actual_cf: Optional[List[Union[str, int, float]]]
    is_match: Optional[Union[bool, None]]


EventRowDB = TypeVar("EventRowDB", bound=BaseEventRowDB)
ClassificationEventRowDB = TypeVar(
    "ClassificationEventRowDB", bound=BaseClassificationEventRowDB
)
