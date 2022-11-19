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

from enum import Enum


class PredictionTaskType(str, Enum):
    BINARY = "BINARY"
    MULTI_CLASS = "MULTICLASS"


class DatasetType(str, Enum):
    BATCH = "BATCH"
    EVENT = "EVENT"


class ColumnDataType(str, Enum):
    NUMERIC = "NUMERIC"
    CATEGORICAL = "CATEGORICAL"
    BOOLEAN = "BOOLEAN"


class ColumnMappingType(str, Enum):
    FEATURE = "FEATURE"
    RAW = "RAW"
    PREDICTION = "PREDICTION"
    PREDICTION_SCORE = "PREDICTION_SCORE"
    ACTUAL = "ACTUAL"
    ACTUAL_SCORE = "ACTUAL_SCORE"
    ACTUAL_RANK_SEQUENCE = "ACTUAL_RANK_SEQUENCE"
    GROUP_BY = "GROUP_BY"
