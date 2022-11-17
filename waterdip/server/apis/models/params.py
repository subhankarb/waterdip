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

from dataclasses import dataclass
from typing import Optional

import pymongo
from fastapi import Query
from pydantic import BaseModel, validator


@dataclass
class RequestPagination:
    """Query pagination params"""

    limit: int = Query(default=10, gte=0, le=1000, description="Response records limit")
    page: int = Query(default=0, ge=0, le=10000, description="Record page")


class RequestSort(BaseModel):
    sort: str = Query(default=None, description="Sort field for records list")

    @validator("sort")
    def name_must_contain_sort_order(cls, v):
        if v is not None:
            values = v.rsplit("_", 1)
            if len(values) != 2:
                raise ValueError("sort must contain at least one _")
            sort_order = values[1]
            if sort_order == "asc" or sort_order == "desc":
                return v
            raise ValueError("sort order must be either asc or desc")

    @property
    def get_sort_order(self) -> int:
        if self.sort is not None:
            sort_order = self.sort.rsplit("_", 1)[1]
            if sort_order == "desc":
                return pymongo.DESCENDING
            else:
                return pymongo.ASCENDING
        return pymongo.DESCENDING

    @property
    def get_sort_field(self) -> Optional[str]:
        if self.sort is not None:
            sort_config = self.sort.rsplit("_", 1)
            return sort_config[0]
        return None
