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

from collections import OrderedDict
from datetime import date, datetime, timedelta
from typing import Dict, List

from dateutil.parser import parse
from fastapi import Depends

from waterdip.core.commons.models import MonitorType
from waterdip.server.apis.models.models import ModelOverviewAlertList
from waterdip.server.db.repositories.alert_repository import (
    AlertDB,
    AlertRepository,
    BaseAlertDB,
)


class AlertService:
    _INSTANCE: "AlertService" = None

    @classmethod
    def get_instance(
        cls, repository: AlertRepository = Depends(AlertRepository.get_instance)
    ):
        if not cls._INSTANCE:
            cls._INSTANCE = cls(repository=repository)
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
            {"$match": {"model_id": {"$in": model_ids}}},
            {
                "$group": {
                    "_id": {"model_id": "$model_id", "monitor_type": "$monitor_type"},
                    "count": {"$sum": 1},
                }
            },
            {
                "$group": {
                    "_id": "$_id.model_id",
                    "alerts": {
                        "$push": {
                            "monitor_type": "$_id.monitor_type",
                            "count": "$count",
                        }
                    },
                }
            },
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

    def count_alert_by_filter(self, filters: Dict) -> int:
        return self._repository.count_alerts(filters)

    def alert_week_stats(self, model_id):
        alerts_days = 7
        today_date = datetime.combine(date.today(), datetime.min.time())

        agg_alert_count_week_pipeline = [
            {
                "$match": {
                    "model_id": str(model_id),
                    "created_at": {
                        "$gte": datetime.utcnow() - timedelta(days=alerts_days),
                        "$lt": today_date,
                    },
                }
            },
            {
                "$project": {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"},
                    "day": {"$dayOfMonth": "$created_at"},
                }
            },
            {
                "$group": {
                    "_id": {"year": "$year", "month": "$month", "day": "$day"},
                    "count": {"$sum": 1},
                }
            },
            {
                "$sort": {
                    "_id.year": 1,
                    "_id.month": 1,
                    "_id.day": 1,
                }
            }
        ]
        week_stats = self._repository.agg_alerts(agg_alert_count_week_pipeline)
        day_vs_count = dict()
        for i in week_stats:
            day_vs_count[
                datetime(i["_id"]["year"], i["_id"]["month"], i["_id"]["day"]).strftime(
                    "%Y-%m-%d"
                )
            ] = i["count"]
        available_days = 0
        for i in range(7):
            current = (datetime.utcnow() - timedelta(days=7) + timedelta(i)).strftime(
                "%Y-%m-%d"
            )
            if current not in day_vs_count.keys():
                day_vs_count[current] = 0
            else:
                available_days += 1
        day_vs_count = OrderedDict(
            sorted(day_vs_count.items(), key=lambda x: parse(x[0]))
        )
        week_alerts_average = sum(day_vs_count.values()) / 7 if available_days else 0
        today_alert_count = self.today_alert_count(model_id)
        if week_alerts_average == 0:
            """
            If week_alerts_average is 0, then we can't calculate the percentage change as it is not defined, hence we are setting it to zero.
            """
            alert_percentage_change = 0
        else:
            alert_percentage_change = int(
                ((today_alert_count - week_alerts_average) / week_alerts_average) * 100
            )

        return {
            "alert_trend_data": list(day_vs_count.values()),
            "alert_percentage_change": alert_percentage_change,
        }

    def find_alerts(
        self, model_id: str, limit: int = 5
    ) -> List[ModelOverviewAlertList]:
        return [
            ModelOverviewAlertList(
                alert_id=alert["alert_id"],
                monitor_type=MonitorType(alert["monitor_type"]),
                created_at=alert["created_at"],
            )
            for alert in self._repository.find_alerts(model_id, limit)
        ]

    def today_alert_count(self, model_id: str) -> int:
        today_date = datetime.combine(date.today(), datetime.min.time())
        today_alerts_count_filter = {
            "model_id": str(model_id),
            "created_at": {
                "$gte": today_date,
                "$lte": datetime.utcnow(),
            },
        }

        today_alert_count = self._repository.count_alerts(today_alerts_count_filter)
        return today_alert_count
