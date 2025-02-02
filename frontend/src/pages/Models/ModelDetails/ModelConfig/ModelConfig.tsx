import Page from '../../../../components/Page';
import LoadingScreen from '../../../../components/LoadingScreen';
import { Box } from '@material-ui/core';
import { experimentalStyled as styled } from '@material-ui/core/styles';
import { Heading } from '../../../../components/Heading';
import { makeStyles } from '@material-ui/core/styles';
import { ConfigBaseLine, ConfigEvaluation, ConfigAdvanced } from './ConfigCards';
import { useLocation } from 'react-router-dom';
import { colors } from '../../../../theme/colors';

const RootStyle = styled('div')({
  overflowY: 'hidden',
  padding: '1.6rem 2.4rem',
  background: colors.white
});
const useStyles = makeStyles(() => ({}));

const ModelConfiguration = (d: any) => {
  const classes = useStyles();
  const location = useLocation();
  const data = location.state === null ? false : true;

  return (
    <Page title="Model Configruration | Waterdip">
      <RootStyle>
        <Box>
          <ConfigBaseLine path={data} data={d}/>
          <ConfigEvaluation data={d}/>
          <ConfigAdvanced />
        </Box>
      </RootStyle>
    </Page>
  );
};

export default ModelConfiguration;
