/*
 *  Copyright 2022-present, the Waterdip Labs Pvt. Ltd.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 */

import { useQuery, UseQueryResult } from 'react-query';
import { AxiosRequestConfig } from 'axios';
import axios from '../../utils/axios';
import { GET_METRICS_DATASET } from '../apis';
import { Optional } from 'react-wordcloud';
import { paramCase } from 'change-case';
const BASE_URL = process.env.REACT_APP_API_URL;


interface Histogram {
  bins: string[];
  val: string[];
}

interface NumericColumnStats {
  column_name: string;
  histogram: Histogram;
  zeros: number;
  missing_total: number;
  missing_percentage: number;
  mean: number;
  std_dev: number;
  min: number;
  max: number;
}

interface CategoricalColumnStats {
  column_name: string;
  histogram: Histogram;
  missing_total: number;
  missing_percentage: number;
  unique: number;
  top: string;
}

interface DatasetInfoResponse {
  numeric_column_stats: NumericColumnStats[];
  categorical_column_stats: CategoricalColumnStats[];
}

interface ResultData {
  dataset_info: any;
  data: DatasetInfoResponse;
  status: number;
  statusText: string;
  headers: any;
  config: AxiosRequestConfig;
  request?: any;
}

interface GetMetricsDatasetParams {
  model_id: string;
  model_version_id: string;
  dataset_id: string;
  start_date?: Date | null;
  end_date?: Date | null;
}


export const useGetMetricsDataset = ({model_id, model_version_id, dataset_id, start_date, end_date }: GetMetricsDatasetParams) => {
  return useQuery([dataset_id], queryDataset, {
    refetchOnWindowFocus: false
  });
  async function queryDataset() {
    const apiParams = {
      model_id: model_id,
      model_version_id: model_version_id, 
      dataset_id: dataset_id,
      start_date: start_date,
      end_date: end_date
    };
    const response = await axios.get<DatasetInfoResponse>(GET_METRICS_DATASET, {
      params: apiParams
    });

    return response;
  }
};
