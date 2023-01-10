import FormMonitor from './FormMonitor';

const {
  formField: {
    monitor_method,
    monitor_condition,
    monitor_identification,
    monitor_domain,
    monitor_schedule,
    monitor_type
  }
} = FormMonitor;

export default {
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
      value : 0
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
};
