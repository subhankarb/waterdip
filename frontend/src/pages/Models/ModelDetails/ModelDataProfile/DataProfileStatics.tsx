import { makeStyles } from '@material-ui/styles';
import { Box } from '@material-ui/core';
import { Heading } from '../../../../components/Heading';
import CollapsibleTable from '../../../../components/Tables/collapsible-table-2';
import { useGetDatasetsInfo } from '../../../../api/datasets/GetDatasetInfo';
import { useSelector } from '../../../../redux/store';
import { DateRangeFilterState } from '../../../../redux/slices/dateRangeFilter';

const useStyles = makeStyles({});

export const DataProfileStats = ({ datasetId }: any) => {
  const classes = useStyles();
  const now = new Date();
  const { fromDate, toDate } = useSelector(
    (state: { dateRangeFilter: DateRangeFilterState }) => state.dateRangeFilter
  );
  const { data } = useGetDatasetsInfo({
    dataset_id: datasetId,
    start_date: fromDate,
    end_date: toDate
  });
  const datasetInfo = data && data;
  return (
    <Box sx={{ marginTop: '30px' }}>
      <Heading heading="Data Statistics" subtitle="Data Statistics" />
      {datasetInfo && (
        <CollapsibleTable
          dataValue={datasetInfo.categorical_column_stats}
          data_type="CATEGORICAL"
        />
      )}
      {datasetInfo && (
        <CollapsibleTable dataValue={datasetInfo.numeric_column_stats} data_type="NUMERIC" />
      )}
    </Box>
  );
};
