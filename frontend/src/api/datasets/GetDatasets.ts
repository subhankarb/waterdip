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
  version_id: string;
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

export const useGetDatasets = (params : GetDatasetParams) => {

  async function queryDataset() {
    const apiParams = {
      model_version_id: params.version_id
    };
    const response = await axios.get<GetDatasetResponse>(
      GET_DATASETS_API,
       { 
         params: apiParams
       }
    );
    return response;
  }
  return useQuery(['models', params], queryDataset, {
    refetchOnWindowFocus: false
  });

};
