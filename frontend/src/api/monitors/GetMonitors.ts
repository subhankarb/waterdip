import { useQuery, UseQueryResult } from 'react-query';
import axios from '../../utils/axios';
import { GET_MONITORS_API } from '../apis';

interface MonitorsList {
    monitor_id: string,
    monitor_name: string,
    monitor_type: string,
    monitor_identification: {
        model_version_id: string,
        model_id: string,
    },
    monitor_condition: {
        evaluation_metric: string,
        dimensions?: any,
        threshold?: any,
        evaluation_window: string,
        baseline?: any
    },
}


interface GetMonitorsResponse {
  monitor_list: Array<MonitorsList>;
  meta: any;
}


interface UseMonitors {
  model_id ?: string;
  model_version_id ?: string;
  page ?: number;
  limit ?: number;
  sort ?: string;
  query ?: string;
}

export const useGetMonitors  = (params: UseMonitors) => {
  return useQuery(['list.monitors', params], queryModels, {
    refetchOnWindowFocus: false
  });

  async function queryModels() {
    const apiParams = {
        model_id: params.model_id,
        model_version_id: params.model_version_id,
        page: params.page,
        limit: params.limit,
        sort: params.sort,
        query: params.query
    };
    const response = await axios.get<GetMonitorsResponse>(
      GET_MONITORS_API,
      {
        params: apiParams
      }
    );
    return response;
    
  }
};
