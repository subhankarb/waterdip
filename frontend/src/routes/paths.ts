function path(root: string, sublink: string) {
  return `${root}${sublink}`;
}

const ROOTS_AUTH = '/auth';
const ROOTS_DASHBOARD = '/app';
const ROOTS_MODELS = (modelId: string) => path(ROOTS_DASHBOARD, `/models/${modelId}`);

export const PATH_AUTH = {
  root: ROOTS_AUTH,
  login: path(ROOTS_AUTH, '/login')
};

export const PATH_PAGE = {
  page404: '/404',
  page500: '/500',
  components: '/components'
};

export const PATH_DASHBOARD = {
  root: ROOTS_DASHBOARD,
  general: {
    models: path(ROOTS_DASHBOARD, '/models'),
    modelDetails: (modelId: string, versionId: string) => path(ROOTS_MODELS(modelId), `/`),
    monitors: path(ROOTS_DASHBOARD, '/monitors'),
    monitorCreate: path(ROOTS_DASHBOARD, '/monitors/create'),
    alerts: path(ROOTS_DASHBOARD, '/alerts')
    // members: path(ROOTS_DASHBOARD, '/members')
  }
};
