import { useMutation } from 'react-query';
import { CREATE_MONITOR_API } from '../apis';

import axios from '../../utils/axios';

type NewMonitor = {
  "monitor_name": string,
  "monitor_type": string,
  "monitor_identification": {
      "model_id": string,
      "model_version_id": string,
  },
  "monitor_condition": {
      "evaluation_metric": string,
      "dimensions"?: any,
      "threshold"?: any,
      "evaluation_window": string,
      "baseline"?: any
  },
};

type ModelCreateResponse = {
  modelName: string;
};

export const useMonitorCreate = () => {
  const createMonitor = async (newMonitor: any) => {
    const response = await axios.post(CREATE_MONITOR_API, newMonitor);
    return response
  };

  const mutation = useMutation(createMonitor);

  return mutation;
};