import axios, { AxiosInstance } from 'axios';
import { loadState } from '../redux/localStorage';

// ----------------------------------------------------------------------
const axiosInstance = (): AxiosInstance => {
  const axiosConf = axios.create({
    baseURL: process.env.REACT_APP_API_URL
  });
  axiosConf.interceptors.request.use(
    (conf) => {
      const state = loadState();
      const org_id = state ? state?.org_id : '';
      let token = null;
      if (state?.user?.token) {
        token = state.user.token;
        conf.headers.Authorization = `Bearer ${token}`;
        conf.headers.Org = org_id;
      }
      // else {
      //   history.push(R_AUTHORIZE());
      // }
      return conf;
    },
    (error: any) => Promise.reject(error)
  );
  axiosConf.interceptors.response.use(
    (response) => response,
    (error) => {
      return Promise.reject(error);
    }
  );
  return axiosConf;
};

const instance = axiosInstance();
export default instance;
