import { useQuery, UseQueryResult } from 'react-query';
import { AxiosRequestConfig } from 'axios';
import axios from '../../utils/axios';
import { GET_MODELS_API } from '../apis';
import { ModelListRow, ModelPredictions, data_type, ModelListMeta } from '../../@types/model';

interface ApiModelList {
  model_id: string;
  model_version_id: string;
  model_name: string;
  org_id: string;
  description: string;
  predictions: ModelPredictions;
  data_type: data_type;
  task_type: string;
  created_at: string;
  total_predictions: string;
  num_alert_perf: string;
  num_alert_data_behave: string;
  num_alert_data_integrity: string;
  last_prediction: string;
}

interface GetModelsParams {
  page: number;
  limit: number;
  sort: string;
  query: string;
}

interface GetModelsResponse {
  model_list: ApiModelList[];
  meta: ModelListMeta;
}

interface ResultData {
  modelList: ModelListRow[];
  meta: ModelListMeta;
  data: GetModelsResponse;
  status: number;
  statusText: string;
  headers: any;
  config: AxiosRequestConfig;
  request?: any;
}

type ModelQuery = UseQueryResult<ResultData>;

interface UsePaginatedModels {
  (params: GetModelsParams): ModelQuery;
}

export const usePaginatedModels: UsePaginatedModels = (params) => {
  return useQuery(['models', params], queryModels, {
    refetchOnWindowFocus: false
  });

  async function queryModels() {
    const response = await axios.get<GetModelsResponse>(GET_MODELS_API, { params });
    const { model_list, meta } = response.data;
    console.log(model_list);
    const modelList = model_list.map(
      (model: ApiModelList): ModelListRow => ({
        id: model.model_id,
        version_id: model.model_version_id,
        name: model.model_name,
        dataType: model.data_type,
        // orgId: model.org_id,
        description: model.description,
        predictions: model.predictions,
        createdAt: model.created_at,
        totalPredictions: model.total_predictions,
        alertPerf: model.num_alert_perf,
        alertDataBehave: model.num_alert_data_behave,
        alertDataIntegrity: model.num_alert_data_integrity,
        lastPrediction: model.last_prediction
      })
    );

    const modelListMeta: ModelListMeta = {
      page: meta?.page || 1,
      limit: meta?.limit || 10,
      total: meta?.total || 0,
      sort: meta?.sort || 'name_asc',
      query: meta?.query || ''
    };

    return {
      ...response,
      modelList,
      meta: modelListMeta
    };
  }
};
