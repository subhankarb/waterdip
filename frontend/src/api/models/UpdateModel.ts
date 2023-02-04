import { UPDATE_MODEL_API } from '../apis';
import axios from '../../utils/axios';
import { useState } from 'react';
type MyError = Error;


interface UpdateModelHook {
  isUpdating : boolean;
  error: MyError | null;
  ModelUpdate: (update: UpdateModelParams) => Promise<void>;
}

interface UpdateModelParams {
    model_id: string,
    property_name: string,
    baseline?: {
      dataset_env?: string,
      time_window?: {
        time_period: string,
      }
    },
    positive_class?: any
}

export const useModelUpdate = (): UpdateModelHook => {
  const [isUpdating, setIsUpdating] = useState(false);
  const [error, setError] = useState<MyError | null>(null);
  const ModelUpdate = async (updated :UpdateModelParams) => {
    setIsUpdating(true);
    try {
      await axios.post(UPDATE_MODEL_API, updated);
    } catch (err) {
      setError(err as MyError);
    } finally {
        setIsUpdating(false);
    }
    
  }; 
  return { isUpdating, error, ModelUpdate }
};