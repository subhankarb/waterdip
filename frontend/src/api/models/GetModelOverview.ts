import { useQuery, UseQueryResult } from 'react-query';
import axios from '../../utils/axios';
import { CREATE_MODEL_ANOMALOUS_EXPORT, GET_MODEL_Overview_API } from '../apis';
import { Model, ModelFeatures, data_type, ModelTasksStat } from '../../@types/model';

interface GetModelInfoParams {
  id: string;
  start_date?: Date | null;
  end_date?: Date | null;
}

interface ApiModelInfo {
  model_name: string;
  model_type: string;
  data_type: data_type;
  task_type: string;
  description: string;
}

interface GetModelInfoResponse {
  model_id: string;
  model_details: ApiModelInfo;
  model_alerts: any;
  model_prediction_graph: any;
  model_predictions: any;
}

type ModelInfoQuery = UseQueryResult<any, unknown>;

interface UseModelInfo {
  (params: GetModelInfoParams): ModelInfoQuery;
}

export const useModelInfo: UseModelInfo = (params) => {
  return useQuery(['model.info', params], queryModels, {
    refetchOnWindowFocus: false
  });

  async function queryModels() {
    const apiParams = {
      start_date: params.start_date,
      end_date: params.end_date
    };
    const response = await axios.get<GetModelInfoResponse>(
      `${GET_MODEL_Overview_API}/${params.id}`,
      {
        params: apiParams
      }
    );
    const {
      model_id,
      model_details: { model_name, model_type, description, data_type }
    } = response.data;

    const modelInfo: any = {
      id: model_id,
      name: model_name,
      modelType: model_type,
      dataType: data_type,
      description
    };

    return {
      ...response,
      modelInfo
    };
  }
};
