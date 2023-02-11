import { useQuery, UseQueryResult } from 'react-query';
import axios from '../../utils/axios';
import { GET_MODEL_PERFORMANCE_API } from '../apis';
// import { ModelPerformance } from '../../@types/model';

interface GetModelInfoParams {
  model_id: string;
  model_version_id: string;
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
  return useQuery(['metric.performance', params], queryModelPerformance, {
    refetchOnWindowFocus: false
  });

  async function queryModelPerformance() {
    const apiParams = {
      model_id: params.model_id,
      model_version_id:params.model_version_id,
      start_date: params.start_date,
      end_date: params.end_date
    };
    try{
      const response = await axios.get<GetModelInfoResponse>(
        `${GET_MODEL_PERFORMANCE_API}/`,
        {
          params: apiParams
        }
      )
      console.log(response);
      return response;
    } catch (error) {
      throw error;
    }
    
  }
};