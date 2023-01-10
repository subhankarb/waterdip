import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import MoreHorizIcon from '@material-ui/icons/MoreHoriz';
import {
  Table,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
  TableContainer,
  TablePagination,
  Card,
  Popover,
  Box,
  Button,
  CircularProgress,
  Switch,
  TableSortLabel
} from '@material-ui/core';
import { capitalize } from 'lodash';
import { makeStyles } from '@material-ui/core/styles';
import Scrollbar from '../../components/Scrollbar';
import { colors } from '../../theme/colors';
import AlertListToolbar from './AlertListToolbar';
import '../../pages/Models/ModelList/shadow.css';
import { fontWeight } from '@material-ui/system';
import { useSelector } from '../../redux/store';
import { usePaginatedAlerts } from '../../api/alerts/GetAlerts';

interface AlertColumn {
  id: 'severity' | 'status' | 'time' | 'monitorName' | 'monitorType' | 'name' | 'action';
  label: string;
  minWidth?: number;
  align?: 'left' | 'center' | 'right';
  format?: (value: number) => string;
  span: number;
}
const ALERT_COLUMNS: AlertColumn[] = [
  { id: 'severity', label: 'Severity', minWidth: 50, span: 1, align: 'center' },
  { id: 'status', label: 'Status', minWidth: 50, span: 1, align: 'center' },
  { id: 'time', label: 'Time', minWidth: 50, span: 1, align: 'center' },
  { id: 'monitorName', label: 'Monitor Name', minWidth: 50, span: 1, align: 'center' },
  { id: 'monitorType', label: 'Monitor Type', minWidth: 50, span: 1, align: 'center' },
  { id: 'name', label: 'Model Name', minWidth: 50, span: 1, align: 'center' },
  { id: 'action', label: 'Action', minWidth: 50, span: 1, align: 'center' }
];
const useStyles = makeStyles(() => ({
  card: {
    backgroundColor: colors.white,
    borderRadius: '10px',
    marginBottom: '20px'
  },
  tableContainer: {
    width: '100%',
    overflowX: 'hidden'
  },
  table: {
    width: '100%',
    margin: 0
  },
  tableHeading: {
    width: '100%'
  },
  tableHead: {
    root: {
      backgroundColor: colors.black
    },
    opacity: 1,
    height: 40,
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 600,
    fontSize: '14px',
    lineHeight: '22px'
  },
  tableHeadCell: {
    root: {
      backgroundColor: colors.black
    },
    backgroundColor: colors.tableHeadBack,
    height: 40,
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 600,
    fontSize: '14px',
    lineHeight: '22px',
    color: colors.text
  },
  tableRow: {
    borderBottom: `1.1px solid ${colors.tableHeadBack}`
  },
  tableCell: {
    height: 40,
    borderRightWidth: '1px',
    borderRightStyle: 'solid',
    borderRightColor: colors.tableHeadBack,
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 400,
    fontSize: '14px',
    lineHeight: '22px',
    color: colors.text,
    '&:last-child': {
      borderRight: 0
    }
  },
  pagination: {
    fontFamily: 'Public Sans',
    fontStyle: 'normal',
    fontWeight: 400,
    fontSize: '14px',
    lineHeight: '22px',
    color: colors.text
  },
  actionBtn: {
    padding: 0,
    margin: 0,
    color: colors.textLight,
    '& :hover': {
      backgroundColor: 'rgba(103, 128, 220, 0.2)',
      color: colors.textPrimary,
      borderRadius: '4px'
    },
    borderRadius: '4px',
    letterSpacing: 3.6,
    fontWeight: 900
  },
  popupBox: {
    '& .css-1p14d49-MuiPaper-root-MuiPopover-paper': {
      borderRadius: '4px !important'
    },
    borderRadius: '4px !important'
  },
  icon: {
    '&:hover': {
      backgroundColor: 'transparent'
    }
  },
  actionPopup: {
    display: 'flex',
    flexDirection: 'column',
    borderRadius: '4px'
  },
  actionPopupBtn: {
    padding: '.5rem 2rem',
    borderRadius: '4px',
    color: colors.textLight,
    fontWeight: 500,
    // borderBottom: `1px solid ${colors.textLight}`,
    '&:last-child': {
      borderBottom: 0
    },
    '& :hover': {
      color: colors.textPrimary
    }
  },
  severnityText: {
    display: 'inline-block',
    padding: '.25rem .85rem',
    fontSize: '.8rem',
    fontWeight: 500,
    color: colors.text,
    borderRadius: '4px'
  },
  low: { background: colors.low },
  medium: { background: colors.medium },
  high: { background: colors.high }
}));

