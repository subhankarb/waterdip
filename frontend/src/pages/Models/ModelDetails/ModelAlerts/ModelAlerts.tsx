import React, { useState } from 'react';
import Page from '../../../../components/Page';
import LoadingScreen from '../../../../components/LoadingScreen';
import { Box } from '@material-ui/core';
import { experimentalStyled as styled } from '@material-ui/core/styles';
import { makeStyles } from '@material-ui/core/styles';
import { colors } from '../../../../theme/colors';
import { useParams } from 'react-router-dom';
import { useDispatch } from '../../../../redux/store';
import AlertListTable from 'pages/Alerts/AlertListTable';

const RootStyle = styled('div')({
  overflowY: 'hidden',
  padding: '.5rem 2.4rem',
  background: colors.white
});
const useStyles = makeStyles(() => ({}));

const ModelAlerts = () => {
  const classes = useStyles();
  const { modelId } = useParams();

  const dispatch = useDispatch();

  return (
    <Page title="Model Alert | Waterdip">
      <RootStyle>
        <AlertListTable value="Model" />
      </RootStyle>
    </Page>
  );
};

export default ModelAlerts;
