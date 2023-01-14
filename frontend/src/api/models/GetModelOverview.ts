import { useQuery, UseQueryResult } from 'react-query';
import axios from '../../utils/axios';
import { GET_MODEL_Overview_API } from '../apis';
import { data_type } from '../../@types/model';

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

interface ModelPredictionOverview {
  pred_yesterday: number;
  pred_percentage_change: number;
  pred_trend_data: Array<number>;
  pred_average: number;
  pred_average_window_days: number;
}

interface Predictions{
  date_bins: Array<string>;
  val: Array<number>;
}
interface ModelPredictionHist{
  predictions: Predictions;
  predictions_versions: any;
}

interface ModelAlertOverview {
  alerts_count: number;
  alert_percentage_change: number;
  alert_trend_data: Array<number>;
}

interface ModelAlertList {
  alert_id: string;
  monitor_name: string;
  monitor_type: string;
  created_at: string;
}
interface GetModelOverviewResponse {
  model_id: string;
  model_prediction_overview: ModelPredictionOverview;
  model_prediction_hist: ModelPredictionHist;
  model_alert_overview: ModelAlertOverview;
  model_alert_list: Array<ModelAlertList>;
  number_of_model_versions: number;
  latest_version_created_at: string;
  latest_version: any;
}

type ModelInfoQuery = UseQueryResult<any, unknown>;

interface UseModelOverview {
  id: string;
}

export const useModelOverview  = (params: UseModelOverview) => {
  return useQuery(['model.overview', params], queryModels, {
    refetchOnWindowFocus: false
  });

  async function queryModels() {
    const apiParams = {
      model_id: params.id
    };
    const response = await axios.get<GetModelOverviewResponse>(
      GET_MODEL_Overview_API,
      {
        params: apiParams
      }
    );
    return response;
    
  }
};
