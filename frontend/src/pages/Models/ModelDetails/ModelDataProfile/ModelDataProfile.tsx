import Page from '../../../../components/Page';
import { experimentalStyled as styled } from '@material-ui/core/styles';
import { makeStyles } from '@material-ui/styles';
import { useParams } from 'react-router-dom';

import { Grid, Box, TextField, MenuItem } from '@material-ui/core';
import { useState, useEffect } from 'react';
import { useSelector } from '../../../../redux/store';
import { DateRangeFilterState } from '../../../../redux/slices/dateRangeFilter';
import { formatDateTime } from '../../../../utils/date';
import { colors } from '../../../../theme/colors';
import { DataProfileOverviewCards } from './DataProfileCards';
import { DataProfileStats } from './DataProfileStatics';
import { useGetDatasets } from '../../../../api/datasets/GetDatasets';
import { useGetDatasetsInfo } from '../../../../api/datasets/GetDatasetInfo';
import { useLocation } from 'react-router-dom';

const RootStyle = styled('div')({
  overflowY: 'hidden',
  padding: '1.6rem 1.6rem',
  background: colors.white
});
const useStyles = makeStyles({
  box: {
    display: 'flex'
  },
  card: {
    width: '100%',
    maxWidth: '360px',
    color: colors.text,
    background: colors.boxBackground,
    borderRadius: '4px',
    padding: '1rem',
    height: '160px'
  },
  cardHeading: {
    fontSize: '.85rem',
    fontWeight: 600,
    letterSpacing: '.25px',
    marginBottom: '.5rem'
  }
});

const ModelDataProfile = () => {
  const classes = useStyles();
  const location = useLocation();
  const { modelId } = useParams();

  const { data } = useGetDatasets({
    sort: 'name_asc',
    limit: 10,
    query: '',
    page: 1,
    model_id: modelId
  });
  const datasetList = data?.dataset_list;
  const [dataset, setDataset] = useState<string>('');
  const now = new Date();
  const { fromDate, toDate } = useSelector(
    (state: { dateRangeFilter: DateRangeFilterState }) => state.dateRangeFilter
  );
  const dateTimeString = `${formatDateTime(fromDate ? fromDate : now)} to ${formatDateTime(
    toDate ? toDate : now
  )} `;

  return (
    <>
      <Page title="Model Dataset | Waterdip">
        <RootStyle>
          {datasetList && (
            <>
              <Box className={classes.box}>
                {dataset && <DataProfileOverviewCards datasetId={dataset} />}
                &nbsp; &nbsp; &nbsp; &nbsp;
                <Box className={classes.card}>
                  <TextField
                    select
                    fullWidth
                    label="Choose the dataset"
                    value={dataset}
                    onChange={(e) => setDataset(e.target.value)}
                    sx={{ mb: 3 }}
                    placeholder="Select Data Profile"
                  >
                    {datasetList?.map((item: any) => {
                      return (
                        <MenuItem key={item.dataset_id} value={item.dataset_id}>
                          {item.dataset_name}
                        </MenuItem>
                      );
                    })}
                  </TextField>
                  <Box className={classes.cardHeading}>Date from {dateTimeString}</Box>
                </Box>
              </Box>
              {dataset && <DataProfileStats datasetId={dataset} />}
            </>
          )}
        </RootStyle>
      </Page>
    </>
  );
};
export default ModelDataProfile;
