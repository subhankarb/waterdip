import { useQuery, UseQueryResult } from 'react-query';
import { AxiosRequestConfig } from 'axios';
import axios from '../../utils/axios';
import { GET_MODEL_DATA_PERF_ANOMALOUS_API } from '../apis';
import { AnomalousMeta, ModelDataPerformanceAnomalous } from '../../@types/model';

interface GetModelDataPerfAnomalousParams {
  id: string;
  start_time: Date | null;
  end_time: Date | null;
  limit: number;
  page: number;
  sort: string;
}

interface GetModelDataPerfAnomalousResponse {
  clusters?: Record<
    string,
    {
      x: number;
      y: number;
    }[]
  >;
  anomalous?: {
    x: number;
    y: number;
  }[];
  total?: number;
  data?: string[];
  data_dict?: Record<string, Record<string, string>[]>;
  row_names?: string[];
  data_list?: Record<string, string | number>[];
  meta?: AnomalousMeta;
}

interface ResultData {
  modelDataPerfAnomalous: ModelDataPerformanceAnomalous;
  data: GetModelDataPerfAnomalousResponse;
  status: number;
  statusText: string;
  headers: any;
  config: AxiosRequestConfig;
  request?: any;
}

type ModelDataPerfAnomalousQuery = UseQueryResult<ResultData, unknown>;

interface UseModelDataPerfAnomalous {
  (params: GetModelDataPerfAnomalousParams): ModelDataPerfAnomalousQuery;
}

export const useModelDataPerfAnomalous: UseModelDataPerfAnomalous = (params) => {
  return useQuery(['model.data.perf.anomalous', params], queryModelPerformance, {
    refetchOnWindowFocus: false
  });

  async function queryModelPerformance() {
    const reqParams = {
      model_id: params.id
    };
    const reqBody = {
      start_time: params.start_time,
      end_time: params.end_time,
      limit: params.limit,
      page: params.page,
      sort: params.sort
    };
    const response = await axios.post<GetModelDataPerfAnomalousResponse>(
      GET_MODEL_DATA_PERF_ANOMALOUS_API,
      reqBody,
      {
        params: reqParams
      }
    );
    const { clusters, anomalous, total, data, data_dict, row_names, data_list } = response.data;

    const modelDataPerfAnomalous: ModelDataPerformanceAnomalous = {
      clusters: clusters
        ? Object.entries(clusters).reduce(
            (acc, [key, value]) => ({
              ...acc,
              [key]: value ? value.map((val) => ({ x: val?.x || 0, y: val?.y || 0 })) : []
            }),
            {}
          )
        : {},
      anomalous: anomalous || [],
      total: total || 0,
      data: data || [],
      row_names: row_names || [],
      data_list: data_list || [],
      data_dict: data_dict
        ? Object.entries(data_dict).reduce(
            (acc, [key, value]) => ({
              ...acc,
              [key]:
                value && value.length > 0
                  ? value.map((valueObj) =>
                      valueObj
                        ? Object.entries(value[0]).reduce(
                            (value_acc, [val_key, val_value]) => ({
                              ...value_acc,
                              [val_key]: val_value || ''
                            }),
                            {}
                          )
                        : {}
                    )
                  : []
            }),
            {}
          )
        : {}
    };

    return { ...response, modelDataPerfAnomalous };
  }
};
