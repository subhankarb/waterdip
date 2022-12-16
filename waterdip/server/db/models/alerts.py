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

from typing import TypeVar
from uuid import UUID

from pydantic import BaseModel, Field

from waterdip.server.commons.models import MonitorType


class AlertIdentification(BaseModel):
    model_version_id: UUID = Field(description="")
    model_id: UUID = Field(description="...")


class BaseAlertDB(BaseModel):
    alert_id: UUID = Field(...)
    monitor_id: str = Field(...)
    alert_identification: AlertIdentification = Field(...)
    alert_type: MonitorType = Field(
        description="Monitor types can be data_drift | prediction_drift"
    )

    def dict(self, *args, **kwargs) -> "DictStrAny":
        alert = super().dict(*args, **kwargs)
        alert["monitor_id"] = str(alert["monitor_id"])
        alert["monitor_identification"]["model_version_id"] = str(
            alert["monitor_identification"]["model_version_id"]
        )
        return alert


AlertDB = TypeVar("AlertDB", bound=BaseAlertDB)
