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

from uuid import UUID

from fastapi import APIRouter, Depends

from waterdip.core.commons.models import TimeRange
from waterdip.server.apis.models.metrics import DatasetMetricsResponse
from waterdip.server.apis.models.params import TimeRangeParam
from waterdip.server.services.metrics_service import DatasetMetricsService

router = APIRouter()


@router.get(
    "/metrics.dataset", response_model=DatasetMetricsResponse, name="metrics:dataset"
)
def model_list(
    model_id: UUID,
    model_version_id: UUID,
    dataset_id: UUID,
    time_range_param: TimeRangeParam = Depends(),
    service: DatasetMetricsService = Depends(DatasetMetricsService.get_instance),
):
    time_range = TimeRange(
        start_time=time_range_param.start_time, end_time=time_range_param.end_time
    )

    metrics: DatasetMetricsResponse = service.combined_metrics(
        model_id=model_id,
        model_version_id=model_version_id,
        dataset_id=dataset_id,
        time_range=time_range,
    )

    return metrics
