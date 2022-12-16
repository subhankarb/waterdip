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

from typing import Any, Dict, List
from uuid import UUID

from pymongo.collection import Collection

from waterdip.core.metrics.base import MongoMetric


class HistogramCategoricalFeatures(MongoMetric):
    """
    The categorical histogram feature measures count of each categorical column.

    ...

    Attributes:
    -----
    collection: Collection
        mongo collection
    dataset_id: UUID
        dataset id on which the metric calculation will be applied

    Methods:
    --------
    aggregation_result()
        returns aggrated metrics agg by categorical column names

    Examples:
        >>> from waterdip.core.metrics.batch_dataset import HistogramCategoricalFeatures
        >>> DATASET_BATCH_ID_V2_3 = UUID("1d195bf6-7a1f-4a33-b7b1-37a603aadd33")
        >>> mongo_collection: Collection
        >>>
        >>> hist = HistogramCategoricalFeatures(
        >>>     collection=mongo_collection,
        >>>     dataset_id=DATASET_BATCH_ID_V2_3,
        >>> )
        >>> hist_result = hist.aggregation_result() # returns histogram result
        >>> # res structure -> [{"column_name": "<name>", "bins": ["<bin1>"], "count": ["<bin1_count>"]}]
    """

    def __init__(self, collection: Collection, dataset_id: UUID):
        super().__init__(collection)
        self._dataset_id = dataset_id

    @property
    def metric_name(self) -> str:
        return "batch_hist_cat_features"

    def aggregation_result(self) -> Dict[str, Any]:
        hist = {}
        for doc in self._collection.aggregate(self._aggregation_query()):
            column_name = doc["_id"]["column_name"]
            column_value = doc["_id"]["column_value"]
            count = doc["count"]
            if column_name not in hist:
                hist[column_name] = {"type": "CATEGORICAL", "bins": [], "count": []}
            hist[column_name]["bins"].append(column_value)
            hist[column_name]["count"].append(count)
        return hist

    def _aggregation_query(self) -> List[Dict[str, Any]]:
        return [
            {"$match": {"dataset_id": str(self._dataset_id)}},
            {"$unwind": "$columns"},
            {"$match": {"columns.data_type": "CATEGORICAL"}},
            {
                "$group": {
                    "_id": {
                        "column_name": "$columns.name",
                        "column_value": "$columns.value_categorical",
                    },
                    "count": {"$sum": 1},
                }
            },
        ]
