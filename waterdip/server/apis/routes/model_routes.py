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

from fastapi import APIRouter, Body, Depends

from waterdip.server.apis.models.models import (
    RegisterModelRequest,
    RegisterModelResponse,
    RegisterModelVersionRequest,
    RegisterModelVersionResponse,
)
from waterdip.server.db.models.models import ModelVersionDB
from waterdip.server.services.model_service import ModelService, ModelVersionService

router = APIRouter()


@router.post(
    "/model.register", response_model=RegisterModelResponse, name="model:register"
)
def register_model(
    request: RegisterModelRequest = Body(...),
    service: ModelService = Depends(ModelService.get_instance),
):
    registered_model = service.register_model(request.model_name)

    return RegisterModelResponse(
        model_id=registered_model.model_id, model_name=registered_model.model_name
    )


@router.post(
    "/model.version.register",
    response_model=RegisterModelVersionResponse,
    name="model_version:register",
)
def register_model_version(
    request: RegisterModelVersionRequest = Body(...),
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
