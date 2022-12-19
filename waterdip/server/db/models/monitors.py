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
from typing import Dict, List, Optional, TypeVar, Union

from waterdip.server.commons.models import (
    DataQualityMetric,
    DriftMetric,
    MonitorType,
    PerformanceMetric,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from uuid import UUID

from pydantic import BaseModel, Field, validator

from waterdip.server.db.models.models import ModelBaseline


class MonitorThreshold(BaseModel):
    threshold: Literal["gt", "lt"] = Field(description="greater than or less than")
    value: float = Field(...)


class MonitorIdentification(BaseModel):
    model_version_id: UUID = Field(description="")
    model_id: UUID = Field(description="...")


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


class DataQualityBaseMonitorCondition(BaseMonitorCondition):
    evaluation_metric: DataQualityMetric = Field(description="Focal is the time window")
    dimensions: MonitorDimensions = Field(...)


class PerformanceBaseMonitorCondition(BaseMonitorCondition):
    evaluation_metric: PerformanceMetric = Field(description="Focal is the time window")


class DriftBaseMonitorCondition(BaseMonitorCondition):
    evaluation_metric: DriftMetric = Field(description="Focal is the time window")
    dimensions: MonitorDimensions = Field(...)
    baseline: ModelBaseline = Field(...)


class BaseMonitorDB(BaseModel):
    monitor_id: UUID = Field(...)
    monitor_name: str = Field(...)
    monitor_identification: MonitorIdentification = Field(...)
    monitor_type: MonitorType = Field(
        description="Monitor types can be data_drift | prediction_drift"
    )

    monitor_condition: BaseMonitorCondition = Field(...)

    def dict(self, *args, **kwargs) -> "DictStrAny":
        monitor = super().dict(*args, **kwargs)
        monitor["monitor_id"] = str(monitor["monitor_id"])
        monitor["monitor_identification"]["model_version_id"] = str(
            monitor["monitor_identification"]["model_version_id"]
        )
        monitor["monitor_identification"]["model_id"] = str(
            monitor["monitor_identification"]["model_id"]
        )
        return monitor


MonitorDB = TypeVar("MonitorDB", bound=BaseMonitorDB)
