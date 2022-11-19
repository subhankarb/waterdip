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
from typing import Dict, Optional

from pydantic import UUID4, BaseModel

from waterdip.server.commons.models import ColumnDataType, PredictionTaskType


class RegisterModelRequest(BaseModel):
    model_name: str


class RegisterModelResponse(BaseModel):
    model_id: UUID4
    model_name: str


class ModelVersionSchema(BaseModel):
    features: Dict[str, ColumnDataType]
    predictions: Dict[str, ColumnDataType]


class RegisterModelVersionRequest(BaseModel):
    model_id: UUID4
    model_version: str
    task_type: PredictionTaskType
    description: Optional[str]
    version_schema: ModelVersionSchema


class RegisterModelVersionResponse(BaseModel):
    model_version_id: UUID4
    model_version: str
