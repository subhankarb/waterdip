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
from typing import Dict, Optional, TypeVar, Union
from uuid import UUID

from pydantic import BaseModel, Field, root_validator

from waterdip.core.commons.models import ColumnDataType


class BaseModelDB(BaseModel):
    model_id: UUID
    model_name: str
    created_at: Optional[datetime]

    def dict(self, *args, **kwargs) -> "DictStrAny":
        model = super().dict(*args, **kwargs)
        model["model_id"] = str(model["model_id"])
        return model


ModelDB = TypeVar("ModelDB", bound=BaseModelDB)


class MovingTimeWindow(BaseModel):
    """
    Fixed time window.

    Attributes:
    ------------------
    skip_period:
       how many days from current day the window starts
    time_period:
       time in days for the moving time window
    aggregation_period:
       agg period for the time window. Default is 1 day
    """

    skip_period: str = Field(default="1d")
    time_period: str = Field(default="15d")
    aggregation_period: str = Field(default="1d")


class FixedTimeWindow(BaseModel):
    """
    Fixed time window.
    Attributes:
    ------------------
    start_time:
        start time of the time window
    end_time:
        end time of the time window
    aggregation_period:
        agg period for the time window. Default is 1 day
    """

    start_time: datetime = Field(...)
    end_time: datetime = Field(...)
    aggregation_period: str = Field(default="1d")


class ModelBaseline(BaseModel):
    """
    Model baseline.
    Model baseline can either be a batch dataset or a time window.
    Any one of it is mandatory

    Attributes:
    ------------------
    dataset_id:
        batch dataset attached to the version id
    time_window:
        time window for the baseline. Time window can be either FixedTimeWindow or MovingTimeWindow

    """

    dataset_id: Optional[UUID] = Field(description="dataset id", default=None)
    time_window: Optional[Union[MovingTimeWindow, FixedTimeWindow]] = Field(
        default=MovingTimeWindow()
    )

    @root_validator
    def any_of(cls, v):
        if not any(v.values()):
            raise ValueError("one of dataset_id or time_window must have a value")
        return v


class ModelVersionSchemaFieldDetails(BaseModel):
    """
    ModelVersionSchemaFieldDetails entity for schema of Model Version

    Attributes:
    ------------------
    data_type:
        Data type of the column
    list_index: int[Optional]:
        index number of the column if multiple prediction columns are present
        This will be used to link between prediction & prediction score, Actual and Actual Score columns
    """

    data_type: ColumnDataType
    list_index: Optional[
        int
    ]  # Can be used to link between prediction and prediction score columns


class ModelVersionSchemaInDB(BaseModel):
    """
    Model schema for the model version

    Attributes:
    ------------------
    features:
        schema for the feature columns
    predictions:
        schema for the prediction columns
    """

    features: Dict[str, ModelVersionSchemaFieldDetails]
    predictions: Dict[str, ModelVersionSchemaFieldDetails]


class BaseModelVersionDB(BaseModel):
    model_version_id: UUID = Field(default=None)
    model_version: str = Field(default=None)
    model_id: UUID = Field(default=None)
    description: Optional[str] = None
    task_type: Optional[str] = None
    created_at: Optional[datetime] = None
    version_schema: ModelVersionSchemaInDB = Field(
        description="Schema for the model version"
    )
    baseline: ModelBaseline = Field(
        default=ModelBaseline(time_window=MovingTimeWindow())
    )

    def dict(self, *args, **kwargs) -> "DictStrAny":
        model_version = super().dict(*args, **kwargs)
        model_version["model_id"] = str(model_version["model_id"])
        model_version["model_version_id"] = str(model_version["model_version_id"])
        return model_version


ModelVersionDB = TypeVar("ModelVersionDB", bound=BaseModelVersionDB)