type modelProps = {
  value: string;
};
interface SortProps {
  name: 'asc' | 'desc' | undefined;
}
const AlertListTable = ({ value }: modelProps) => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchName, setSearchName] = useState('');
  const [anchorEl, setAnchorEl] = useState<HTMLButtonElement | null>(null);
  const [orderDirection, setOrderDirection] = useState<SortProps>({
    name: 'asc'
  });
  const { data, isLoading } = usePaginatedAlerts({
    query: searchName,
    page: page + 1,
    limit: rowsPerPage,
    sort: orderDirection.name === 'asc' ? 'name_asc' : 'name_desc'
  });
  const alertList = data?.alertList || [];
  const meta = data?.meta || { page: 0, total: 0, limit: 10, sort: 'name_asc' };

  const classes = useStyles();

  const handleChangePage = (_event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setPage(page);
  };

  const handleFilterByName = (searchName: string) => {
    setSearchName(searchName);
  };
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleSortRequest = () => {
    orderDirection.name === 'asc'
      ? setOrderDirection({ name: 'desc' })
      : setOrderDirection({ name: 'asc' });
  };

  const open = Boolean(anchorEl);
  const id = open ? 'simple-popover' : undefined;

  return (
    <>
      <AlertListToolbar searchName={searchName} onSearch={handleFilterByName} />
      <Card className={classes.card}>
        <Scrollbar>
          <TableContainer className={classes.tableContainer}>
            <Table className={classes.table}>
              <TableHead className={classes.tableHeading}>
                <TableRow className={classes.tableHead}>
                  {ALERT_COLUMNS.map((column) =>
                    column.id !== 'name' ? (
                      <TableCell
                        key={column.id}
                        align={column.align}
                        colSpan={column.span}
                        className={classes.tableHeadCell}
                      >
                        {column.label}
                      </TableCell>
                    ) : value !== 'Model' ? (
                      <TableCell
                        key={column.id}
                        align={column.align}
                        colSpan={column.span}
                        className={classes.tableHeadCell}
                        onClick={() => handleSortRequest()}
                      >
                        <TableSortLabel active={true} direction={orderDirection.name}>
                          {column.label}&nbsp;
                        </TableSortLabel>
                      </TableCell>
                    ) : null
                  )}
                </TableRow>
              </TableHead>
              <TableBody>
                {alertList &&
                  alertList.map((row: any) => (
                    <TableRow
                      key={row.id}
                      tabIndex={-1}
                      role="checkbox"
                      className={classes.tableRow}
                    >
                      <TableCell className={classes.tableCell} align="center">
                        <Box
                          className={`${classes.severnityText} ${
                            row.severity === 'low' && `${classes.low}`
                          } ${row.severity === 'medium' && `${classes.medium}`} ${
                            row.severity === 'high' && `${classes.high}`
                          }`}
                        >
                          {capitalize(row.severity)}
                        </Box>
                      </TableCell>
                      <TableCell className={classes.tableCell} align="center">
                        {row.status}
                      </TableCell>
                      <TableCell className={classes.tableCell} align="center">
                        {row.time}
                      </TableCell>
                      <TableCell className={classes.tableCell} align="center">
                        {row.monitorName}
                      </TableCell>
                      <TableCell className={classes.tableCell} align="center">
                        {row.monitorMethod}
                      </TableCell>
                      {value !== 'Model' ? (
                        <TableCell className={classes.tableCell} align="center">
                          {row.modelId}
                        </TableCell>
                      ) : null}
                      <TableCell
                        className={classes.tableCell}
                        align="center"
                        sx={{
                          borderRightWidth: '0px',
                          borderRightColor: colors.white,
                          color: 'black'
                        }}
                      >
                        <Button
                          className={classes.actionBtn}
                          aria-describedby={id}
                          onClick={handleClick}
                        >
                          <MoreHorizIcon className={classes.icon} />
                        </Button>
                        <Popover
                          id={id}
                          open={open}
                          anchorEl={anchorEl}
                          onClose={handleClose}
                          anchorOrigin={{
                            vertical: 'bottom',
                            horizontal: 'left'
                          }}
                          className={classes.popupBox}
                        >
                          <Box className={classes.actionPopup}>
                            <Button className={classes.actionPopupBtn}>Disable</Button>
                            <Button className={classes.actionPopupBtn}>Edit</Button>
                            <Button className={classes.actionPopupBtn}>Delete</Button>
                          </Box>
                        </Popover>
                      </TableCell>
                    </TableRow>
                  ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Scrollbar>

        <TablePagination
          page={0}
          component="div"
          count={0}
          rowsPerPage={rowsPerPage}
          onPageChange={handleChangePage}
          rowsPerPageOptions={[5, 10, 50]}
          onRowsPerPageChange={handleChangeRowsPerPage}
          className={classes.pagination}
        />
      </Card>
    </>
  );
};

export default AlertListTable;
