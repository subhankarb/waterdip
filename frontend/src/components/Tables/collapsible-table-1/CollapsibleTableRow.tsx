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

  return (
    <>
      <TableRow
        sx={{ border: `1px solid ${colors.tableHeadBack}`, borderBottom: 0 }}
        className= "borderBottom"
      >
        <TableCell className={classes.name}>
          &nbsp;
          {row.name}
        </TableCell>

        <TableCell align="center" width="20%">
          {Math.round(row.driftscore * 1000) / 1000}
        </TableCell>
      </TableRow>
    </>
  );
}
