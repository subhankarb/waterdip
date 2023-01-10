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
      evaluation_metric: '',
      dimensions: {
        features: [],
        predictions: []
      },
      threshold: {
        threshold: '',
        value: number
      },
      actions: {
        monitor_name: '',
        severity: ''
      },
      logicEvaluations: {}
    },
    monitor_identification: {
      model_id: '',
      model_version_id: ''
    },
    
    monitor_domain: '',
    monitor_schedule: '',
    monitor_type: ''
  }
};
