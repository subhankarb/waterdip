import { useEffect, useState, useReducer } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery, UseQueryResult } from 'react-query';
import axios from '../../../utils/axios';
import { GET_MONITORS_API } from '../../../api/apis';
import MoreHorizIcon from '@material-ui/icons/MoreHoriz';
import { useSnackbar } from 'notistack';
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
  Switch
} from '@material-ui/core';
import { capitalize } from 'lodash';
import { makeStyles } from '@material-ui/core/styles';
import Scrollbar from '../../../components/Scrollbar';
import { colors } from '../../../theme/colors';
import '../../../pages/Models/ModelList/shadow.css';
import MonitorListToolbar from './MonitorListToolbar';
import { fontWeight } from '@material-ui/system';
import { useSelector } from '../../../redux/store';
import { ModelMonitorState } from '../../../redux/slices/ModelMonitorState';
import { useGetMonitors } from 'api/monitors/GetMonitors';
import { useMonitorDelete } from 'api/monitors/deleteMonitor';

interface ModelColumn {
  id: 'name' | 'type' | 'modelName' | 'date' | 'lastRun' | 'severity' | 'number' | 'action';
  label: string;
  minWidth?: number;
  align?: 'left' | 'center' | 'right';
  format?: (value: number) => string;
  span: number;
}
const MODEL_COLUMNS: ModelColumn[] = [
  { id: 'name', label: 'Monitor name', minWidth: 50, span: 1, align: 'center' },
  { id: 'type', label: 'Monitior Type', minWidth: 50, span: 1, align: 'center' },
  { id: 'modelName', label: 'Model Name', minWidth: 50, span: 1, align: 'center' },
  { id: 'date', label: 'Created at', minWidth: 50, span: 1, align: 'center' },
  { id: 'lastRun', label: 'Last run', minWidth: 50, span: 1, align: 'center' },
  { id: 'severity', label: 'Severity', minWidth: 50, span: 1, align: 'center' },
  { id: 'number', label: 'No. of alerts', minWidth: 50, span: 1, align: 'center' },
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

interface SortProps {
  monitor_name: 'asc' | 'desc' | undefined;
  created: 'asc' | 'desc' | undefined;
}

const MonitorListTable = (props: any) => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchName, setSearchName] = useState('');
  const [anchorEl, setAnchorEl] = useState<HTMLButtonElement | null>(null);
  const [ignored, forceUpdate] = useReducer((x) => x + 1, 0);

  const refetch = async () => {
    const monitors = await axios.get<any>(
      GET_MONITORS_API,
      {
        params: {
          query: searchName,
          page: page + 1,
          limit: rowsPerPage,
          ...(props.model_id && {model_id: props.model_id})
        }
      }
      
    );
    setMonitorList(monitors.data ? monitors.data.monitor_list : [])
  }
  const monitors = useGetMonitors({
    query: searchName,
    page: page + 1,
    limit: rowsPerPage,
    ...(props.model_id && {model_id: props.model_id})
  });
  const meta = monitors?.data?.data.meta || { page: 0, total: 0, limit: 10};
  const [monitorList, setMonitorList] = useState<any>(monitors.data ? monitors.data.data.monitor_list : []);
  const handleDelete = async (monitorId: string) => {
    await MonitorDelete(monitorId);
    setMonitorList(monitorList.filter((monitor : any) => monitor.monitor_id !== monitorId));
    forceUpdate();
    enqueueSnackbar('Deleted Monitor.', { variant: 'info' });
  }

  const { enqueueSnackbar } = useSnackbar();

  const { isDeleting, error, MonitorDelete } = useMonitorDelete();

  useEffect(() => {
    refetch();
  }, [ignored, searchName, page, rowsPerPage])

  const classes = useStyles();

  const { modelID } = useSelector(
    (state: { modelMonitorState: ModelMonitorState }) => state.modelMonitorState
  );

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
  const [openPopover, setOpenPopover] = useState('');
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>, id: string) => {
    if (id === openPopover) {
      setOpenPopover('');
      setAnchorEl(null);
    } else {
      setOpenPopover(id);
      setAnchorEl(event.currentTarget);
    }
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setOpenPopover('');
    setAnchorEl(null);
  };

  

  const open = Boolean(anchorEl);
  const id = open ? 'simple-popover' : undefined;

  return (
    <>
      <MonitorListToolbar searchName={searchName} onSearch={handleFilterByName} />
      <Card className={classes.card}>
        <Scrollbar>
          <TableContainer className={classes.tableContainer}>
            <Table className={classes.table}>
              <TableHead className={classes.tableHeading}>
                <TableRow className={classes.tableHead}>
                  {MODEL_COLUMNS.map((column) =>
                    column.id !== 'modelName' ? (
                      <TableCell
                        key={column.id}
                        align={column.align}
                        colSpan={column.span}
                        className={classes.tableHeadCell}
                      >
                        {column.label}
                      </TableCell>
                    ) : modelID === null ? (
                      <TableCell
                        key={column.id}
                        align={column.align}
                        colSpan={column.span}
                        className={classes.tableHeadCell}
                      >
                        {column.label}
                      </TableCell>
                    ) : null
                  )}
                </TableRow>
              </TableHead>
              <TableBody>
                {monitorList &&
                  monitorList.map((row: any) => (
                    <TableRow
                      key={row.id}
                      tabIndex={-1}
                      role="checkbox"
                      className={classes.tableRow}
                    >
                      <TableCell className={classes.tableCell} align="center">
                        {row.monitor_name}
                      </TableCell>
                      <TableCell className={classes.tableCell} align="center">
                        {row.monitor_type}
                      </TableCell>
                      {modelID === null ? (
                        <TableCell className={classes.tableCell} align="center">
                          {row.model_name}
                        </TableCell>
                      ) : null}

                      <TableCell className={classes.tableCell} align="center">
                        {row.monitor_type}
                      </TableCell>
                      <TableCell className={classes.tableCell} align="center">
                        {row.last_run}
                      </TableCell>
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
                        {capitalize(row.num_alerts)}
                      </TableCell>
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
                          onClick={(event) => handleClick(event, row.monitor_id)}
                        >
                          <MoreHorizIcon className={classes.icon} />
                        </Button>
                        <Popover
                          id={row.monitor_id}
                          open={row.monitor_id === openPopover}
                          anchorEl={anchorEl}
                          key={row.monitor_id}
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
                            <Button onClick={() => handleDelete(row.monitor_id)} className={classes.actionPopupBtn}>Delete</Button>
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
          page={meta.page}
          component="div"
          count={meta.total}
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

export default MonitorListTable;
