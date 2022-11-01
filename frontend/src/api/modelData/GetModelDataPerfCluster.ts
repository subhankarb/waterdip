import { useQuery, UseQueryResult } from 'react-query';
import { AxiosRequestConfig } from 'axios';
import axios from '../../utils/axios';
import { GET_MODEL_DATA_PERF_CLUSTER_API } from '../apis';
import { ModelDataPerformanceCluster } from '../../@types/model';

interface GetModelDataPerfClusterParams {
  id: string;
  start_time: Date | null;
  end_time: Date | null;
}

interface GetModelDataPerfClusterResponse {
  clusters?: Record<
    string,
    {
      cluster_id: string;
      serving_count: number;
      training_boundary: {
        x: number;
        y: number;
      }[];
      serving_data: {
        x: number;
        y: number;
      }[];
    }
  >;
}

interface ResultData {
  modelDataPerfCluster: ModelDataPerformanceCluster;
  data: GetModelDataPerfClusterResponse;
  status: number;
  statusText: string;
  headers: any;
  config: AxiosRequestConfig;
  request?: any;
}

type ModelDataPerfClusterQuery = UseQueryResult<ResultData, unknown>;

interface UseModelDataPerfCluster {
  (params: GetModelDataPerfClusterParams): ModelDataPerfClusterQuery;
}

export const useModelDataPerfCluster: UseModelDataPerfCluster = (params) => {
  return useQuery(['model.data.perf.cluster', params], queryModelPerformance, {
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
    const response = await axios.post<GetModelDataPerfClusterResponse>(
      GET_MODEL_DATA_PERF_CLUSTER_API,
      reqBody,
      {
        params: reqParams
      }
    );
    const { clusters } = response.data;

    const modelDataPerfCluster: ModelDataPerformanceCluster = {
      clusters: clusters
        ? Object.entries(clusters).reduce(
            (acc, [key, value]) => ({
              ...acc,
              [key]: {
                clusterId: value?.cluster_id || '',
                servingCount: value?.serving_count || 0,
                trainingBoundary: value?.training_boundary || [],
                servingData: value?.serving_data || []
              }
            }),
            {}
          )
        : {}
    };

    return { ...response, modelDataPerfCluster };
  }
};
