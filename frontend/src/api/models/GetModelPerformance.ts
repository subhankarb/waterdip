import { useQuery, UseQueryResult } from 'react-query';
import axios from '../../utils/axios';
import { GET_MODEL_PERFORMANCE_API } from '../apis';
// import { ModelPerformance } from '../../@types/model';

interface GetModelInfoParams {
  id: string;
  start_date?: Date | null;
  end_date?: Date | null;
}

interface ApiAccuracyInfo {
  time_buckets: Array<string>;
  accuracy_data: Array<number>;
  perf_breakdown: {
    name: string;
    hist_values: Array<number>;
    buckets: Array<string>;
    impact: number;
  }[];
}
interface GetModelInfoResponse {
  model_id: string;
  accuracy: ApiAccuracyInfo;
}
// interface ResultData {
//   modelPerformance: ModelPerformance;
//   data: GetModelPerformanceResponse;
//   status: number;
//   statusText: string;
//   headers: any;
//   config: AxiosRequestConfig;
//   request?: any;
// }

// type ModelPerformanceQuery = UseQueryResult<ResultData, unknown>;
type ModelPerformanceQuery = UseQueryResult<any, unknown>;

interface UseModelPerformance {
  (params: GetModelInfoParams): ModelPerformanceQuery;
}

export const useModelPerformance: UseModelPerformance = (params) => {
  return useQuery(['model.performance', params], queryModelPerformance, {
    refetchOnWindowFocus: false
  });

  async function queryModelPerformance() {
    const apiParams = {
      model_version_id:params.id,
      start_date: params.start_date,
      end_date: params.end_date
    };
    const response = await axios.get<GetModelInfoResponse>(
      `${GET_MODEL_PERFORMANCE_API}/`,
      {
        params: apiParams
      }
    );
    const { model_id } = response.data;

    const modelPerformance: any = {
      id: model_id
    };

    return { ...response, modelPerformance };
  }
};
