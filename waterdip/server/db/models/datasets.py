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
from typing import Any, Dict, List, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field, root_validator

from waterdip.core.commons.models import ColumnDataType, DatasetType, Environment


class BaseColumnInfoDB(BaseModel):
    name: str = Field(default=None)
    column_type: ColumnDataType = Field(default=None)
    possible_values: Optional[List[Any]]
    is_nullable: Optional[bool]
    value_range_min: Optional[float]
    value_range_max: Optional[float]


ColumnInfoDB = TypeVar("ColumnInfoDB", bound=BaseColumnInfoDB)


class BaseDatasetDB(BaseModel):

    dataset_id: UUID = Field(default=None)
    dataset_name: str = Field(default=None)
    created_at: datetime = Field(default=None)
    dataset_type: DatasetType = Field(
        description="Dataset type. It can be batch dataset or event dataset"
    )
    model_id: UUID = Field(description="Reference model id")
    model_version_id: UUID = Field(description="Reference model version id")
    environment: Environment = Field(
        description="""
                                               Dataset environment. Use can upload at max one dataset every
                                               environment. There are three environment. So user can only upload
                                               max three dataset per model version
                                               """
    )
    meta: Optional[Dict] = None

    @classmethod
    @root_validator
    def env_dataset_type_validator(cls, values):
        dataset_type: DatasetType = values.get("dataset_type")
        environment: Environment = values.get("environment")
        if dataset_type == DatasetType.EVENT:
            if environment != Environment.PRODUCTION:
                raise ValueError(
                    "DatasetType EVENT can only applicable to PRODUCTION Env"
                )
        if dataset_type == DatasetType.BATCH:
            if environment == Environment.PRODUCTION:
                raise ValueError(
                    "DatasetType BATCH can not applicable to PRODUCTION Env"
                )

    def dict(self, *args, **kwargs) -> "DictStrAny":
        dataset = super().dict(*args, **kwargs)
        dataset["dataset_id"] = str(dataset["dataset_id"])
        dataset["model_id"] = str(dataset["model_id"])
        dataset["model_version_id"] = str(dataset["model_version_id"])
        return dataset


DatasetDB = TypeVar("DatasetDB", bound=BaseDatasetDB)
