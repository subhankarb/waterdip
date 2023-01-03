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

from pydantic import BaseModel

from waterdip.server.commons.models import Histogram


class NumericColumnStats(BaseModel):
    column_name: str
    missing_total: Optional[int]
    missing_percentage: Optional[float]
    mean: Optional[float]
    std_dev: Optional[float]
    zeros: Optional[int]
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