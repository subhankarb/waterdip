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
from typing import List, Optional
from uuid import UUID

from pydantic import UUID4
from pydantic.dataclasses import dataclass

from waterdip.server.services.logging_service import ServiceLogEvent, ServiceLogRow


class BatchDatasetLogRowReq(ServiceLogRow):
    """batch dataset row in API request"""

    pass


@dataclass
class BatchDatasetLogRequest:
    """
    Request Body for batch dataset upload API

    Attributes:
    ------------------
    model_version_id:
        unique id of the model version
    environment:
        the environment this dataset will be used for. possible values can ve training, testing and validation
    rows:
        list of rows of the dataset

    TODO Make environment attribute an ENUM
    """

    model_version_id: UUID
    environment: str
    rows: List[BatchDatasetLogRowReq]


class EventLogRowReq(ServiceLogEvent):
    """event row in Event logging API request"""

    pass


@dataclass
class EventLogRequest:
    """
    Request Body for model prediction event upload API

    Attributes:
    ------------------
     model_version_id:
        unique id of the model version
    events:
        list of prediction events need to be logged
    timestamp:
        timestamp of all the events. This is an optional attribute.
        If timestamp is not present then current server utc time will be
        generated and attached to the events

    """

    model_version_id: UUID
    events: List[EventLogRowReq]
    timestamp: Optional[datetime] = None
