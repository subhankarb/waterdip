import { DELETE_MODEL_API } from '../apis';
import axios from '../../utils/axios';
import { useState } from 'react';
type MyError = Error;
interface DeleteModelHook {
  isDeleting: boolean;
  error: MyError | null;
  ModelDelete: (modelId: string) => Promise<void>;
}
export const useModelDelete = (): DeleteModelHook => {
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState<MyError | null>(null);
  const ModelDelete = async (modelID: string) => {
    setIsDeleting(true);
    try {
      await axios.post(DELETE_MODEL_API,  modelID);
    } catch (err) {
      setError(err as MyError);
    } finally {
      setIsDeleting(false);
    }
    
  }; 
  return { isDeleting, error, ModelDelete }
};