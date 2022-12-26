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

from typing import Dict, List, Optional
from uuid import UUID

from fastapi import Depends

from waterdip.server.db.models.alerts import AlertDB, BaseAlertDB
from waterdip.server.db.models.models import BaseModelVersionDB, ModelDB, ModelVersionDB
from waterdip.server.db.mongodb import (
    MONGO_COLLECTION_ALERTS,
    MONGO_COLLECTION_MODEL_VERSIONS,
    MONGO_COLLECTION_MODELS,
    MongodbBackend,
)


class AlertRepository:
    _INSTANCE = None

    @classmethod
    def get_instance(
        cls, mongodb: MongodbBackend = Depends(MongodbBackend.get_instance)
    ):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls(mongodb=mongodb)
        return cls._INSTANCE

    def __init__(self, mongodb: MongodbBackend):
        self._mongo = mongodb

    def insert_alert(self, alert: BaseAlertDB) -> AlertDB:
        inserted_alert = self._mongo.database[MONGO_COLLECTION_ALERTS].insert_one(
            document=alert.dict()
        )

        created_alert = self._mongo.database[MONGO_COLLECTION_ALERTS].find_one(
            {"_id": inserted_alert.inserted_id}
        )

        return BaseAlertDB(**created_alert)

    def count_alerts(self, filters: Dict) -> int:
        total = self._mongo.database[MONGO_COLLECTION_ALERTS].count_documents(
            filter=filters
        )
        return total

    def agg_alerts(self, agg_pipeline: List[Dict]):
        return self._mongo.database[MONGO_COLLECTION_ALERTS].aggregate(
            pipeline=agg_pipeline
        )
