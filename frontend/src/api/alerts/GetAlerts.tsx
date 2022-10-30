import { UseQueryResult, useQuery } from 'react-query';
import { AxiosRequestConfig } from 'axios';
import axios from '../../utils/axios';
import { GET_ALERTS_API } from '../apis';
import { AlertsListRow, AlertsListMeta } from '../../@types/alerts';

interface ApiAlertsList {
  monitor_id: string;
  monitor_name: string;
  monitor_method: string;
  model_id: string;
  severity: string;
  status: string;
  time: string;
}

interface GetAlertsParams {
  page: number;
  limit: number;
  sort: string;
  query: string;
}

interface GetAlertsResponse {
  alert_list: ApiAlertsList[];
  meta: AlertsListMeta;
}

interface ResultData {
  alertList: AlertsListRow[];
  meta: AlertsListMeta;
  data: GetAlertsResponse;
  status: number;
  statusText: string;
  headers: any;
  config: AxiosRequestConfig;
  request?: any;
}

type AlertsQuery = UseQueryResult<ResultData>;

interface UsePaginatedAlerts {
  (params: GetAlertsParams): AlertsQuery;
}

export const usePaginatedAlerts: UsePaginatedAlerts = (params) => {
  return useQuery(['alerts', params], queryAlerts, {
    refetchOnWindowFocus: false
  });

  async function queryAlerts() {
    const response = await axios.get<GetAlertsResponse>(GET_ALERTS_API, { params });

    const { alert_list, meta } = response.data;

    const alertList = alert_list.map(
      (alert: ApiAlertsList): AlertsListRow => ({
        monitorId: alert.monitor_id,
        monitorName: alert.monitor_name,
        monitorMethod: alert.monitor_method,
        modelId: alert.model_id,
        severity: alert.severity,
        status: alert.status,
        time: alert.time
      })
    );

    const AlertsListMeta: AlertsListMeta = {
      page: meta?.page || 1,
      limit: meta?.limit || 10,
      total: meta?.total || 4,
      sort: meta?.sort || 'name_asc',
      query: meta?.query || ''
    };

    return {
      ...response,
      alertList,
      meta: AlertsListMeta
    };
  }
};
