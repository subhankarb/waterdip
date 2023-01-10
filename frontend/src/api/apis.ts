import {BASE_URL} from "../config";

console.log("==================")
console.log(BASE_URL)
const makeUrl = (path: string) => `${BASE_URL}/v1/${path}`;

export const GET_MODELS_API = makeUrl('list.models');
export const GET_MODEL_Info_API = makeUrl('model.info');
export const GET_MODEL_Overview_API = makeUrl('model.overview');
export const GET_MODEL_PERFORMANCE_API = makeUrl('model.performance');
export const CREATE_MODEL_API = makeUrl('model.register');
export const GET_MODEL_VERSION_INFO_API = makeUrl('model.version.info')

export const GET_MODEL_DATA_PERF_PCA_API = makeUrl('data.perf.pca');
export const GET_MODEL_DATA_PERF_CLUSTER_API = makeUrl('data.perf.cluster');
export const GET_MODEL_DATA_PERF_ANOMALOUS_API = makeUrl('data.perf.anomalous');

export const GET_MODEL_DATA_EXPORT_LIST = makeUrl('model.export.list');
export const CREATE_MODEL_ANOMALOUS_EXPORT = makeUrl('model.export.anomalous');

export const GET_DATASETS_API = makeUrl('list.datasets');
export const GET_DATASET_INFO_API = makeUrl(`dataset.info`);
export const GET_METRICS_DATASET = makeUrl(`metrics.dataset`);

export const CREATE_MONITOR_API = makeUrl('monitor.create');

export const GET_ALERTS_API = makeUrl('list.incidents');
