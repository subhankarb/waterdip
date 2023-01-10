import { useQuery, UseQueryResult } from 'react-query';
import axios from '../../utils/axios';
import { GET_MODEL_VERSION_INFO_API } from '../apis';

interface FeaturesInfo{
    data_type: string;
    list_index: any;
}

interface TimeWindowInfo{
    skip_period: string;
    time_period: string;
    aggregation_period: string;
}
interface GetModelVersionInfo{
  model_version_id : string;
  model_version: string;
  model_id: string;
  description: string;
  task_type: string;
  created_at: string;
  version_schema: {
    features: {
            [key: string]: FeaturesInfo
    };
    predictions: {
            [key: string]: FeaturesInfo
    };
  };
  baseline: {
    time_window: TimeWindowInfo
  }
}

type ModelInfoQuery = UseQueryResult<any, unknown>;

interface UseModelInfo {
  (params: {model_version_id: string}): ModelInfoQuery;
}

export const useModelVersionInfo: UseModelInfo = (params) => {
  return useQuery(['model.version.info', params], queryModels, {
    refetchOnWindowFocus: false
  });

  async function queryModels() {
    const apiParams = {
        model_version_id: params.model_version_id
    };
    const response = await axios.get<GetModelVersionInfo>(
      `${GET_MODEL_VERSION_INFO_API}`,
      {
        params: apiParams
      }
    );
    return {
      ...response,
    };
  }
};
