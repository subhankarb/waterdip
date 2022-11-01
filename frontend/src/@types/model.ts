export type ModelTaskdata_type = 'NUMERIC' | 'CATEGORICAL' | 'BOOLEAN';
export type PredictionTaskType = 'binary' | 'multiclass';
export type data_type = 'TEXT' | 'TABULAR';
export type ModelFeatures = Record<string, ModelTaskdata_type>;
// export type ModelRawInputs = Record<string, ModelTaskdata_type>;
export type ModelPredictions = Record<string, ModelTaskdata_type>;
export type ModelPredictionTasks = Record<string, PredictionTaskType>;

export type ModelTasksStat = {
  taskName: string;
  avgPrecision: any;
  avgRecall: any;
  avgAccuracy: any;
};

export interface Model {
  id: string;
  version_id: string;
  name: string;
  dataType: data_type;
  description: string;
  // features: ModelFeatures;
  // rawInputs: ModelRawInputs;
  predictions: ModelPredictions;
  createdAt: string;
  totalPredictions: string;
  alertPerf: string;
  alertDataBehave: string;
  alertDataIntegrity: string;
  lastPrediction: string;
}

// export type ModelListRow = Omit<Model, 'features' | 'rawInputs'>;
export type ModelListRow = Omit<Model, 'features'>;

export interface ExportListRow {
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

export interface ModelListMeta {
  page: number;
  limit: number;
  total: number;
  sort: string;
  query: string;
}

export type ModelPredictionTaskReq = Record<
  string,
  {
    task_type: 'BINARY' | 'MULTICLASS';
    predictions: Record<string, ModelTaskdata_type>;
  }
>;

export interface ModelPerformaceRequests {
  buckets: {
    count: number;
    key: string;
  }[];
}

export interface ModelPerformanceConfustionMatrix {
  total: number;
  confusionClasses: {
    className: string;
    confusions: {
      confusionType: string;
      count: number;
    }[];
  }[];
}

export interface ModelPerformancePrecision {
  avgPrecision: number;
  precisionByClassList: {
    className: string;
    precisionByClass: number;
  }[];
}

export interface ModelPerformanceRecall {
  avgRecall: number;
  recallByClassList: {
    className: string;
    recallByClass: number;
  }[];
}

export interface ModelPerformance {
  requests: ModelPerformaceRequests;
  confusionMatrix: ModelPerformanceConfustionMatrix;
  precision: ModelPerformancePrecision;
  recall: ModelPerformanceRecall;
}

// model data

export interface ModelDataPerformancePcaComponent {
  name: string;
  binKeys: string[];
  serving: number[];
  training: number[];
}

export interface ModelDataPerformancePca {
  components: ModelDataPerformancePcaComponent[];
}

export interface ModelPerformanceCluster {
  clusterId: string;
  servingCount: number;
  trainingBoundary: {
    x: number;
    y: number;
  }[];
  servingData: {
    x: number;
    y: number;
  }[];
}

export interface ModelDataPerformanceCluster {
  clusters: Record<string, ModelPerformanceCluster>;
}

export interface ModelPerformanceAnomalousCluster {
  x: number;
  y: number;
}

export interface AnomalousMeta {
  query: string;
  page: string;
  limit: string;
  total: string;
  sort: string;
}

export interface ModelDataPerformanceAnomalous {
  clusters: Record<string, ModelPerformanceAnomalousCluster[]>;
  anomalous: {
    x: number;
    y: number;
  }[];
  total: number;
  data: string[];
  data_dict: Record<string, Record<string, string>[]>;
  row_names?: string[];
  data_list?: Record<string, string | number>[];
  meta?: AnomalousMeta;
}

export interface ModelProfileBaseFeature {
  name: string;
  distinctCount: number;
  distinctPercentage: number;
  missingCount: number;
  missingPercentage: number;
}

export interface ModelProfileTextFeature extends ModelProfileBaseFeature {
  wordCounts: Record<string, number>;
  meanLength: number;
  minLength: number;
  maxLength: number;
  histogram: Record<string, number>;
}

export interface ModelProfileNumericalFeature extends ModelProfileBaseFeature {
  zeroesCount: number;
  zeroesPercentage: number;
  minimum: number;
  maximum: number;
  mean: number;
  std: number;
  variance: number;
  '5%': number;
  '25%': number;
  '50%': number;
  '75%': number;
  '95%': number;
  kurtosis: number;
  skewness: number;
  histogram: {
    counts: number[];
    binEdges: number[];
  };
}

export interface ModelProfileCategoricalFeature extends ModelProfileBaseFeature {
  histogram: Record<string, number>;
  histogramValueType: string;
}

export interface ModelProfile {
  totalFeatures: number;
  totalDataRows: number;
  totalDuplicates: number;
  totalMissingValues: number;
  percentageDuplicates: number;
  percentageMissingValues: number;
  text: {
    total: number;
    data: ModelProfileTextFeature[];
  };
  numerical: {
    total: number;
    data: ModelProfileNumericalFeature[];
  };
  categorical: {
    total: number;
    data: ModelProfileCategoricalFeature[];
  };
}
