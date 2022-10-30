export interface AlertsListRow {
  monitorId: string;
  monitorName: string;
  monitorMethod: string;
  modelId: string;
  severity: string;
  status: string;
  time: string;
}

export interface AlertsListMeta {
  page: number;
  limit: number;
  total: number;
  sort: string;
  query: string;
}
