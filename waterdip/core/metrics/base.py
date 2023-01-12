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

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from pymongo.collection import Collection

from waterdip.core.commons.models import TimeRange


class MongoMetric(ABC):
    def __init__(self, collection: Collection):
        self._collection = collection

    @property
    @abstractmethod
    def metric_name(self) -> str:
        pass

    @abstractmethod
    def aggregation_result(self, **kwargs) -> Dict[str, Any]:
        pass

    @abstractmethod
    def _aggregation_query(self, *args, **kwargs) -> List[Dict[str, Any]]:
        pass

    @staticmethod
    def _time_filter_builder(time_range: TimeRange = None):
        time_filter = {}
        if time_range is not None:
            time_filter = {
                "created_at": {
                    "$gte": time_range.start_time,
                    "$lte": time_range.end_time,
                }
            }
        return time_filter
