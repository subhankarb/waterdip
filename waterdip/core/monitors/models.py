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

try:
    from typing import Literal, TypeVar
except ImportError:
    from typing_extensions import Literal

from typing import List, Optional, Union

from pydantic import BaseModel, Field, validator

from waterdip.core.commons.models import (
    DataQualityMetric,
    DriftMetric,
    ModelBaseline,
    PerformanceMetric,
)


class MonitorThreshold(BaseModel):
    threshold: Literal["gt", "lt"] = Field(description="greater than or less than")
    value: float = Field(...)


class MonitorDimensions(BaseModel):
    features: Optional[List[str]] = Field(
        description="""
        List of feature fields this monitor monitors. Example: ["feature1", "feature2"...].
        In some cases this list can be really long as a monitor can monitors all the features of a model
    """,
        default=None,
    )
    predictions: Optional[List[str]] = Field(
        description="""
        List of prediction fields this monitor monitors. Example: ["pred1", "pred2"...].
    """,
        default=None,
    )

    @validator("predictions", always=True)
    def check_one_must_field(cls, predictions, values):
        if not values.get("features") and not predictions:
            raise ValueError("Either features or predictions is required")
        return predictions


class BaseMonitorCondition(BaseModel):
    evaluation_metric: Union[DriftMetric, DataQualityMetric, PerformanceMetric] = Field(
        description="Focal is the time window"
    )
    dimensions: Optional[MonitorDimensions] = Field(default=None)
    threshold: MonitorThreshold = Field(...)

    baseline: Optional[ModelBaseline] = Field(default=None)
    evaluation_window: Optional[str] = Field(
        default="1d", description="evaluation_window is the time window example: 1d, 2d"
    )
    skip_period: Optional[str] = Field(
        default="1d",
        description="",
    )

    @staticmethod
    def day_validator(value):
        if len(value) < 2:
            raise ValueError("evaluation_window must be of >= 2")
        no_of_days, day_unit = value[:-1], value[-1]
        if day_unit != "d":
            raise ValueError("evaluation_window value must end with d")
        if not no_of_days.isnumeric():
            raise ValueError("number of days must be numeric")

    @validator("evaluation_window", allow_reuse=True)
    def evaluation_window_validator(cls, value):
        if value == "0":
            return value
        else:
            cls.day_validator(value)
        return value

    @validator("skip_period", allow_reuse=True)
    def evaluation_window_validator(cls, value):
        cls.day_validator(value)
        return value


MonitorCondition = TypeVar("MonitorCondition", bound=BaseMonitorCondition)


class DataQualityBaseMonitorCondition(BaseMonitorCondition):
    evaluation_metric: DataQualityMetric = Field(description="Focal is the time window")
    dimensions: MonitorDimensions = Field(...)


class PerformanceBaseMonitorCondition(BaseMonitorCondition):
    evaluation_metric: PerformanceMetric = Field(description="Focal is the time window")


class DriftBaseMonitorCondition(BaseMonitorCondition):
    evaluation_metric: DriftMetric = Field(description="Focal is the time window")
    dimensions: MonitorDimensions = Field(...)
    baseline: ModelBaseline = Field(...)
