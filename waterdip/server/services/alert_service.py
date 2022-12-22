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
from typing import List, Optional, TypeVar, Dict
from uuid import UUID

from fastapi import Depends
from pydantic import Field

from waterdip.server.apis.models.params import RequestPagination, RequestSort
from waterdip.server.commons.models import DatasetType
from waterdip.server.db.models.datasets import BaseDatasetDB, DatasetDB
from waterdip.server.db.repositories.dataset_repository import DatasetRepository
from waterdip.server.db.repositories.model_repository import ModelVersionRepository
from waterdip.server.db.repositories.alert_repository import AlertRepository, BaseAlertDB, AlertDB
from waterdip.server.errors.base_errors import EntityNotFoundError


class AlertService:
    _INSTANCE: "AlertService" = None

    @classmethod
    def get_instance(
        cls,
        repository: AlertRepository = Depends(AlertRepository.get_instance)
    ):
        if not cls._INSTANCE:
            cls._INSTANCE = cls(
                repository=repository
            )
        return cls._INSTANCE

    def __init__(
        self,
        repository: AlertRepository,
    ):
        self._repository = repository

    def insert_alert(self, alert: BaseAlertDB) -> AlertDB:
        return self._repository.insert_alert(alert)

    def get_alerts(self, model_ids: List[str]) -> Dict[str, Dict[str, int]]:
        _agg_alerts: Dict[str, Dict[str, int]] = dict()
        agg_pipeline = [
            {
                '$match': {
                    'model_id': {
                        '$in': model_ids
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        'model_id': '$model_id',
                        'monitor_type': '$monitor_type'
                    },
                    'count': {
                        '$sum': 1
                    }
                }
            }, {
                '$group': {
                    '_id': '$_id.model_id',
                    'alerts': {
                        '$push': {
                            'monitor_type': '$_id.monitor_type',
                            'count': '$count'
                        }
                    }
                }
            }
        ]
        for doc in self._repository.agg_alerts(agg_pipeline):
            model_id = doc["_id"]
            d = {"DRIFT": 0, "DATA_QUALITY": 0, "DATA_PERFORMANCE": 0}
            for alert in doc["alerts"]:
                """
                "monitor_type":"DRIFT",
                "count": 1
                """
                d[alert["monitor_type"]] = alert["count"]
            _agg_alerts[model_id] = d
        return _agg_alerts
