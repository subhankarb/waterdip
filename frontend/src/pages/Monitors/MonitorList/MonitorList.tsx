import React from 'react';
import { Box } from '@material-ui/core';
import Page from '../../../components/Page';
import HeaderBreadcrumbs from '../../../components/HeaderBreadcrumbs';
import { makeStyles } from '@material-ui/core/styles';
import MonitorListTable from './MonitorListTable';
import { setModelMonitorData } from '../../../redux/slices/ModelMonitorState';
import { useDispatch } from '../../../redux/store';

const useStyles = makeStyles(() => ({
  model_list_container: {
    padding: '0 4rem 0 2.1rem'
  }
}));

const MonitorList: React.FC = () => {
  const classes = useStyles();
  const dispatch = useDispatch();
  dispatch(setModelMonitorData({ modelID: null, pathLocation: 'monitor' }));
  return (
    <Page title="Monitor List | Waterdip">
      <Box>
        <HeaderBreadcrumbs heading="Monitors" links={[]} action={''} />
      </Box>
      <div className={classes.model_list_container}>
        <MonitorListTable />
      </div>
    </Page>
  );
};

export default MonitorList;
