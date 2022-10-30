import React from 'react';
import { Box } from '@material-ui/core';
import Page from '../../components/Page';
import HeaderBreadcrumbs from '../../components/HeaderBreadcrumbs';
import { makeStyles } from '@material-ui/core/styles';
import { useDispatch } from '../../redux/store';
import AlertListTable from './AlertListTable';

const useStyles = makeStyles(() => ({
  model_list_container: {
    padding: '0 4rem 0 2.1rem'
  }
}));

const AlertList: React.FC = () => {
  const classes = useStyles();
  const dispatch = useDispatch();
  return (
    <Page title="Alerts List | Waterdip">
      <Box>
        <HeaderBreadcrumbs heading="Alerts" links={[]} action={''} />
      </Box>
      <div className={classes.model_list_container}>
        <AlertListTable value="Not Model" />
      </div>
    </Page>
  );
};

export default AlertList;
