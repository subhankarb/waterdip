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
    pass


@dataclass
class BatchDatasetLogRequest:
    model_version_id: UUID
    environment: str
    rows: List[BatchDatasetLogRowReq]


class EventLogRowReq(ServiceLogEvent):
    pass


@dataclass
class EventLogRequest:
    model_version_id: UUID
    events: List[EventLogRowReq]
    timestamp: Optional[datetime]
