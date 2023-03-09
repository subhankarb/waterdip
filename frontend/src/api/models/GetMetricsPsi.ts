import { useQuery, UseQueryResult } from 'react-query';
import axios from '../../utils/axios';
import { GET_METRICS_PSI } from '../apis';

interface GetMetricsPsiResponse {
    description?: any;
    drift_psi: Array<any>
}

interface GetMetricsPsiParams {
  model_id: string,
  model_version_id: string,
  start_time: Date | null,
  end_time: Date | null
}

type MetricsPsiQuery = UseQueryResult<any, unknown>;

interface UseMetricsPsi {
  (params: GetMetricsPsiParams): MetricsPsiQuery;
}

export const useMetricsPsi: UseMetricsPsi  = (params) => {

  return useQuery(['metric.psi', params], queryModels, {
    refetchOnWindowFocus: false
  });

  async function queryModels() {
    try {
        const response = await axios.get<GetMetricsPsiResponse>(
            GET_METRICS_PSI, { params }
          );
        return response.data;
    } catch (error) {
        throw error;
    }
  }
};
