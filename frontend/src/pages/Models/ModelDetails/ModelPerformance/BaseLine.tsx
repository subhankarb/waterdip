import { Heading } from '../../../../components/Heading';
import { makeStyles } from '@material-ui/styles';
import { useSelector } from '../../../../redux/store';
import { DateRangeFilterState } from '../../../../redux/slices/dateRangeFilter';
import { formatDateTime } from '../../../../utils/date';
import { Button } from '@material-ui/core';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { PATH_PAGE, PATH_DASHBOARD } from '../../../../routes/paths';
import { colors } from '../../../../theme/colors';
import { useMemo } from 'react';

const useStyles = makeStyles({
  baseLine: {
    paddingLeft: '.8rem',
    marginTop: '-2rem'
  },
  baseLineContent: {
    marginTop: '.6rem',
    width: '100%',
    color: colors.text,
    background: colors.boxBackground,
    borderRadius: '4px',
    padding: '1rem'
  },
  contentHeading: {
    fontSize: '.85rem',
    fontWeight: 600,
    letterSpacing: '.25px',
    marginBottom: '.5rem'
  },
  contentText: {
    fontSize: '.8rem',
    fontWeight: 500,
    letterSpacing: '.25px',
    padding: '.7rem 0 .5rem'
  },
  contentButton: {
    padding: '.5rem 0rem',
    fontSize: '.8rem',
    fontWeight: 500,
    letterSpacing: '.25px',
    color: colors.textPrimary
  }
});

function useQuery() {
  const { search } = useLocation();

  return useMemo(() => new URLSearchParams(search), [search]);
}

export default function BaseLine() {
  const navigate = useNavigate();
  const { modelId, tabName } = useParams();
  const classes = useStyles();
  let query = useQuery();
  const now = new Date();

  const { fromDate, toDate } = useSelector(
    (state: { dateRangeFilter: DateRangeFilterState }) => state.dateRangeFilter
  );

  const dateTimeString = `${formatDateTime(fromDate ? fromDate : now)} to ${formatDateTime(
    toDate ? toDate : now
  )} `;

  return (
    <div className={classes.baseLine}>
      <Heading heading="BaseLine" subtitle="baseline" />
      <div className={classes.baseLineContent}>
        <div className={classes.contentHeading}>Production</div>
        <hr />
        <div className={classes.contentText}>Date from {dateTimeString}</div>
        <Button
          className={classes.contentButton}
          onClick={() =>
            navigate(`${PATH_DASHBOARD.general.models}/${modelId}/configuration?version_id=${query.get('version_id')}`, {
              state: { baseline: true }
            })
          }
        >
          Configure baseline {'>'}
        </Button>
      </div>
    </div>
  );
}
