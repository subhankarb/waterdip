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

from typing import Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel


class DatasetListRow(BaseModel):
    """
    Dataset entity for dataset_list API response

    Attributes:
    ------------------
    dataset_name:
        name of the dataset
    dataset_id:
        unique dataset id

    """

    dataset_name: str
    dataset_id: UUID


class DatasetListResponse(BaseModel):
    """
    Dataset List API response

    Attributes:
    ------------------
    dataset_list:
        list of dataset rows
    meta:
        information about the dataset list i.e. page, limit, total

    """

    dataset_list: List[DatasetListRow]
    meta: Optional[Dict[str, Union[int, str]]]
