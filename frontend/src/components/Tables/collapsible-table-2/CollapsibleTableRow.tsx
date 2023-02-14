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
    backgroundColor: colors.boxBackground,
    width: '100%'
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
  tableCell: {
    fontSize: '.8rem',
    fontWeight: 500
  },
  minMax: { fontSize: '.75rem', fontWeight: 500 },
  span: {
    background: 'rgba(103, 128, 220, 0.16)',
    borderRadius: '6px',
    color: colors.textPrimary,
    display: 'inline-block',
    padding: '0.2rem 0.7rem',
    fontWeight: 600
  }
}));

export default function CollapsibleTableRow(props: { row: any, data_type: any }) {
  const classes = useStyles();
  const { row, data_type } = props;
  console.log(row);
  const [open, setOpen] = useState(false);

  return (
    <>
      <TableRow
        sx={{ border: `1px solid ${colors.tableHeadBack}`, borderBottom: 0 }}
        className={`${open ? classes.openBack : ''} borderBottom`}
      >
        <TableCell className={(classes.tableCell, classes.name)}>{
          row.histogram && Object.keys(row.histogram).length !== 0 ?
          <IconButton size="small" onClick={() => setOpen(!open)}>
            <Icon icon={open ? arrowIosUpwardFill : arrowIosDownwardFill} />
          </IconButton> : null
          }
          &nbsp;
          {row.column_name}
        </TableCell>

        {row.histogram && Object.keys(row.histogram).length !== 0 ? (
          <TableCell
            className={classes.tableCell}
            style={{ display: 'flex', justifyContent: 'center' }}
          >
            <ChartBar
              name={row.column_name}
              categories={row.histogram.bins}
              data={row.histogram.val}
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
        ): <TableCell className={classes.tableCell} align="center">
        No Data Available
      </TableCell>}
        {data_type === 'NUMERIC' && (
          <TableCell className={classes.tableCell} align="center">
            {row.zeros}&nbsp;&nbsp;
            <span className={classes.span}>{row.total === 0 ? 0 : row.zeros / row.total}%</span>
          </TableCell>
        )}

        <TableCell className={classes.tableCell} align="center">
          {row.missing_total}&nbsp;&nbsp;
          <span className={classes.span}>{row.missing_percentage}%</span>
        </TableCell>
        {data_type === 'NUMERIC' ? (
          <>
            <TableCell className={classes.tableCell} align="center">
              {row.range ? <>{row.range}</> : <>-</>}
            </TableCell>
            <TableCell className={classes.tableCell} align="center">
              {row.mean ? <>{row.mean}</> : <>-</>}
            </TableCell>
            <TableCell className={classes.tableCell} align="center">
              {row.variance ? <>{row.variance}</> : <>-</>}
            </TableCell>
            <TableCell className={classes.tableCell} align="center">
              {row.std_dev}
            </TableCell>
          </>
        ) : (
          <>
            <TableCell className={classes.tableCell} align="center">
              {row.unique ? <>{row.unique}</> : <>-</>}
            </TableCell>
            <TableCell className={classes.tableCell} align="center">
              {row.top ? <>{row.top}</> : <>-</>}
            </TableCell>
          </>
        )}
      </TableRow>

      <TableRow
        sx={{ border: `1px solid ${colors.tableHeadBack}`, borderTop: 0 }}
        className={classes.openBack}
      >
        <TableCell
          className={classes.tableCell}
          style={{ paddingBottom: 0, paddingTop: 0 }}
          colSpan={10}
        >
          <Collapse in={open} timeout="auto" unmountOnExit>
            <>
              <Box className={classes.minMax}>
                Dataset {row.column_name}: Accuracy minimum is {Math.min(...row.histogram.val)} and
                maximum is {Math.max(...row.histogram.val)}
              </Box>
              <ChartBar
                name={row.column_name}
                categories={row.histogram.bins}
                data={row.histogram.val}
                options={{
                  height: 200,
                  width: '70%',
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
