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

import numpy as np
from pymongo.collection import Collection

from waterdip.core.commons.models import TimeRange
from waterdip.core.metrics.base import MongoMetric
from waterdip.core.metrics.data_metrics import (
    CategoricalCountHistogram,
    CategoricalNestedDateCountHistogram,
    NumericCountHistogram,
    NumericNestedCountDateHistogram,
)


class PSIMetrics(MongoMetric):
    """
    PSI Metrics

    This metric is used to calculate the PSI between two datasets.
    The baseline dataset is used to calculate the expected distribution of the data.
    The current dataset is used to calculate the actual distribution of the data.
    The PSI is calculated by comparing the expected and actual distribution of the data.
    The PSI is calculated for each categorical and numeric field in the dataset.

    The PSI is calculated using the following formula:
    PSI = SUM( (actual - expected) * log(actual / expected) )

    Attributes:
    ----------
    collection:
        The collection object for the production dataset
    dataset_id:
        The dataset id for the production dataset
    baseline_dataset_id:
        The dataset id for the baseline dataset
    baseline_collection:
        The collection object for the baseline dataset
    baseline_time_range:
        The time range for the baseline dataset
    """

    def __init__(
        self,
        collection: Collection,
        dataset_id: UUID,
        baseline_dataset_id: UUID,
        baseline_collection: Collection,
        baseline_time_range: TimeRange = None,
    ):
        super().__init__(collection)
        self._dataset_id = dataset_id

        self._baseline_dataset_id = baseline_dataset_id
        self._baseline_collection = baseline_collection
        self._baseline_time_range = baseline_time_range

        self._cat_count_date_histogram = CategoricalNestedDateCountHistogram(
            collection=self._collection, dataset_id=self._dataset_id
        )
        self._numeric_count_date_histogram = NumericNestedCountDateHistogram(
            collection=self._collection, dataset_id=self._dataset_id
        )

        self._cat_count_histogram_baseline = CategoricalCountHistogram(
            collection=self._baseline_collection, dataset_id=self._baseline_dataset_id
        )
        self._numeric_count_histogram_baseline = NumericCountHistogram(
            collection=self._baseline_collection, dataset_id=self._baseline_dataset_id
        )

    @property
    def metric_name(self) -> str:
        return "drift_psi"

    def _numeric_baseline_distribution(
        self, numeric_columns: List
    ) -> (Dict[str, Dict], Dict[str, List[str]]):
        """
        Will return count histogram for each feature
        Args:
            numeric_columns:
                List of numeric columns
        Returns:
            columns_histogram: Dict[str, Dict]
                Count histogram for each feature
            bins: Dict[str, List[str]]
                Bins for each numeric column
        """
        columns_histogram = self._numeric_count_histogram_baseline.aggregation_result(
            numeric_columns=numeric_columns, time_range=self._baseline_time_range
        )
        bins: Dict[str, List[str]] = {}
        for column_name, column_histogram in columns_histogram.items():
            bins[column_name] = column_histogram["bins"]

        return columns_histogram, bins

    def _numeric_production_distribution(
        self, numeric_columns: List, bins: Dict[str, List[str]], time_range: TimeRange
    ) -> Dict[str, Dict]:
        """
        Will return count histogram for each feature
        Args:
            numeric_columns:
                List of numeric columns
            bins:
                Bins for each numeric column, already calculated in baseline
            time_range:
                Time range for the production dataset

        Returns:
            columns_histogram: Dict[str, Dict]
                Count histogram for each feature
        """
        columns_histogram = self._numeric_count_date_histogram.aggregation_result(
            numeric_columns=numeric_columns, time_range=time_range, bins=bins
        )
        return columns_histogram

    def _categorical_baseline_distribution(self) -> Dict[str, Dict]:
        """
        Will return count histogram for each feature for the baseline dataset
        Returns:
            columns_histogram: Dict[str, Dict]
                Count histogram for each feature

        """
        return self._cat_count_histogram_baseline.aggregation_result(
            time_range=self._baseline_time_range
        )

    def _categorical_production_distribution(
        self, time_range: TimeRange
    ) -> Dict[str, Dict]:
        """
        Will return count histogram for each feature for the production dataset
        Args:
            time_range:
                Time range for the production dataset
        Returns:
            columns_histogram: Dict[str, Dict]
                Count histogram for each feature
        """
        return self._cat_count_date_histogram.aggregation_result(time_range=time_range)

    @staticmethod
    def count_to_density(count_array: List[int]) -> List[float]:
        """
        Will convert count array to density array
        Args:
            count_array: List[int]
                Count array
        Returns:
            density_array: List[float]
                Density array
        """
        array = np.array(count_array)
        total = np.sum(array)
        array = array / total
        return array.tolist()

    @staticmethod
    def psi_from_bins(baseline_density: List[float], production_density: List[float]):
        """
        Will calculate the PSI value from the density arrays.
        The PSI is calculated using the following formula:
        PSI = SUM( (actual - expected) * log(actual / expected) )

        Args:
            baseline_density: List[float]
                density array for the baseline dataset
            production_density: List[float]
                density array for the production dataset
        Returns:
            psi_value: float
        """
        return np.sum(
            [
                (n - b) * np.log(n / b)
                for b, n in zip(baseline_density, production_density)
            ]
        ).tolist()

    def _calculate_psi_value(
        self,
        columns: List[str],
        baseline_distribution: Dict[str, Dict],
        production_distribution: Dict[str, Dict],
    ) -> Dict:
        """
        Will calculate the PSI value for each column
        Args:
            columns: List[str]
                List of columns
            baseline_distribution: Dict[str, Dict]
                Baseline distribution
            production_distribution: Dict[str, Dict]
                Production distribution

        Returns:
            psi_values: Dict
                PSI value for each column

        """
        psi_values = {}
        for column in columns:
            if column in baseline_distribution and column in production_distribution:
                baseline_count_array = baseline_distribution[column]["count"]
                production_count_array = production_distribution[column]["count"]
                baseline_density = self.count_to_density(baseline_count_array)
                production_density = self.count_to_density(production_count_array)
                psi_value = self.psi_from_bins(
                    baseline_density=baseline_density,
                    production_density=production_density,
                )
                psi_values[column] = psi_value
        return psi_values

    def _psi_numeric_date_agg(
        self, numeric_columns: List, time_range: TimeRange
    ) -> Dict[str, Dict[str, float]]:
        """
        Will calculate the PSI value for each numeric column for
        each date in the production dataset
        Args:
            numeric_columns: List[str]
                List of numeric columns
            time_range: TimeRange
                Time range for the production dataset
        Returns:
            psi_numeric_date_agg: Dict[str, Dict[str, float]]
                PSI value for each numeric column for each date in the production dataset
        """
        psi_numeric_date_agg = {}

        numeric_baseline_distribution, bins = self._numeric_baseline_distribution(
            numeric_columns=numeric_columns
        )
        numeric_production_distribution_date_agg = (
            self._numeric_production_distribution(
                numeric_columns=numeric_columns, bins=bins, time_range=time_range
            )
        )

        for (
            date_str,
            numeric_production_distribution,
        ) in numeric_production_distribution_date_agg.items():
            numeric_psi_values_ny_columns = self._calculate_psi_value(
                columns=numeric_columns,
                baseline_distribution=numeric_baseline_distribution,
                production_distribution=numeric_production_distribution,
            )
            psi_numeric_date_agg[date_str] = numeric_psi_values_ny_columns
        return psi_numeric_date_agg

    def _psi_categorical_date_agg(
        self, categorical_columns: List, time_range: TimeRange
    ) -> Dict[str, Dict[str, float]]:
        """
        Will calculate the PSI value for each categorical column for each date in the production dataset
        Args:
            categorical_columns: List[str]
                List of categorical columns
            time_range: TimeRange
                Time range for the production dataset

        Returns: Dict[str, Dict[str, float]]
            PSI value for each categorical column for each date in the production dataset
        """
        psi_cat_date_agg = {}
        categorical_baseline_distribution = self._categorical_baseline_distribution()

        categorical_production_distribution_date_agg = (
            self._categorical_production_distribution(time_range=time_range)
        )

        for (
            date_str,
            categorical_production_distribution,
        ) in categorical_production_distribution_date_agg.items():
            categorical_psi_values_ny_columns = self._calculate_psi_value(
                columns=categorical_columns,
                baseline_distribution=categorical_baseline_distribution,
                production_distribution=categorical_production_distribution,
            )
            psi_cat_date_agg[date_str] = categorical_psi_values_ny_columns

        return psi_cat_date_agg

    def aggregation_result(
        self,
        numeric_columns: List,
        categorical_columns: List,
        time_range: TimeRange,
        **kwargs
    ) -> Dict[str, Dict[str, float]]:
        """
        Will calculate the PSI value for each column for each date in the production dataset


        Args:
            numeric_columns: List[str]
            categorical_columns: List[str]
            time_range: TimeRange
            **kwargs:

        Returns:
            psi_date_agg: Dict[str, Dict[str, float]]
                PSI value for each column for each date in the production dataset
        """
        psi_date_agg: Dict[str, Dict[str, float]] = {}

        psi_numeric_date_agg = self._psi_numeric_date_agg(
            numeric_columns=numeric_columns, time_range=time_range
        )
        pas_cat_date_agg = self._psi_categorical_date_agg(
            categorical_columns=categorical_columns, time_range=time_range
        )

        for date_str in time_range.get_date_list:
            psi_date_agg[date_str] = {}
            if date_str in psi_numeric_date_agg:
                psi_date_agg[date_str].update(psi_numeric_date_agg[date_str])
            if date_str in pas_cat_date_agg:
                psi_date_agg[date_str].update(pas_cat_date_agg[date_str])

        return psi_date_agg

    def _aggregation_query(self, *args, **kwargs) -> List[Dict[str, Any]]:
        pass

    @staticmethod
    def _average_psi_column_agg(calculate_psi_values: Dict[str, Dict[str, float]]):
        """
        Will calculate the average PSI value for each column
        Args:
            calculate_psi_values: Dict[str, Dict[str, float]]
                PSI value for each column for each date in the production dataset

        Returns:
            average_psi_column_agg: Dict[str, float]
                Average PSI value for each column
        """
        average_psi_column_agg = {}
        for date_str, psi_values in calculate_psi_values.items():
            for column, psi_value in psi_values.items():
                if column not in average_psi_column_agg:
                    average_psi_column_agg[column] = []
                average_psi_column_agg[column].append(psi_value)
        return {
            column: np.mean(psi_values).tolist()
            for column, psi_values in average_psi_column_agg.items()
        }

    @staticmethod
    def _average_psi_date_agg(calculate_psi_values: Dict[str, Dict[str, float]]):
        """
        Will calculate the average PSI value for each date
        Args:
            calculate_psi_values: Dict[str, Dict[str, float]]
                PSI value for each column for each date in the production dataset

        Returns:
            average_psi_date_agg: Dict[str, float]
                Average PSI value for each date
        """
        average_psi_date_agg = {}
        for date_str, psi_values in calculate_psi_values.items():
            average_psi_date_agg[date_str] = np.mean(list(psi_values.values()))
        return average_psi_date_agg
