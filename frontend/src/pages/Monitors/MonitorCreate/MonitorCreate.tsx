import React from 'react';
import { Container, Link, Box } from '@material-ui/core';
import { Link as RouterLink } from 'react-router-dom';
import Page from '../../../components/Page';
import HeaderBreadcrumbs from '../../../components/HeaderBreadcrumbs';
import { PATH_DASHBOARD } from '../../../routes/paths';
import { makeStyles } from '@material-ui/core/styles';
import VerticalLinearStepper from './stepper/VerticalLinearStepper';
import { useLocation } from 'react-router-dom';
import { colors } from '../../../theme/colors';

const useStyles = makeStyles(() => ({
  createMonitorText: {
    fontWeight: 500,
    fontSize: '1rem',
    color: '#2A2A2A',
    padding: '1.4rem 0 .3rem 0'
  },
  stepperContainer: { padding: '0 2.4rem' },
  monitorTextType: {
    color: colors.textPrimary,
    fontSize: '1.05rem',
    fontWeight: 500
  }
}));

const MonitorCreate = () => {
  const classes = useStyles();
  const location = useLocation();
  const data: any = location.state;
  return (
    <Page title="Create a new Monitor | Waterdip">
      <Box>
        <HeaderBreadcrumbs
          links={[{ name: 'Monitors', href: `${PATH_DASHBOARD.general.monitors}` }]}
          heading="Create monitor"
        />
      </Box>

      <Box className={classes.stepperContainer}>
        <Box className={classes.createMonitorText}>
          Create a monitor of type&nbsp;
          <span className={classes.monitorTextType}>{data.type}</span> and model{' '}
          <span className={classes.monitorTextType}></span>
        </Box>
        <VerticalLinearStepper monitorType={data.type} model_id={data.model} model_version_id={data.version}/>
      </Box>
    </Page>
  );
};
export default MonitorCreate;
