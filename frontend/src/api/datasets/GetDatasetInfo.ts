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
import { GET_DATASET_INFO_API } from '../apis';
import { Optional } from 'react-wordcloud';
import { paramCase } from 'change-case';
const BASE_URL = process.env.REACT_APP_API_URL;

interface DatasetOverview {
  dataset_name: string;
  dataset_id: string;
  total_row: number;
  missing_total: number;
  missing_percentage: number;
  duplicate_total: number;
  duplicate_percentage: number;
}

interface Histogram {
  bins: string[];
  val: string[];
}

interface NumericColumnStats {
  column_name: string;
  histogram: Histogram;
  zeros_total: number;
  missing_total: number;
  missing_percentage: number;
  mean: number;
  median: number;
  standard_deviation: number;
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
  dataset_overview: DatasetOverview;
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

interface GetDetasetInfoParams {
  dataset_id: string;
  start_date?: Date | null;
  end_date?: Date | null;
}

type DatasetQuery = UseQueryResult<ResultData>;

interface DatasetsType {
  (params: GetDetasetInfoParams): DatasetQuery;
}

export const useGetDatasetsInfo = ({ dataset_id, start_date, end_date }: GetDetasetInfoParams) => {
  console.log(dataset_id);
  return useQuery([dataset_id], queryDataset, {
    refetchOnWindowFocus: false
  });
  async function queryDataset() {
    console.log(`${GET_DATASET_INFO_API}/${dataset_id}`);
    const apiParams = {
      start_date: start_date,
      end_date: end_date
    };
    const response = await axios.get<DatasetInfoResponse>(`${GET_DATASET_INFO_API}/${dataset_id}`, {
      params: apiParams
    });

    const { dataset_overview, numeric_column_stats, categorical_column_stats } = response.data;

    return {
      dataset_overview,
      numeric_column_stats,
      categorical_column_stats
    };
  }
};
