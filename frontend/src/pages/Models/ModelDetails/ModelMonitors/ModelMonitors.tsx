import React, { useState } from 'react';
import Page from '../../../../components/Page';
import LoadingScreen from '../../../../components/LoadingScreen';
import { Box } from '@material-ui/core';
import { experimentalStyled as styled } from '@material-ui/core/styles';
import { makeStyles } from '@material-ui/core/styles';
import { colors } from '../../../../theme/colors';
import MonitorListTable from '../../../Monitors/MonitorList/MonitorListTable';
import { useParams } from 'react-router-dom';
import { setModelMonitorData } from '../../../../redux/slices/ModelMonitorState';
import { useDispatch } from '../../../../redux/store';

const RootStyle = styled('div')({
  overflowY: 'hidden',
  padding: '.7rem 2.4rem',
  background: colors.white
});
const useStyles = makeStyles(() => ({}));

const ModelMonitors = () => {
  const classes = useStyles();
  const { modelId } = useParams();

  const dispatch = useDispatch();
  dispatch(setModelMonitorData({ modelID: modelId, pathLocation: 'model' }));

  return (
    <Page title="Model Monitor | Waterdip">
      <RootStyle>
        <MonitorListTable />
      </RootStyle>
    </Page>
  );
};

export default ModelMonitors;
