import { combineReducers } from 'redux';
// import { persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
// slices
import userReducer from './slices/user';
import dateRangeFilterReducer from './slices/dateRangeFilter';
import modelMonitorStateReducer from './slices/ModelMonitorState';

// ----------------------------------------------------------------------

const rootPersistConfig = {
  key: 'root',
  storage,
  keyPrefix: 'redux-',
  whitelist: []
};

// const productPersistConfig = {
//   key: 'product',
//   storage,
//   keyPrefix: 'redux-',
//   whitelist: ['sortBy', 'checkout']
// };

const rootReducer = combineReducers({
  user: userReducer,
  dateRangeFilter: dateRangeFilterReducer,
  modelMonitorState: modelMonitorStateReducer
});

export { rootPersistConfig, rootReducer };
