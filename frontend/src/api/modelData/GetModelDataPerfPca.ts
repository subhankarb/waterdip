import { useQuery, UseQueryResult } from 'react-query';
import { AxiosRequestConfig } from 'axios';
import axios from '../../utils/axios';
import { GET_MODEL_DATA_PERF_PCA_API } from '../apis';
import { ModelDataPerformancePca } from '../../@types/model';

interface GetModelDataPerfPcaParams {
  id: string;
  start_time: Date | null;
  end_time: Date | null;
}

interface GetModelDataPerfPcaResponse {
  components?: {
    name: string;
    bin_keys: string[];
    serving: number[];
    training: number[];
  }[];
}

interface ResultData {
  modelDataPerfPca: ModelDataPerformancePca;
  data: GetModelDataPerfPcaResponse;
  status: number;
  statusText: string;
  headers: any;
  config: AxiosRequestConfig;
  request?: any;
}

type ModelDataPerfPcaQuery = UseQueryResult<ResultData, unknown>;

interface UseModelDataPerfPca {
  (params: GetModelDataPerfPcaParams): ModelDataPerfPcaQuery;
}

export const useModelDataPerfPca: UseModelDataPerfPca = (params) => {
  return useQuery(['model.data.perf.pca', params], queryModelPerformance, {
    refetchOnWindowFocus: false
  });

  async function queryModelPerformance() {
    const reqParams = {
      model_id: params.id
    };
    const reqBody = {
      start_time: params.start_time,
      end_time: params.end_time
    };
    const response = await axios.post<GetModelDataPerfPcaResponse>(
      GET_MODEL_DATA_PERF_PCA_API,
      reqBody,
      {
        params: reqParams
      }
    );
    const { components } = response.data;

    const modelDataPerfPca: ModelDataPerformancePca = {
      components:
        components?.map((component) => ({
          name: component?.name || '',
          binKeys: component?.bin_keys || [],
          serving: component?.serving || [],
          training: component?.training || []
        })) || []
    };

    return { ...response, modelDataPerfPca };
  }
};
