import { makeStyles } from '@material-ui/styles';
import { Box } from '@material-ui/core';
import { colors } from '../../../../theme/colors';
import { useGetDatasetsInfo } from '../../../../api/datasets/GetDatasetInfo';
import { useState, useEffect } from 'react';
import { Data } from 'emoji-mart';
import { string } from 'yup/lib/locale';
import { useSelector } from '../../../../redux/store';
import { DateRangeFilterState } from '../../../../redux/slices/dateRangeFilter';
const useStyles = makeStyles({
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
  },
  cardContent: {
    display: 'grid',
    gridTemplateColumns: 'repeat(2,1fr)',
    gridTemplateRows: 'repeat(3,1fr)',
    gridColumnGap: '1.5rem'
  },
  cardEntry: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '.6rem  0'
  },
  entryTitle: { fontSize: '.62rem', fontWeight: 400, color: colors.text },
  entryContent: { fontSize: '.62rem', fontWeight: 400, color: colors.textLight }
});

const CardEntry = ({ title, value }: any) => {
  const classes = useStyles();
  return (
    <Box className={classes.cardEntry}>
      <Box className={classes.entryTitle}>{title}</Box>
      <Box className={classes.entryContent}>{value}</Box>
    </Box>
  );
};

export const DataProfileOverviewCards = ({ datasetId }: any) => {
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

  console.log(datasetInfo);

  return (
    <Box className={classes.card}>
      <Box className={classes.cardHeading}>Overview</Box>
      {datasetInfo && (
        <Box className={classes.cardContent}>
          <CardEntry title="Missing %" value={datasetInfo?.dataset_overview.missing_percentage} />
          <CardEntry title="Total Data Rows" value={datasetInfo?.dataset_overview.total_row} />
          <CardEntry
            title="Total Duplicates"
            value={datasetInfo?.dataset_overview.duplicate_total}
          />
          <CardEntry title="Total Missing" value={datasetInfo?.dataset_overview.missing_total} />
          <CardEntry
            title="Duplicates %"
            value={datasetInfo?.dataset_overview.duplicate_percentage}
          />
        </Box>
      )}
    </Box>
  );
};
