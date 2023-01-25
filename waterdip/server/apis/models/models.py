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

from waterdip.core.commons.models import (
    ColumnDataType,
    DateHistogram,
    ModelBaseline,
    MonitorType,
    PredictionTaskType,
    ModelBaseline,
)
from waterdip.server.db.models.datasets import DatasetDB
from waterdip.server.db.models.models import BaseModelVersionDB, BaseModelDB


class RegisterModelRequest(BaseModel):
    """
    Register model API request

    Attributes:
    ------------------
    model_name:
        name of the model
    """

    model_name: str
    model_id: Optional[UUID] = None

class UpdateModelRequest(BaseModel):
    """
    Update model API request

    Attributes:
    ------------------
    model_name:
        name of the model
    property_name:
        name of the property to update
    baseline:
        baseline of the model
    positive_class:
        positive class of the model
    """

    model_id: Optional[UUID] = None
    property_name: Optional[str] = None
    baseline: Optional[ModelBaseline] = None
    positive_class : Optional[Dict] = None



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
    baseline: ModelBaseline


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
    """
    Schema of Model List row response

    Attributes:
    ------------------
    model_id:
        Model ID
    model_name:
        Name of the model
    model_version_id:
        Model version ID
    created_at:
        Model creation time
    total_predictions:
        Total number of prediction across all versions
    num_alert_perf:
        Total number of performance alerts across all versions
    num_alert_drift:
        Total number of drift alerts across all versions
    num_alert_data_quality:
        Total number of data quality alerts across all versions
    model_versions:
        all model versions with their name and id in {version_name: version_id} format
    """

    model_id: UUID
    model_name: str
    model_version_id: Optional[UUID]
    created_at: Optional[datetime]
    total_predictions: int = 0
    last_prediction: Optional[datetime]
    num_alert_perf: int = 0
    num_alert_drift: int = 0
    num_alert_data_quality: int = 0
    model_versions: Optional[List[Dict[str, UUID]]]


class ModelListResponse(BaseModel):
    model_list: List[ModelListRow]
    meta: Optional[Dict[str, Union[str, int]]]


class ModelVersionInfoResponse(BaseModel):
    model_version: BaseModelVersionDB
    datasets: List[DatasetDB]


class ModelOverviewPredictions(BaseModel):
    """
    Schema of Model prediction overview

    Attributes:
    ------------------
    pred_yesterday:
        number of prediction on the day before
    pred_percentage_change:
        change in percentage over last 7 days' average
    pred_trend_data:
        agg number of predictions per day for last 7 days
    pred_average:
        average number of predictions
    pred_average_window_days:
        number of days the average has been calculated

    """

    pred_yesterday: int
    pred_percentage_change: int
    pred_trend_data: List[int]
    pred_average: int
    pred_average_window_days: int


class ModelPredictionHistogram(BaseModel):
    """
    Schema of Model prediction histograms

    Attributes:
    ------------------
    predictions:
        number of total predictions across all the versions agg per day
    predictions_versions:
        number of predictions agg by version per day
    """

    predictions: DateHistogram
    predictions_versions: List[Dict[str, DateHistogram]]


class ModelOverviewAlerts(BaseModel):
    """
    Schema of Model overview alert list row

    Attributes:
    ------------------
    alerts_count:
        total number of alerts generated
    alert_percentage_change:
        change in percentage over last 7 days' average
    alert_trend_data:
        agg number of alerts per day for last 7 days
    """

    alerts_count: int
    alert_percentage_change: int
    alert_trend_data: List[int]


class ModelOverviewAlertList(BaseModel):
    """
    Schema of Model overview alert list row

    Attributes:
    ------------------
    alert_id:
        Alert ID
    monitor_name:
        name of the monitor, which generated the alert
    monitor_type:
        Type of the monitor
    created_at:
        created time of the alert
    """

    alert_id: UUID
    monitor_name: Optional[str]
    monitor_type: MonitorType
    created_at: datetime


class ModelOverviewResponse(BaseModel):
    """
    Schema of Model overview response

    Attributes:
    ------------------
    model_id:
        Model ID
    model_prediction_overview:
        prediction overview across all the versions
    model_prediction_hist:
        prediction histogram total and all versions
    model_alert_overview:
        alert overview alerts all the versions
    model_alert_list:
        latest five alerts from all the versions
    number_of_model_versions:
        number of versions registered under a particular model
    latest_version:
        latest version registered for the model
    latest_version_created_at:
        creation time of latest version of the model

    """

    model_id: UUID
    model_prediction_overview: ModelOverviewPredictions
    model_prediction_hist: ModelPredictionHistogram
    model_alert_overview: ModelOverviewAlerts
    model_alert_list: List[ModelOverviewAlertList]
    number_of_model_versions: int = 0
    latest_version: BaseModelVersionDB = None
    latest_version_created_at: datetime = None


class ModelInfoResponse(BaseModel):
    """
    Schema of Model info response

    Attributes:
    ------------------
    model_id:
        Model ID
    model_name:
        model name
    model_versions:
        list of all model versions associated with this model
    """

    model_id: UUID
    model_name: str
    model_versions: List[BaseModelVersionDB]

class UpdateModelResponse(BaseModelDB):
    pass
    
