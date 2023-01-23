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

from datetime import date, datetime, timedelta
from typing import Dict, List, Union

from fastapi import Depends
from uuid import UUID
from waterdip.server.apis.models.models import DateHistogram, ModelOverviewPredictions
from waterdip.server.db.models.dataset_rows import (
    BaseClassificationEventRowDB,
    BaseDatasetBatchRowDB,
    BaseEventRowDB,
)
from waterdip.server.db.repositories.dataset_row_repository import (
    BatchDatasetRowRepository,
    EventDatasetRowRepository,
)
from waterdip.server.db.repositories.model_repository import ModelRepository


class ServiceDatasetBatchRow(BaseDatasetBatchRowDB):
    pass


class BatchDatasetRowService:

    _INSTANCE: "BatchDatasetRowService" = None

    @classmethod
    def get_instance(
        cls,
        repository: BatchDatasetRowRepository = Depends(
            BatchDatasetRowRepository.get_instance
        ),
    ):
        if not cls._INSTANCE:
            cls._INSTANCE = cls(repository=repository)
        return cls._INSTANCE

    def __init__(self, repository: BatchDatasetRowRepository):
        self._repository = repository

    def insert_rows(self, rows: List[ServiceDatasetBatchRow]) -> int:
        inserted_rows = self._repository.inset_rows(rows)
        return len(inserted_rows)

    def delete_rows_by_model_id(self, model_id: UUID) -> int:
        self._repository.delete_rows_by_model_id(str(model_id))


class ServiceEventRow(BaseEventRowDB):
    pass


class ServiceClassificationEventRow(BaseClassificationEventRowDB):
    pass


class EventDatasetRowService:

    _INSTANCE: "EventDatasetRowService" = None

    @classmethod
    def get_instance(
        cls,
        repository: EventDatasetRowRepository = Depends(
            EventDatasetRowRepository.get_instance
        ),
    ):
        if not cls._INSTANCE:
            cls._INSTANCE = cls(repository=repository)
        return cls._INSTANCE

    def __init__(self, repository: EventDatasetRowRepository):
        self._repository = repository

    def insert_rows(
        self, rows: Union[List[ServiceEventRow], List[ServiceClassificationEventRow]]
    ) -> int:
        inserted_rows = self._repository.inset_rows(rows)
        return len(inserted_rows)

    def count_prediction_by_model_id(self, model_id: str) -> int:
        total_predictions = self._repository.count_prediction_by_model_id(model_id)
        return total_predictions

    def find_last_prediction_date(self, model_id: str) -> datetime:
        last_prediction = self._repository.find_last_prediction_date(model_id)
        return last_prediction

    def prediction_average(self, model_id: str) -> Dict:
        days = 30
        start_date = self._repository.find_first_prediction_date(str(model_id))
        if start_date is None:
            """
            No predictions have been made!
            """
            return {
                "pred_average": 0,
                "pred_average_window_days": 0,
            }
        window = datetime.utcnow() - start_date
        window_date = datetime.utcnow() - timedelta(days=window.days)
        if window.days > days:
            window_date = datetime.utcnow() - days
        window_prediction_count = self._repository.prediction_count(
            filter={"model_id": str(model_id), "created_at": {"$gte": window_date}}
        )
        if not window.days:
            """
            Model has been created today!
            """
            return {
                "pred_average": window_prediction_count,
                "pred_average_window_days": 1,
            }
        return {
            "pred_average": int(window_prediction_count / window.days),
            "pred_average_window_days": window.days,
        }

    def week_prediction_stats(self, model_id: str) -> Dict:
        prediction_days = 7
        today_date = datetime.combine(date.today(), datetime.min.time())
        today = datetime.combine(date.today(), datetime.min.time())
        today_predicition_count = self._repository.prediction_count(
            filter={"model_id": str(model_id), "created_at": {"$gte": today}}
        )
        agg_week_prediction_count_pipeline = [
            {
                "$match": {
                    "model_id": str(model_id),
                    "created_at": {
                        "$gte": datetime.utcnow() - timedelta(days=prediction_days),
                        "$lt": today_date,
                    },
                }
            },
            {"$project": {"day": {"$substr": ["$created_at", 0, 10]}}},
            {"$sort": {"created_at": 1}},
            {"$group": {"_id": "$day", "count": {"$sum": 1}}},
        ]
        week_stats = self._repository.agg_prediction(agg_week_prediction_count_pipeline)
        day = []
        count = []
        for i in week_stats:
            day.append(i["_id"])
            count.append(i["count"])
        available_days = 0
        pre_trend = []
        for i in range(0, prediction_days):
            current = (
                datetime.utcnow() - timedelta(days=prediction_days - i)
            ).strftime("%Y-%m-%d")
            if current not in day:
                pre_trend.append(0)
            else:
                pre_trend.append(count[available_days])
                available_days += 1

        yesterday_prediction_count = pre_trend[-1] if available_days != 0 else 0
        week_prediction_average = sum(count) / 7 if available_days != 0 else 0
        if week_prediction_average == 0:
            """
            Percentage change when there is no prediction in the last 7 days is not defined.
            """
            pred_percentage_change = 0
        else:
            pred_percentage_change = int(
                (
                    (today_predicition_count - week_prediction_average)
                    / week_prediction_average
                )
                * 100
            )

        return {
            "pred_yesterday": yesterday_prediction_count,
            "pred_percentage_change": pred_percentage_change,
            "pred_trend_data": pre_trend,
        }

    def prediction_histogram(self, model_id: str) -> dict:

        preidiction_histogram_pipeline = [
            {"$match": {"model_id": model_id}},
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
            },
        ]

        prediction_histogram = self._repository.agg_prediction(
            preidiction_histogram_pipeline
        )
        date_bins = []
        val = []
        for i in prediction_histogram:
            date_bins.append(
                datetime(i["_id"]["year"], i["_id"]["month"], i["_id"]["day"])
            )
            val.append(i["count"])
        return DateHistogram(date_bins=date_bins, val=val)

    def prediction_histogram_version(self, model_id: str) -> dict:

        preidiction_histogram_pipeline = [
            {"$match": {"model_id": model_id}},
            {
                "$project": {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"},
                    "day": {"$dayOfMonth": "$created_at"},
                    "model_version_id": "$model_version_id",
                }
            },
            {
                "$group": {
                    "_id": {
                        "year": "$year",
                        "month": "$month",
                        "day": "$day",
                        "version": "$model_version_id",
                    },
                    "count": {"$sum": 1},
                }
            },
            {
                "$group": {
                    "_id": "$_id.version",
                    "prediction": {
                        "$push": {
                            "year": "$$ROOT._id.year",
                            "month": "$$ROOT._id.month",
                            "day": "$$ROOT._id.day",
                            "count": "$$ROOT.count",
                        }
                    },
                }
            },
            {
                "$sort": {
                    "_id.year": 1,
                    "_id.month": 1,
                    "_id.day": 1,
                }
            },
        ]
        predictions_versions = []
        for versions_prediction in self._repository.agg_prediction(
            preidiction_histogram_pipeline
        ):
            date_bins = []
            val = []
            for i in versions_prediction["prediction"]:

                date_bins.append(datetime(i["year"], i["month"], i["day"]))
                val.append(i["count"])
            predictions_versions.append(
                {
                    versions_prediction["_id"]: DateHistogram(
                        date_bins=date_bins, val=val
                    )
                }
            )
        return predictions_versions

    def delete_rows_by_model_id(self, model_id: UUID) -> None:
        self._repository.delete_rows_by_model_id(str(model_id))
