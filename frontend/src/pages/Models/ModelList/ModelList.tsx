import React from 'react';
import { Box } from '@material-ui/core';
import Page from '../../../components/Page';
import HeaderBreadcrumbs from '../../../components/HeaderBreadcrumbs';
import ModelListTable from './ModelListTable';
import { makeStyles } from '@material-ui/core/styles';
import './shadow.css';
const useStyles = makeStyles(() => ({
  model_list_container: {
    padding: '0 4rem 0 2.1rem'
  }
}));

const ModelList: React.FC = () => {
  const classes = useStyles();
  return (
    <Page title="Model List | Waterdip">
      <Box>
        <HeaderBreadcrumbs heading="Models" links={[]} action={''} />
      </Box>
      <div className={classes.model_list_container}>
        <ModelListTable />
      </div>
    </Page>
  );
};

export default ModelList;
