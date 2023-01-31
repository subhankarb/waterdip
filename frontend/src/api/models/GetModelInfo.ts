import { useQuery, UseQueryResult } from 'react-query';
import axios from '../../utils/axios';
import { GET_MODEL_Info_API } from '../apis';
import { data_type } from '../../@types/model';
import { useState } from 'react';

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
  model_name: string;
  model_versions: any;
  model_details: ApiModelInfo;
  model_alerts: any;
  model_prediction_graph: any;
  model_predictions: any;
}

type ModelInfoQuery = UseQueryResult<any, unknown>;

interface UseModelInfo {
  id: string;
}

export const useModelInfo  = (params: UseModelInfo) => {
  return useQuery(['model.info', params], queryModels, {
    refetchOnWindowFocus: false
  });

  async function queryModels(): Promise<{} | any> {
    const apiParams = {
      model_id: params.id
    };
    try {
      const response = await axios.get<GetModelInfoResponse>(
        GET_MODEL_Info_API,
        {
          params: apiParams
        }
      );
      return response;
    } catch (err) {
      return {};
    }
  }
};
