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

from fastapi import APIRouter, Body

from waterdip.server.apis.models.monitors import (
    CreateMonitorRequest,
    CreateMonitorResponse,
)
from waterdip.server.commons.models import MonitorType

router = APIRouter()


@router.post(
    "/monitor.create", response_model=CreateMonitorResponse, name="monitor:create"
)
def create_monitor(
    request: CreateMonitorRequest = Body(
        ..., description="the request model register info"
    ),
):
    monitor_type: MonitorType = request.monitor_type

    if monitor_type == MonitorType.DATA_QUALITY:
        print(1)
    elif monitor_type == MonitorType.PERFORMANCE:
        print(2)
    else:
        print(3)
