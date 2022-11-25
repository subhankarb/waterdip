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
from typing import Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel

from waterdip.server.commons.models import ColumnDataType, PredictionTaskType


class RegisterModelRequest(BaseModel):
    """
    Register model API request

    Attributes:
    ------------------
    model_name:
        name of the model
    """

    model_name: str


class RegisterModelResponse(BaseModel):
    """
    Registered model API response

    Attributes:
    ------------------
    model_id:
        server generated unique id (uuid4)
    model_name:
        user provided model display name
    """

    model_id: UUID
    model_name: str


class ModelVersionSchema(BaseModel):
    """
    Schema of Model version

    Attributes:
    ------------------
    features:
        schema of the features for model version
    predictions:
        schema of the predictions for model version

    Example:
        version_schema = ModelVersionSchema(
            features={"age": ColumnDataType.NUMERIC, "location": ColumnDataType.CATEGORICAL},
            predictions={"is_eligible": ColumnDataType.BOOLEAN},
        )

    """

    features: Dict[str, ColumnDataType]
    predictions: Dict[str, ColumnDataType]


class RegisterModelVersionRequest(BaseModel):
    """
    Model version register API request.
    One model can have multiple model version

    Attributes:
    ------------------
    model_id:
        unique id of the parent model of the model version
    model_version:
        name of the model version i.e. v1, v2 etc
    task_type:
        type of prediction task i.e. Binary, Multi-class
    version_schema:
        schema of this model version
    description:
        small details of this model version, optional

    """

    model_id: UUID
    model_version: str
    task_type: PredictionTaskType
    version_schema: ModelVersionSchema
    description: Optional[str]


class RegisterModelVersionResponse(BaseModel):
    """
    Registered model version API response

    Attributes:
    ------------------
    model_version_id:
        server generated unique model version id (uuid4)
    model_version:
        user provided model version name

    """

    model_version_id: UUID
    model_version: str


class ModelListRow(BaseModel):
    model_id: UUID
    model_name: str
    model_version_id: Optional[str]
    created_at: Optional[datetime]
    total_predictions: int = 0
    last_prediction: Optional[datetime]
    num_alert_perf: int = 0
    num_alert_data_behave: int = 0
    num_alert_data_integrity: int = 0


class ModelListResponse(BaseModel):
    model_list: List[ModelListRow]
    meta: Optional[Dict[str, Union[str, int]]]
