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

from redbird.repos import MongoRepo
from rocketry import Rocketry

from waterdip.server.commons.config import settings

mongo_repo = MongoRepo(
    uri=settings.mongo_url, database=settings.mongo_database, collection="rocketry"
)

scheduler = Rocketry(config={"task_execution": "async"}, logger_repo=mongo_repo)
