import Page from '../../../../components/Page';
import LoadingScreen from '../../../../components/LoadingScreen';
import CollapsibleTable from '../../../../components/Tables/collapsible-table-1';
import { MenuItem, Grid, Box, TextField } from '@material-ui/core';
import { experimentalStyled as styled } from '@material-ui/core/styles';
import { Heading } from '../../../../components/Heading';
import { makeStyles } from '@material-ui/core/styles';
import { colors } from '../../../../theme/colors';

import ChartBar from '../../../../components/charts/ChartBar';
const data = {
  feat_breakdown: [
    {
      buckets: ['f_0', 'f_1', 'f_2', 'f_3', 'f_4', 'f_5', 'f_6', 'f_7', 'f_8', 'f_9'],
      hist_values: [22, 27, 23, 30, 13, 27, 20, 15, 12, 10],
      impact: 0.1725,
      name: 'Fico_Score'
    },
    {
      buckets: ['f_0', 'f_1', 'f_2', 'f_3', 'f_4', 'f_5', 'f_6', 'f_7', 'f_8', 'f_9'],
      hist_values: [22, 27, 23, 30, 13, 27, 20, 15, 12, 10],
      impact: 0.1725,
      name: 'Fico_Score'
    },
    {
      buckets: ['f_0', 'f_1', 'f_2', 'f_3', 'f_4', 'f_5', 'f_6', 'f_7', 'f_8', 'f_9'],
      hist_values: [22, 27, 23, 30, 13, 27, 20, 15, 12, 10],
      impact: 0.1725,
      name: 'Fico_Score'
    }
  ],
  data: [84, 77, 53, 76, 54, 71, 73, 71, 68, 70],
  time_buckets: [
    '2022-05-19T10:41:58.617981',
    '2022-05-18T10:41:58.617988',
    '2022-05-17T10:41:58.617989',
    '2022-05-16T10:41:58.617990',
    '2022-05-15T10:41:58.617991',
    '2022-05-14T10:41:58.617992',
    '2022-05-13T10:41:58.617993',
    '2022-05-12T10:41:58.617994',
    '2022-05-11T10:41:58.617995',
    '2022-05-10T10:41:58.617996'
  ]
};
const RootStyle = styled('div')({
  overflowY: 'hidden',
  padding: '1.6rem 2.4rem',
  background: colors.white
});
const useStyles = makeStyles(() => ({
  graph: {
    maxWidth: '1000px'
  },
  table: {
    marginTop: '1.6rem',
    maxWidth: '1000px'
  }
}));

const ModelDrift = () => {
  const classes = useStyles();

  return (
    <Page title="Model Drift | Waterdip">
      <RootStyle>
        <Box className={classes.graph}>
          <Heading heading="Prediction drift over time" subtitle="Prediction drift over time" />
          <ChartBar
            data={data.data}
            categories={data.time_buckets.map((bucket: string) => bucket.split('T')[0])}
            name={'PSI'}
            options={{ width: '100%', height: 240, columnWidth: '50%', enableDataLabels: false }}
          />
        </Box>
        <Box className={classes.table}>
          <Heading heading="Feature Breakdown" subtitle="Feature breakdown" />
          <CollapsibleTable tablehead_name="Feature Class" dataValue={data.feat_breakdown} />
        </Box>
      </RootStyle>
    </Page>
  );
};

export default ModelDrift;
