import { useQuery, UseQueryResult } from 'react-query';
import { AxiosRequestConfig } from 'axios';
import axios from '../../utils/axios';
import { GET_DATASETS_API } from '../apis';
import { DatasetListMeta } from '../../@types/dataset';

interface ApiDatasetList {
  dataset_id: string;
  dataset_name: string;
}

interface GetDatasetParams {
  page: number;
  limit: number;
  sort: string;
  query: string;
  model_id: string;
}

interface GetDatasetResponse {
  dataset_list: ApiDatasetList[];
  meta: DatasetListMeta;
}

interface ResultData {
  dataset_list: any;
  meta: DatasetListMeta;
  data: GetDatasetResponse;
  status: number;
  statusText: string;
  headers: any;
  config: AxiosRequestConfig;
  request?: any;
}

type DatasetQuery = UseQueryResult<ResultData>;

interface DatasetsType {
  (params: GetDatasetParams): DatasetQuery;
}

export const useGetDatasets: DatasetsType = (params) => {
  return useQuery(['models', params], queryDataset, {
    refetchOnWindowFocus: false
  });

  async function queryDataset() {
    const response = await axios.get<GetDatasetResponse>(GET_DATASETS_API, { params });

    const { dataset_list, meta } = response.data;

    const datasetListMeta: DatasetListMeta = {
      page: meta?.page || 1,
      limit: meta?.limit || 10,
      total: meta?.total || 0,
      sort: meta?.sort || 'name_asc',
      query: meta?.query || '',
      model_id: meta?.model_id
    };

    return {
      dataset_list,
      meta: datasetListMeta
    };
  }
};
