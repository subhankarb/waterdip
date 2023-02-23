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
from datetime import timedelta
from typing import Any, Dict, List
from uuid import UUID

from pymongo.collection import Collection

from waterdip.core.commons.models import TimeRange
from waterdip.core.metrics.base import MongoMetric


class ClassificationDateHistogramDBMetrics(MongoMetric):
    """
    Attributes:
    -----
    collection: Collection
        mongo collection
    dataset_id: UUID
        dataset id on which the metric calculation will be applied

    """

    def __init__(self, collection: Collection, dataset_id: UUID, positive_class: str):
        super().__init__(collection)
        self._dataset_id = dataset_id
        self._positive_class = positive_class
        self._class_position = 0

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

    @staticmethod
    def _dict_day_ratio(cnt, total) -> Dict:
        dct = {}
        for key in set(cnt.keys()) & set(total.keys()):
            if total[key] != 0:
                dct[key] = round(cnt[key] / total[key], 2)
            else:
                dct[key] = None
        return dct

    def _date_histogram_converter(
        self, histograms: List, histogram_buckets: List[str]
    ) -> Dict:
        date_histogram = {}
        for item in histograms:
            date_id = item["_id"]
            date_key = self._date_histogram_bin_format(
                day=date_id["day"], month=date_id["month"], year=date_id["year"]
            )
            date_histogram[date_key] = item["count"]

        for histogram_bucket in histogram_buckets:
            if histogram_bucket not in date_histogram:
                date_histogram[histogram_bucket] = 0

        return date_histogram


    @property
    def metric_name(self) -> str:
        return "classification_date_hist"

    def _histogram_ratio(
        self, numerators: List, denominators: List, histogram_buckets: List[str]
    ) -> Dict:
        is_match_count_date_hist = self._date_histogram_converter(
            numerators, histogram_buckets
        )
        total_hist_date_hist = self._date_histogram_converter(
            denominators, histogram_buckets
        )
        return self._dict_day_ratio(is_match_count_date_hist, total_hist_date_hist)

    @staticmethod
    def _precision(true_positive_hist: Dict, false_positive_hist: Dict) -> Dict:
        precision_hist = {}
        for key, tp_value in true_positive_hist.items():
            fp_value = false_positive_hist[key]
            if tp_value is not None and fp_value is not None:
                numerator = tp_value + fp_value
                if numerator != 0:
                    precision = tp_value / (tp_value + fp_value)
                    precision_hist[key] = precision
                else:
                    precision_hist[key] = None
            else:
                precision_hist[key] = None
        return precision_hist

    @staticmethod
    def _recall(true_positive_hist: Dict, false_negative_hist: Dict) -> Dict:
        precision_hist = {}
        for key, tp_value in true_positive_hist.items():
            fn_value = false_negative_hist[key]
            if tp_value is not None and fn_value is not None:
                numerator = tp_value + fn_value
                if numerator != 0:
                    precision = tp_value / (tp_value + fn_value)
                    precision_hist[key] = precision
                else:
                    precision_hist[key] = None
            else:
                precision_hist[key] = None
        return precision_hist

    @staticmethod
    def _sensitivity(true_positive_hist: Dict, false_negative_hist: Dict) -> Dict:
        precision_hist = {}
        for key, tp_value in true_positive_hist.items():
            fn_value = false_negative_hist[key]
            if tp_value is not None and fn_value is not None:
                numerator = tp_value + fn_value
                if numerator != 0:
                    precision = tp_value / (tp_value + fn_value)
                    precision_hist[key] = precision
                else:
                    precision_hist[key] = None
            else:
                precision_hist[key] = None
        return precision_hist

    @staticmethod
    def _specificity(true_negative_hist: Dict, false_positive_hist: Dict) -> Dict:
        precision_hist = {}
        for key, tn_value in true_negative_hist.items():
            fp_value = false_positive_hist[key]
            if tn_value is not None and fp_value is not None:
                numerator = tn_value + fp_value
                if numerator != 0:
                    precision = tn_value / (tn_value + fp_value)
                    precision_hist[key] = precision
                else:
                    precision_hist[key] = None
            else:
                precision_hist[key] = None
        return precision_hist

    @staticmethod
    def _f1(precision_hist: Dict, recall_hist: Dict) -> Dict:
        f1_hist = {}
        for key, precision_value in precision_hist.items():
            recall_value = recall_hist[key]
            if precision_value is not None and recall_value is not None:
                numerator = precision_value + recall_value
                if numerator != 0:
                    f1 = 2 * (precision_value * recall_value) / numerator
                    f1_hist[key] = round(f1, 2)
                else:
                    f1_hist[key] = None
            else:
                f1_hist[key] = None
        return f1_hist

    def aggregation_result(self, time_range: TimeRange, **kwargs) -> Dict[str, Any]:
        hist_buckets = self._get_date_hist_bins(time_range=time_range)
        agg_query = self._aggregation_query(
            positive_class=self._positive_class,
            time_filter=self._time_filter_builder(time_range=time_range),
            **kwargs,
        )

        facets = self._collection.aggregate(agg_query).next()

        total_hist = facets["total_hist"]

        accuracy = self._histogram_ratio(
            facets["is_match_count_hist"], total_hist, hist_buckets
        )
        true_positive = self._histogram_ratio(
            facets["tp_count_hist"], total_hist, hist_buckets
        )
        false_negative = self._histogram_ratio(
            facets["fn_count_hist"], total_hist, hist_buckets
        )
        true_negative = self._histogram_ratio(
            facets["tn_count_hist"], total_hist, hist_buckets
        )
        false_positive = self._histogram_ratio(
            facets["fp_count_hist"], total_hist, hist_buckets
        )
        precision = self._precision(
            true_positive_hist=true_positive, false_positive_hist=false_positive
        )
        recall = self._recall(
            true_positive_hist=true_positive, false_negative_hist=false_negative
        )
        sensitivity = self._sensitivity(
            true_positive_hist=true_positive, false_negative_hist=false_negative
        )
        specificity = self._specificity(
            true_negative_hist=true_negative, false_positive_hist=false_positive
        )
        f1 = self._f1(precision_hist=precision, recall_hist=recall)

        date_hist_metrics: Dict[str, Dict] = {
            "accuracy": accuracy,
            "true_positive": true_positive,
            "false_negative": false_negative,
            "true_negative": true_negative,
            "false_positive": false_positive,
            "precision": precision,
            "recall": recall,
            "sensitivity": sensitivity,
            "specificity": specificity,
            "f1": f1,
        }

        return date_hist_metrics

    def _aggregation_query(
        self,
        time_filter: Dict,
        positive_class: str,
        class_position: int = 0,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        count_group_query = {
            "$group": {
                "_id": {"year": "$year", "month": "$month", "day": "$day"},
                "count": {"$sum": 1},
            }
        }
        facets = {
            "total_hist": [count_group_query],
            "is_match_count_hist": [{"$match": {"is_match": True}}, count_group_query],
            "tp_count_hist": [
                {
                    "$match": {
                        f"prediction_cf.{class_position}": positive_class,
                        f"actual_cf.{class_position}": positive_class,
                    }
                },
                count_group_query,
            ],
            "fn_count_hist": [
                {
                    "$match": {
                        f"prediction_cf.{class_position}": {"$ne": positive_class},
                        f"actual_cf.{class_position}": positive_class,
                    }
                },
                count_group_query,
            ],
            "tn_count_hist": [
                {
                    "$match": {
                        f"prediction_cf.{class_position}": {"$ne": positive_class},
                        f"actual_cf.{class_position}": {"$ne": positive_class},
                    }
                },
                count_group_query,
            ],
            "fp_count_hist": [
                {
                    "$match": {
                        f"prediction_cf.{class_position}": positive_class,
                        f"actual_cf.{class_position}": {"$ne": positive_class},
                    }
                },
                count_group_query,
            ],
        }

        return [
            {
                "$match": {
                    "dataset_id": str(self._dataset_id),
                    **(time_filter if time_filter is not None else {}),
                }
            },
            {
                "$addFields": {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"},
                    "day": {"$dayOfMonth": "$created_at"},
                }
            },
            {"$facet": facets},
        ]
