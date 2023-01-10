import Page from '../../../../components/Page';
import { experimentalStyled as styled } from '@material-ui/core/styles';
import { makeStyles } from '@material-ui/styles';
import { useParams } from 'react-router-dom';

import { Grid, Box, Select, TextField, MenuItem } from '@material-ui/core';
import { useState, useEffect } from 'react';
import { useSelector } from '../../../../redux/store';
import { DateRangeFilterState } from '../../../../redux/slices/dateRangeFilter';
import { formatDateTime } from '../../../../utils/date';
import { colors } from '../../../../theme/colors';
import { DataProfileOverviewCards } from './DataProfileCards';
import { DataProfileVersionCard } from './DataProfileCards';
import { DataDatasetSelectCard } from './DataProfileCards';
import { DataProfileStats } from './DataProfileStatics';
import { useGetDatasets } from '../../../../api/datasets/GetDatasets';
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
  flexBox: {
    display: 'flex',
    gap: '10%'
  },
  conatinerHeading: {
    fontSize: '.9rem',
    color: colors.text,
    fontWeight: 500
  },
  select: {
    marginTop: '.75rem',
    marginBottom: '.75rem',
    backgroundColor: `${colors.white} !important`,
    fontFamily: 'Poppins',
    maxWidth: '20rem',
    minWidth: '20rem',
    transform: 'scale(1,.8)',
    '& .MuiInputBase-input': {
      transform: 'scale(1,1.2)'
    },
    [`& fieldset`]: {
      borderRadius: 2,
      borderColor: `${colors.textLight} !important`
    },
    [`&.Mui-focused fieldset`]: {
      borderRadius: 4,
      borderColor: `${colors.text} !important`
    }
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
  const [dataset, setDataset] = useState<string>('');
  const handleChange = (id: string) => setVersion(id);
  const handleData = (dataset: string) => setDataset(dataset);
  const [version, setVersion] = useState<string>('');
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
          <Box className={classes.flexBox}>
            <Box className={classes.box}>
              <DataProfileVersionCard model_id={modelId} on_change={handleChange} />
            </Box>
            {
              version.length ?
              (<Box className={classes.box}>
                <DataDatasetSelectCard version_id={version} on_change={handleData} dateTimeString={dateTimeString} />
              </Box>): null
              
            }
            
          </Box>
            <>
              {dataset.length ? <DataProfileStats datasetId={dataset} model_id={modelId} model_version_id={version} /> : null}
            </>
        </RootStyle>
      </Page>
    </>
  );
};
export default ModelDataProfile;
