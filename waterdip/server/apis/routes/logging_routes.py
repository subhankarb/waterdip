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

#   Copyright 2022-present, the Waterdip Labs Pvt. Ltd.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from fastapi import APIRouter, Body, Depends

from waterdip.server.apis.models.rows import BatchDatasetLogRequest, EventLogRequest
from waterdip.server.services.logging_service import (
    BatchLoggingService,
    EventLoggingService,
)

router = APIRouter()


@router.post(
    "/log.dataset",
    name="log:dataset",
    response_model_exclude_none=True,
)
def log_batch_dataset(
    request: BatchDatasetLogRequest = Body(
        ...,
    ),
    service: BatchLoggingService = Depends(BatchLoggingService.get_instance),
):
    logged_row_count = service.log(
        model_version_id=request.model_version_id,
        rows=request.rows,
        environment=request.environment,
    )
    return {"total": logged_row_count}


@router.post(
    "/log.events",
    name="log:events",
    response_model_exclude_none=True,
)
def log_events(
    request: EventLogRequest = Body(
        ...,
    ),
    service: EventLoggingService = Depends(EventLoggingService.get_instance),
):
    logged_row_count = service.log(
        model_version_id=request.model_version_id,
        events=request.events,
        log_timestamp=request.timestamp,
    )
    return {"total": logged_row_count}
