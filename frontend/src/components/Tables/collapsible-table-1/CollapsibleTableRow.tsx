import { Icon } from '@iconify/react';
import { useState } from 'react';
import arrowIosUpwardFill from '@iconify/icons-eva/arrow-ios-upward-fill';
import arrowIosDownwardFill from '@iconify/icons-eva/arrow-ios-downward-fill';

// material
import {
  Box,
  Table,
  Collapse,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
  Typography,
  IconButton
} from '@material-ui/core';
import { ChartBar } from 'components/charts';
import { makeStyles } from '@material-ui/core/styles';
import { colors } from '../../../theme/colors';

// ----------------------------------------------------------------------

const useStyles = makeStyles(() => ({
  openBack: {
    backgroundColor: colors.boxBackground
  },
  pointer: {
    '&:hover': {
      backgroundColor: colors.boxBackground,
      cursor: 'pointer'
    }
  },
  name: {
    textTransform: 'capitalize',
    fontWeight: 600,
    color: colors.textPrimary,
    fontSize: '0.875rem'
  },
  impact: {
    fontWeight: 500,
    color: colors.text,
    fontSize: '0.8rem'
  },
  minMax: { fontSize: '.75rem', fontWeight: 500 }
}));

export default function CollapsibleTableRow(props: { row: any }) {
  const classes = useStyles();
  const { row } = props;

  const [open, setOpen] = useState(false);

  return (
    <>
      <TableRow
        // onClick={() => {
        //   setOpen(!open);
        // }}
        sx={{ border: `1px solid ${colors.tableHeadBack}`, borderBottom: 0 }}
        className={`${open ? classes.openBack : ''} borderBottom`}
      >
        <TableCell className={classes.name}>
          <IconButton size="small" onClick={() => setOpen(!open)}>
            <Icon icon={open ? arrowIosUpwardFill : arrowIosDownwardFill} />
          </IconButton>
          &nbsp;
          {row.name}
        </TableCell>

        <TableCell style={{ display: 'flex', justifyContent: 'center' }}>
          <ChartBar
            name={row.name}
            categories={row.buckets}
            data={row.hist_values}
            options={{
              height: 60,
              width: '200',
              sparkline: true,
              enableDataLabels: false,
              showGridLines: false,
              showYAxisLabels: false,
              color: colors.graphDark,
              followCursor: true,
              tooltip: {
                enabled: true,
                followCursor: true,
                style: {
                  fontSize: '12px',
                  fontFamily: 'Poppins'
                },
                onDatasetHover: {
                  highlightDataSeries: false
                },
                x: {
                  show: false
                },
                y: {
                  formatter: undefined,
                  title: {
                    formatter: () => ''
                  }
                },
                marker: {
                  show: false
                }
              }
            }}
          />
        </TableCell>
        <TableCell align="center" width="20%">
          {Math.round(row.impact * 1000) / 1000}
        </TableCell>
      </TableRow>

      <TableRow sx={{ border: '1px solid #E5E8EB', borderTop: 0 }} className={classes.openBack}>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <>
              <Box className={classes.minMax}>
                Dataset {row.name}: Accuracy minimum is {Math.min(...row.hist_values)} and maximum
                is {Math.max(...row.hist_values)}
              </Box>
              <ChartBar
                name={row.name}
                categories={row.buckets}
                data={row.hist_values}
                options={{
                  height: 200,
                  width: '80%',
                  color: colors.graphLight,
                  enableDataLabels: false,
                  columnWidth: '50%'
                }}
              />
            </>
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
}
