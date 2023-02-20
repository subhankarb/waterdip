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
from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel

from waterdip.core.commons.models import Histogram


class NumericColumnStats(BaseModel):
    column_name: str
    missing_total: Optional[int]
    missing_percentage: Optional[float]
    mean: Optional[float]
    std_dev: Optional[float]
    variance: Optional[float]
    zeros: Optional[int]
    total: Optional[float]
    min: Optional[float]
    max: Optional[float]
    histogram: Optional[Histogram]


class CategoricalColumnStats(BaseModel):
    column_name: str
    missing_total: Optional[int]
    missing_percentage: Optional[float]
    unique: Optional[int]
    top: Optional[str]
    histogram: Optional[Histogram]


class DatasetMetricsResponse(BaseModel):
    numeric_column_stats: List[NumericColumnStats]
    categorical_column_stats: List[CategoricalColumnStats]


class PerfomanceMetricResponse(BaseModel):
    """
    Perfomance model API response

    Attributes:
    ------------------
    accuracy:
        accuracy of the model
    true_positive:
        true positive of the model
    false_negative:
        false negative of the model
    true_negative:
        true negative of the model
    false_positive:
        false positive of the model
    precision:
        precision of the model
    recall:
        recall of the model
    sensitivity:
        sensitivity of the model
    specificity:
        specificity of the model
    f1:
        f1 of the model
    """

    accuracy: Dict
    true_positive: Dict
    false_negative: Dict
    true_negative: Dict
    false_positive: Dict
    precision: Dict
    recall: Dict
    sensitivity: Dict
    specificity: Dict
    f1: Dict
