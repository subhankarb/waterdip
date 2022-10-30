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
      if (error.response) {
        // eslint-disable-next-line prefer-promise-reject-errors
        return Promise.reject(error?.response?.data?.errors);
      }
      if (error.request) {
        // The request was made but no response was received
        // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
        // http.ClientRequest in node.js
        // eslint-disable-next-line prefer-promise-reject-errors
        return Promise.reject([{ msg: 'Something went wrong!! Please reload.' }]);
      }
      // eslint-disable-next-line prefer-promise-reject-errors
      return Promise.reject([{ msg: error.message }]);
    }
  );
  return axiosConf;
};

const instance = axiosInstance();
export default instance;
