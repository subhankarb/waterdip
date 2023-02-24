import { makeStyles } from '@material-ui/styles';
import { Box } from '@material-ui/core';
import { Heading } from '../../../../components/Heading';
import CollapsibleTable from '../../../../components/Tables/collapsible-table-2';
import { useGetMetricsDataset } from 'api/datasets/GetMetricsDataset';
import { useSelector } from '../../../../redux/store';
import { DateRangeFilterState } from '../../../../redux/slices/dateRangeFilter';

const useStyles = makeStyles({});

export const DataProfileStats = ({ datasetId, model_id, model_version_id }: any) => {
  const classes = useStyles();
  const now = new Date();
  const { fromDate, toDate } = useSelector(
    (state: { dateRangeFilter: DateRangeFilterState }) => state.dateRangeFilter
  );
  const { data } = useGetMetricsDataset({
      model_id: model_id,
      model_version_id: model_version_id,
      dataset_id: datasetId,
      start_date: fromDate,
      end_date: toDate 
  })
  const datasetInfo = data && data.data;
  return (
    <Box sx={{ marginTop: '30px' }}>
      <Heading heading="Data Statistics" subtitle="Data Statistics for each columns" />
      {datasetInfo && datasetInfo.categorical_column_stats.length != 0 ?(
        <>
          <Heading heading="Categorical Table" />
          <CollapsibleTable
            dataValue={datasetInfo.categorical_column_stats}
            data_type="CATEGORICAL"
         />
        </>     
      ): null}
      {datasetInfo && datasetInfo.numeric_column_stats.length != 0  ?(
        <>
          <Heading heading="Numeric Table" />
          <CollapsibleTable dataValue={datasetInfo.numeric_column_stats} data_type="NUMERIC" />
        </>
      ): null}
    </Box>
  );
};
