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
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends

from waterdip.server.apis.models.datasets import DatasetListResponse, DatasetListRow
from waterdip.server.apis.models.params import RequestPagination, RequestSort
from waterdip.server.db.models.datasets import DatasetDB
from waterdip.server.services.dataset_service import DatasetService

router = APIRouter()


@router.get(
    "/list.datasets",
    name="dataset:list",
    response_model=DatasetListResponse,
    response_model_exclude_none=True,
)
def get_dataset_list(
    model_version_id: UUID,
    pagination: RequestPagination = Depends(),
    sort: RequestSort = Depends(),
    service: DatasetService = Depends(DatasetService.get_instance),
):

    list_dataset: tuple[List[DatasetDB], int] = service.list_dataset(
        model_version_id=model_version_id, pagination=pagination, sort_request=sort
    )
    response = DatasetListResponse(
        dataset_list=[
            DatasetListRow(
                dataset_id=data_set.dataset_id, dataset_name=data_set.dataset_name
            )
            for data_set in list_dataset[0]
        ],
        meta={
            "page": pagination.page,
            "limit": pagination.limit,
            "total": list_dataset[1],
        },
    )
    return response
