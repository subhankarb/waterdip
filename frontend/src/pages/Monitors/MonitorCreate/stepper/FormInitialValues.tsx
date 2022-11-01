import FormMonitor from './FormMonitor';

const {
  formField: {
    monitor_method,
    monitor_condition,
    monitor_identification,
    monitor_name,
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
    evaluation_metric: {},
    dimensions: {
      features: [],
      predictions: []
    },
    threshold: {
      gt: 0.2,
      lt: 0.8
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
};
