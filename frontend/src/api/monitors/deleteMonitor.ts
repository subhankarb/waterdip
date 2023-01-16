import { useMutation } from 'react-query';
import { DELETE_MONITOR_API } from '../apis';
import axios from '../../utils/axios';
import { useState } from 'react';

type MyError = Error;

interface DeleteMonitorHook {
  isDeleting: boolean;
  error: MyError | null;
  MonitorDelete: (monitorId: string) => Promise<void>;
}
export const useMonitorDelete = (): DeleteMonitorHook => {
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState<MyError | null>(null);

  const MonitorDelete = async (monitorID: string) => {
    setIsDeleting(true);
    try {
      await axios.delete(DELETE_MONITOR_API, { data : ""+ monitorID });
    } catch (err) {
      setError(err as MyError);
    } finally {
      setIsDeleting(false);
    }
    
  }; 
  return { isDeleting, error, MonitorDelete }
};
       