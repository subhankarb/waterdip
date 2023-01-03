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
from enum import Enum
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, root_validator


class MonitorType(str, Enum):
    """
    Monitor types of the model

    Attributes:
    ------------------
    DATA_QUALITY:
    DRIFT:
    MODEL_PERFORMANCE:
    """

    DATA_QUALITY = "DATA_QUALITY"
    DRIFT = "DRIFT"
    PERFORMANCE = "PERFORMANCE"


class DriftMetric(str, Enum):
    PSI = "PSI"


class DataQualityMetric(str, Enum):
    MISSING_VALUE = "MISSING_VALUE"
    EMPTY_VALUE = "EMPTY_VALUE"
    NEW_VALUE = "NEW_VALUE"


class PerformanceMetric(str, Enum):
    PRECISION = "PRECISION"
    RECALL = "RECALL"
    F1 = "F1"


class TimeRange(BaseModel):
    """
    Attributes:
    ------------------
    start_time:
        start time of the time range
    model_version:
        end time of the time range
    """

    start_time: datetime
    end_time: datetime


class MovingTimeWindow(BaseModel):
    skip_period: str = Field(description="", default="1d")
    time_period: str = Field(description="15d", default="15d")
    aggregation_period: str = Field(default="1d")


class FixedTimeWindow(BaseModel):
    start_time: datetime = Field(...)
    end_time: datetime = Field(...)
    aggregation_period: str = Field(default="1d")


class ModelBaseline(BaseModel):
    dataset_id: Optional[UUID] = Field(description="dataset id", default=None)
    time_window: Optional[Union[MovingTimeWindow, FixedTimeWindow]] = Field(
        default=MovingTimeWindow()
    )

    @root_validator
    def any_of(cls, v):
        if not any(v.values()):
            raise ValueError("one of dataset_id or time_window must have a value")
        return v


class Histogram(BaseModel):
    bins: List[str]
    val: List[Union[float, int]]


class DateHistogram(BaseModel):
    date_bins: List[datetime]
    val: List[Union[float, int]]


class PredictionTaskType(str, Enum):
    """
    prediction task type for any model version.

    Attributes:
    ------------------
    BINARY:
        Binary Classification
    MULTI_CLASS:
        Multi Class Classification

    """

    BINARY = "BINARY"
    MULTI_CLASS = "MULTICLASS"


class DatasetType(str, Enum):
    """
    dataset type of the datasets associated to model versions

    Attributes:
    ------------------
    BATCH:
        One time uploaded dataset. It is a non-time series dataset
    """

    BATCH = "BATCH"
    EVENT = "EVENT"


class ColumnDataType(str, Enum):
    """
    data type of the dataset

    Attributes:
    ------------------
    NUMERIC:
        numeric data type. It can be integer or float
    CATEGORICAL:
        categorical data type can take on one of a limited,
        and usually fixed, number of possible values
    BOOLEAN:
        boolean data type, i.e. True or False

    """

    NUMERIC = "NUMERIC"
    CATEGORICAL = "CATEGORICAL"
    BOOLEAN = "BOOLEAN"


class ColumnMappingType(str, Enum):
    """
    mapping of column type to model version schema.

    Attributes:
    ------------------
    FEATURE:
        column type is a feature input type
    PREDICTION:
        column type is a prediction output type
    PREDICTION_SCORE:
        column type is a prediction score type
    ACTUAL:
        column type is an actual type. Actual is realized and final output
    ACTUAL_SCORE:
        column type is an actual score.


    """

    FEATURE = "FEATURE"
    PREDICTION = "PREDICTION"
    PREDICTION_SCORE = "PREDICTION_SCORE"
    ACTUAL = "ACTUAL"
    ACTUAL_SCORE = "ACTUAL_SCORE"
