import { useMutation } from 'react-query';
import { CREATE_MODEL_API } from '../apis';

import axios from '../../utils/axios';

type NewModel = {
  model_name: string;
};

type ModelCreateResponse = {
  modelName: string;
};

export const UseModelCreate = async (newModel: NewModel) => {
  const response = await axios.post(CREATE_MODEL_API, newModel);

  const { model_name } = response.data;

  const modelCreateResponse: ModelCreateResponse = {
    modelName: model_name || ''
  };

  return { ...response, modelCreateResponse };
  // const createModel = async (newModel: NewModel) => {
  //   console.log("hello")
  //   const response = await axios.post(CREATE_MODEL_API, newModel);

  //   const { model_name } = response.data;

  //   const modelCreateResponse: ModelCreateResponse = {
  //     modelName: model_name || ''
  //   };

  //   return { ...response, modelCreateResponse };
  // };

  // const mutation = useMutation(createModel);

  // return mutation;
};
