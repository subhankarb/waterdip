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
