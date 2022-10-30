import { number } from 'yup/lib/locale';

export default {
  formId: 'FormMonitor',
  formField: {
    monitor_method: {
      method: '',
      baseline: {
        skip_period: '',
        time_period: '',
        aggregation_period: ''
      },
      dataset_id: ''
    },
    monitor_condition: {
      evaluation_window: '',
      evaluation_metric: {},
      dimensions: {
        features: [],
        predictions: []
      },
      threshold: {
        gt: number,
        lt: number
      },
      actions: [{}],
      logicEvaluations: {}
    },
    monitor_identification: {
      model: {},
      environment: ''
    },
    monitor_name: '',
    monitor_domain: '',
    monitor_schedule: '',
    monitor_type: ''
  }
};
