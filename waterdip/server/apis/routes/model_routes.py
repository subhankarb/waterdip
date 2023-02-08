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

from fastapi import APIRouter, Body, Depends
from waterdip.server.apis.models.models import (
    ModelInfoResponse,
    ModelListResponse,
    ModelOverviewResponse,
    ModelVersionInfoResponse,
    RegisterModelRequest,
    RegisterModelResponse,
    RegisterModelVersionRequest,
    RegisterModelVersionResponse,
    UpdateModelRequest,
    UpdateModelResponse,
)
from waterdip.server.apis.models.params import (
    RequestPagination,
    RequestSort,
)
from waterdip.server.db.models.datasets import DatasetDB
from waterdip.server.db.models.models import ModelDB, ModelVersionDB
from waterdip.server.services.model_service import ModelService, ModelVersionService

router = APIRouter()


@router.get(
    "/model.overview", response_model=ModelOverviewResponse, name="model:overview"
)
def model_overview(
    model_id: UUID,
    model_service: ModelService = Depends(ModelService.get_instance),
):
    return model_service.model_overview(model_id=model_id)


@router.get("/model.info", response_model=ModelInfoResponse, name="model:info")
def model_info(
    model_id: UUID,
    model_service: ModelService = Depends(ModelService.get_instance),
    model_version_service: ModelVersionService = Depends(
        ModelVersionService.get_instance
    ),
):
    model: ModelDB = model_service.find_by_id(model_id=model_id)
    model_baseline = model.baseline
    versions = model_version_service.find_all_versions_for_model(
        model_id=model_id)
    return ModelInfoResponse(
        model_id=model.model_id, model_name=model.model_name, model_versions=versions, model_baseline=model_baseline,
    )


@router.get("/list.models", response_model=ModelListResponse, name="list:models")
def model_list(
    pagination: RequestPagination = Depends(),
    sort: RequestSort = Depends(),
    service: ModelService = Depends(ModelService.get_instance),
    get_all_versions_flag: Optional[bool] = False,
):
    list_models = service.list_models(
        sort_request=sort,
        pagination=pagination,
        get_all_versions_flag=get_all_versions_flag,
    )
    response = ModelListResponse(
        model_list=list_models,
        meta={
            "page": pagination.page,
            "limit": pagination.limit,
            "total": service.count_models(),
        },
    )
    return response


@router.post(
    "/model.register",
    response_model=RegisterModelResponse,
    name="model:register",
    response_model_exclude_none=True,
)
def register_model(
    request: RegisterModelRequest = Body(
        ..., description="the request model register info"
    ),
    service: ModelService = Depends(ModelService.get_instance),
):
    registered_model = service.register_model(
        model_name=request.model_name, model_id=request.model_id
    )

    return RegisterModelResponse(
        model_id=registered_model.model_id,
        model_name=registered_model.model_name,
        baseline=registered_model.baseline,
    )


@router.post(
    "/model.version.register",
    response_model=RegisterModelVersionResponse,
    name="model_version:register",
)
def register_model_version(
    request: RegisterModelVersionRequest = Body(
        ..., description="the request model version register info"
    ),
    service: ModelVersionService = Depends(ModelVersionService.get_instance),
):
    registered_model_version: ModelVersionDB = service.register_model_version(
        model_id=request.model_id,
        model_version=request.model_version,
        version_schema=request.version_schema,
    )
    return RegisterModelVersionResponse(
        model_version=registered_model_version.model_version,
        model_version_id=registered_model_version.model_version_id,
    )


@router.get(
    "/model.version.info",
    response_model=ModelVersionInfoResponse,
    name="model_version:info",
)
def model_version_info(
    model_version_id: UUID,
    service: ModelVersionService = Depends(ModelVersionService.get_instance),
):
    model_version: ModelVersionDB = service.find_by_id(
        model_version_id=model_version_id
    )
    associated_datasets: List[DatasetDB] = service.get_all_datasets(
        model_version_id=model_version_id
    )

    return ModelVersionInfoResponse(
        model_version=model_version, datasets=associated_datasets
    )


@router.post("/model.delete")
def delete_model(
    model_id: UUID = Body(..., description="the model id to delete"),
    service: ModelService = Depends(ModelService.get_instance),
):
    service.delete_model(model_id=model_id)
    return {"message": "Model deleted successfully"}


@router.post(
    "/model.update",
    response_model=UpdateModelResponse,
    name="model:update",
)
def update_model(
    request: UpdateModelRequest = Body(
        ..., description="the request model update info"
    ),
    service: ModelService = Depends(ModelService.get_instance),
):
    updated_model = service.update_model(
        model_id=request.model_id,
        property_name=request.property_name,
        baseline=request.baseline,
        positive_class=request.positive_class,
    )
    return updated_model
