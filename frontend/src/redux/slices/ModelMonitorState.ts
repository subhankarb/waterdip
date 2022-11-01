import { createSlice } from '@reduxjs/toolkit';

export type ModelMonitorState = {
  modelID: string | null;
  modelName: string | null;
  pathLocation: 'model' | 'monitor' | 'dataset' | null;
};

const initialState: ModelMonitorState = {
  modelID: null,
  modelName: null,
  pathLocation: null
};

const modelMonitorSlice = createSlice({
  name: 'modelMonitorState',
  initialState,
  reducers: {
    setModelMonitorData(state, action) {
      state.modelID = action.payload.modelID;
      state.modelName = action.payload.modelName;
      state.pathLocation = action.payload.pathLocation;
    }
  }
});

export default modelMonitorSlice.reducer;

export const { setModelMonitorData } = modelMonitorSlice.actions;
