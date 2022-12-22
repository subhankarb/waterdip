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
    """
    prediction task type for any model version.

    Attributes:
    ------------------
    BINARY:
        Binary Classification
    MULTI_CLASS:
        Multi Class Classification

    """

    BINARY = "BINARY"
    MULTI_CLASS = "MULTICLASS"


class DatasetType(str, Enum):
    """
    dataset type of the datasets associated to model versions

    Attributes:
    ------------------
    BATCH:
        One time uploaded dataset. It is a non-time series dataset
    """

    BATCH = "BATCH"
    EVENT = "EVENT"


class ColumnDataType(str, Enum):
    """
    data type of the dataset

    Attributes:
    ------------------
    NUMERIC:
        numeric data type. It can be integer or float
    CATEGORICAL:
        categorical data type can take on one of a limited,
        and usually fixed, number of possible values
    BOOLEAN:
        boolean data type, i.e. True or False

    """

    NUMERIC = "NUMERIC"
    CATEGORICAL = "CATEGORICAL"
    BOOLEAN = "BOOLEAN"


class ColumnMappingType(str, Enum):
    """
    mapping of column type to model version schema.

    Attributes:
    ------------------
    FEATURE:
        column type is a feature input type
    PREDICTION:
        column type is a prediction output type
    PREDICTION_SCORE:
        column type is a prediction score type
    ACTUAL:
        column type is an actual type. Actual is realized and final output
    ACTUAL_SCORE:
        column type is an actual score.


    """

    FEATURE = "FEATURE"
    PREDICTION = "PREDICTION"
    PREDICTION_SCORE = "PREDICTION_SCORE"
    ACTUAL = "ACTUAL"
    ACTUAL_SCORE = "ACTUAL_SCORE"


class MonitorType(str, Enum):
    """
    Alert type of the dataset

    Attributes:
    ------------------
    DATA_QUALITY:

    DRIFT:

    MODEL_PERFORMANCE:
    
    """

    DATA_QUALITY = "DATA_QUALITY"
    DRIFT = "DRIFT"
    MODEL_PERFORMANCE = "MODEL_PERFORMANCE"

class DriftMetric(str, Enum):
    PSI = "PSI"


class DataQualityMetric(str, Enum):
    MISSING_VALUE = "MISSING_VALUE"
    EMPTY_VALUE = "EMPTY_VALUE"
    NEW_VALUE = "NEW_VALUE"


class PerformanceMetric(str, Enum):
    PRECISION = "PRECISION"
    RECALL = "RECALL"
    F1 = "F1"



