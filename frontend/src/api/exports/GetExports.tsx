import { useQuery, UseQueryResult } from 'react-query';
import { AxiosRequestConfig } from 'axios';
import { ExportListRow, ModelListMeta, ModelListRow } from '../../@types/model';
import axios from '../../utils/axios';
import { GET_MODEL_DATA_EXPORT_LIST } from '../apis';

interface GetExportParams {
  page: number;
  limit: number;
  model_id: string;
  sort: string;
  query: string;
}

interface ApiExportListRow {
  model_id: string;
  id: string;
  type: string;
  status: string;
  object_id: string;
  object_url: string;
  created_at: string;
  total_predictions: string;
  num_alert_perf: string;
  num_alert_data_behave: string;
  num_alert_data_integrity: string;
  last_prediction: string;
}

interface GetExportsResponse {
  export_list: ApiExportListRow[];
  meta: ModelListMeta;
}

interface ResultData {
  exportList: ExportListRow[];
  meta: ModelListMeta;
  data: GetExportsResponse;
  status: number;
  statusText: string;
  headers: any;
  config: AxiosRequestConfig;
  request?: any;
}

type ExportQuery = UseQueryResult<ResultData>;

interface UsePaginateExports {
  (params: GetExportParams): ExportQuery;
}

export const usePaginateExports: UsePaginateExports = (params) => {
  return useQuery(['model.export.list', params], queryExports, {
    refetchOnWindowFocus: false
  });

  async function queryExports() {
    const response = await axios.get<GetExportsResponse>(GET_MODEL_DATA_EXPORT_LIST, { params });

    const { export_list, meta } = response.data;

    const exportList = export_list.map(
      (export_row: ApiExportListRow): ExportListRow => ({
        id: export_row.id,
        model_id: export_row.model_id,
        type: export_row.type,
        status: export_row.status,
        object_id: export_row.object_id,
        object_url: export_row.object_url,
        created_at: export_row.created_at,
        total_predictions: export_row.total_predictions,
        num_alert_perf: export_row.num_alert_perf,
        num_alert_data_behave: export_row.num_alert_data_behave,
        num_alert_data_integrity: export_row.num_alert_data_integrity,
        last_prediction: export_row.last_prediction
      })
    );

    const exportListMeta: ModelListMeta = {
      page: meta?.page || 0,
      limit: meta?.limit || 1,
      total: meta?.total || 0,
      sort: meta?.sort || 'name_asc',
      query: meta?.query || ''
    };

    return {
      ...response,
      exportList,
      meta: exportListMeta
    };
  }
};
