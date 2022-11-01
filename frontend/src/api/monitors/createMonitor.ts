import { useMutation } from 'react-query';
import { CREATE_MONITOR_API } from '../apis';
import axios from '../../utils/axios';
export const MonitorCreate = () => {
  const createMonitor = async (newMonitor: any) => {
    const response = await axios.post(CREATE_MONITOR_API, newMonitor);

    const { monitor_id } = response.data;

    return { ...response, monitor_id };
  };

  const mutation = useMutation(createMonitor);

  return mutation;
};
