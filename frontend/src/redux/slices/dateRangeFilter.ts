import { createSlice } from '@reduxjs/toolkit';

export type DateRangeFilterState = {
  fromDate: Date | null;
  toDate: Date | null;
};

const initialState: DateRangeFilterState = {
  fromDate: null,
  toDate: null
};

const slice = createSlice({
  name: 'dateRangeFilter',
  initialState,
  reducers: {
    setDateRange(state, action) {
      state.fromDate = action.payload.fromDate;
      state.toDate = action.payload.toDate;
    }
  }
});

export default slice.reducer;

export const { setDateRange } = slice.actions;
