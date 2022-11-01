import {
  Box,
  Grid,
  Table,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
  TableContainer,
  MenuItem,
  Menu,
  MenuProps,
  Button,
  Switch,
  Stack
} from '@material-ui/core';
import {
  experimentalStyled as styled,
  useTheme,
  makeStyles,
  alpha
} from '@material-ui/core/styles';
import { useParams } from 'react-router-dom';
import { Icon } from '@iconify/react';
import { useModelInfo } from '../../../../api/models/GetModelOverview';
import LoadingScreen from '../../../../components/LoadingScreen';
import ChartLine from '../../../../components/charts/ChartOverview';
import ChartSparkline from '../../../../components/charts/ChartSparkline';
import React, { useState } from 'react';
import { CardHeading, Heading } from '../../../../components/Heading';

import { useSelector } from '../../../../redux/store';
import { DateRangeFilterState } from '../../../../redux/slices/dateRangeFilter';
import FiberManualRecordIcon from '@material-ui/icons/FiberManualRecord';
import trendingUpFill from '@iconify/icons-eva/trending-up-fill';
import trendingDownFill from '@iconify/icons-eva/trending-down-fill';
import { formattedDate } from '../../../../utils/date';
import Scrollbar from 'components/Scrollbar';

import downwardOutline from '@iconify/icons-eva/arrow-ios-downward-outline';

import { colors } from '../../../../theme/colors';

const StyledMenu = styled((props: MenuProps) => (
  <Menu
    anchorOrigin={{
      vertical: 'bottom',
      horizontal: 'right'
    }}
    transformOrigin={{
      vertical: 'top',
      horizontal: 'right'
    }}
    {...props}
  />
))(({ theme }) => ({
  '& .MuiPaper-root': {
    background: colors.white,
    borderRadius: '4px',
    width: '172px',
    // height: '120px',
    '& .MuiMenu-list': {
      padding: '4px 0'
    },
    '& .MuiMenuItem-root': {
      '& .MuiSvgIcon-root': {
        fontFamily: 'Poppins',
        fontStyle: 'normal',
        fontWeight: 500,
        fontSize: '12px'
      },
      '&:active': {
        backgroundColor: colors.white
      }
    }
  }
}));
const IconWrapperStyle = styled('div')(({ theme }) => ({
  width: 24,
  height: 24,
  display: 'flex',
  borderRadius: '50%',
  alignItems: 'center',
  justifyContent: 'center',
  color: theme.palette.success.main,
  backgroundColor: alpha(theme.palette.success.main, 0.16)
}));

const useStyles = makeStyles(() => ({
  smallBox: {
    height: '160px',
    background: colors.white,
    boxShadow: '0px 0.5px 1.75px rgba(0, 0, 0, 0.039), 0px 1.85px 6.25px rgba(0, 0, 0, 0.19)',
    borderRadius: '4px',
    marginRight: '20px'
  },

  BoxSubHeading: {
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 400,
    fontSize: '.7rem',
    lineHeight: '15px',
    color: colors.text,
    marginTop: '6px'
  },
  modelDetailDiv: {
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 300,
    fontSize: '.7rem',
    color: colors.textLight,
    marginTop: '6px'
  },
  divNumber: {
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 400,
    fontSize: '34px',
    color: colors.text
  },
  container: {
    maxWidth: '100%',
    maxHeight: '270px',
    overflowX: 'hidden',
    borderWidth: '1px',
    borderStyle: 'solid',
    borderColor: colors.tableHeadBack,
    borderRadius: '4px'
  },
  tableHead: {
    root: {
      backgroundColor: colors.black
    },
    borderRadius: '4px',
    opacity: 1,
    height: '24px',
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 500,
    fontSize: '12px'
  },
  tableHeadCell: {
    root: {
      backgroundColor: colors.black
    },
    height: '24px',
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 600,
    fontSize: '12px',
    lineHeight: '22px',
    paddingTop: '3px',
    paddingBottom: '3px',
    color: colors.text,
    boxShadow: 'none !important',
    borderRadius: '0px !important',
    '&:first-child': { borderTopLeftRadius: '4px !important' },
    '&:last-child': { borderTopRightRadius: '4px !important' }
  },
  tableCell: {
    height: '24px',
    borderRightWidth: '1px',
    borderRightStyle: 'solid',
    borderRightColor: colors.tableHeadBack,
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 400,
    fontSize: '11px',
    color: colors.text,
    paddingTop: '3px',
    paddingBottom: '3px',
    '&:last-child': {
      borderRight: 0
    }
  },
  MenuText: {
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 500,
    fontSize: '.8rem',
    width: '100%',
    display: 'flex',
    justifyContent: 'space-between'
  }
}));

interface ModelColumn {
  id: 'name' | 'type' | 'date';
  label: string;
  align?: 'left' | 'center' | 'right';
  span: number;
}

const MODEL_DATA: ModelColumn[] = [
  { id: 'name', label: 'Name', span: 1, align: 'center' },
  { id: 'type', label: 'Type', span: 1, align: 'center' },
  { id: 'date', label: 'Date', align: 'center', span: 1 }
];

const ModelOverview = () => {
  const { modelId } = useParams();
  const theme = useTheme();

  const { fromDate, toDate } = useSelector(
    (state: { dateRangeFilter: DateRangeFilterState }) => state.dateRangeFilter
  );
  // console.log("fromDate")
  // console.log(fromDate ? fromDate.toISOString() : fromDate)
  // console.log(toDate ? toDate.toISOString() : toDate)

  const { data, isLoading } = useModelInfo({ id: modelId, start_date: fromDate, end_date: toDate });
  const modelInfo = data?.modelInfo;
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const PERCENT1 = data?.data.model_alerts.alert_percentage_change;
  const PERCENT2 = data?.data.model_alerts.alert_percentage_change;
  const [state, setState] = React.useState({
    T1: false,
    T2: false
  });

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState({
      ...state,
      [event.target.name]: event.target.checked
    });
  };

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  if (isLoading)
    return (
      <Box sx={{ height: 'calc(100vh - 150px)' }}>
        <LoadingScreen />
      </Box>
    );

  return (
    <>
      <Grid container sx={{ flexGrow: 1 }}>
        <Grid item container xs={12} sx={{ maxWidth: '90%', alignItems: 'stretch' }}>
          <Grid item xs={3}>
            <Box sx={{ p: 3 }} className={classes.smallBox}>
              <CardHeading heading="Model details" />
              <Grid item container xs={12}>
                <Grid item xs={6}>
                  <div className={classes.BoxSubHeading}>Name</div>
                </Grid>
                <Grid item xs={6}>
                  <div className={classes.modelDetailDiv}>{modelInfo?.name}</div>
                </Grid>
                <Grid item xs={6}>
                  <div className={classes.BoxSubHeading}>Model Type</div>
                </Grid>
                <Grid item xs={6}>
                  <div className={classes.modelDetailDiv}>{modelInfo?.modelType}</div>
                </Grid>
                <Grid item xs={6}>
                  <div className={classes.BoxSubHeading}>Data Type</div>
                </Grid>
                <Grid item xs={6}>
                  <div className={classes.modelDetailDiv}>{modelInfo?.dataType}</div>
                </Grid>
                <Grid item xs={6}>
                  <div className={classes.BoxSubHeading}>Description</div>
                </Grid>
                <Grid item xs={6}>
                  <div className={classes.modelDetailDiv}>{modelInfo?.description}</div>
                </Grid>
              </Grid>
            </Box>
          </Grid>
          <Grid item xs={3}>
            <Box sx={{ p: 3 }} className={classes.smallBox}>
              <CardHeading heading="Today's Prediction" />
              <Grid item container xs={12}>
                <Grid item xs={6}>
                  <div className={classes.divNumber}>
                    {data?.data.model_predictions.pred_yesterday}
                  </div>
                  <div>
                    <Stack
                      direction="row"
                      alignItems="center"
                      spacing={1}
                      sx={{
                        mb: 1,
                        mt: 0.5,
                        fontSize: '.8rem',
                        fontWeight: 500,
                        color: `${PERCENT2 > 0 ? colors.success : colors.error}`
                      }}
                    >
                      <IconWrapperStyle
                        sx={{
                          ...(PERCENT1 < 0
                            ? {
                                color: 'error.main',
                                bgcolor: alpha(theme.palette.error.main, 0.16)
                              }
                            : {
                                color: 'success.main',
                                bgcolor: alpha(theme.palette.success.main, 0.16)
                              }),
                          mr: 1
                        }}
                      >
                        <Icon
                          width={16}
                          height={16}
                          icon={PERCENT1 >= 0 ? trendingUpFill : trendingDownFill}
                        />
                      </IconWrapperStyle>
                      {data?.data.model_predictions.pred_yesterday_percentage_change}%
                    </Stack>
                  </div>
                </Grid>
                <Grid item xs={6}>
                  <ChartSparkline
                    colors={`${PERCENT1 >= 0 ? colors.success : colors.error}`}
                    data={data?.data.model_predictions.pred_trend_data}
                  />
                </Grid>
              </Grid>
            </Box>
          </Grid>
          <Grid item xs={3}>
            <Box sx={{ p: 3 }} className={classes.smallBox}>
              <CardHeading heading="Average Prediction" subtitle="Average Prediction" />

              <div className={classes.divNumber}>{data?.data.model_predictions.pred_average}</div>
              <Box sx={{ color: colors.textLight, fontSize: '.7rem', mt: 1, fontWeight: 500 }}>
                Last {data?.data.model_predictions.pred_average_window_days} days
              </Box>
            </Box>
          </Grid>
          <Grid item xs={3}>
            <Box sx={{ p: 3 }} className={classes.smallBox}>
              <CardHeading heading="No. of alerts trends" subtitle="No. of alerts trends" />
              <Grid item container xs={12}>
                <Grid item xs={6}>
                  <div className={classes.divNumber}>{data?.data.model_alerts.alerts_count}</div>
                  <div>
                    <Stack
                      direction="row"
                      alignItems="center"
                      spacing={1}
                      sx={{
                        mb: 1,
                        mt: 0.5,
                        fontSize: '.8rem',
                        fontWeight: 500,
                        color: `${PERCENT2 < 0 ? colors.success : colors.error}`
                      }}
                    >
                      <IconWrapperStyle
                        sx={{
                          ...(PERCENT2 >= 0
                            ? {
                                color: 'error.main',
                                bgcolor: alpha(theme.palette.error.main, 0.16)
                              }
                            : {
                                color: 'success.main',
                                bgcolor: alpha(theme.palette.success.main, 0.16)
                              }),
                          mr: 1
                        }}
                      >
                        <Icon
                          width={16}
                          height={16}
                          icon={PERCENT2 >= 0 ? trendingUpFill : trendingDownFill}
                        />
                      </IconWrapperStyle>
                      {data?.data.model_alerts.alert_percentage_change}%
                    </Stack>
                  </div>
                </Grid>
                <Grid item xs={6}>
                  <ChartSparkline
                    colors={`${PERCENT2 < 0 ? colors.success : colors.error}`}
                    data={data?.data.model_alerts.alert_trend_data}
                  />
                </Grid>
              </Grid>
            </Box>
          </Grid>
        </Grid>
        <Grid item container xs={12}>
          <Grid item xs={8}>
            <Box
              sx={{
                p: 3,
                background: colors.white,
                height: '360px',
                boxShadow:
                  '0px 0.5px 1.75px rgba(0, 0, 0, 0.039), 0px 1.85px 6.25px rgba(0, 0, 0, 0.19)',
                borderRadius: '4px',
                marginTop: '20px',
                marginBottom: '30px'
              }}
            >
              <Grid item container xs={12}>
                <Grid item xs={10}>
                  <Heading heading="PREDICTION VOLUME" subtitle="prediction volume" />
                </Grid>
                <Grid item xs={2}>
                  <div>
                    <Button
                      aria-controls={open ? 'demo-customized-menu' : undefined}
                      aria-haspopup="true"
                      aria-expanded={open ? 'true' : undefined}
                      variant="contained"
                      disableElevation
                      onClick={handleClick}
                      // endIcon={<Icon icon={arrowDown}  />}
                      style={{
                        fontFamily: 'Poppins',
                        fontStyle: 'normal',
                        fontWeight: 400,
                        fontSize: '13px',
                        color: colors.text,

                        background: colors.white,
                        border: `1px solid ${colors.tableHeadBack}`,
                        borderRadius: '2px',
                        width: '140px',
                        height: '30px',
                        boxShadow: 'none'
                      }}
                    >
                      Target class&nbsp;&nbsp;
                      <Icon width={16} height={16} icon={downwardOutline} />
                    </Button>
                    <StyledMenu
                      id="demo-customized-menu"
                      MenuListProps={{
                        'aria-labelledby': 'demo-customized-button'
                      }}
                      anchorEl={anchorEl}
                      open={open}
                      onClose={handleClose}
                    >
                      <MenuItem disableRipple className={classes.MenuText}>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <FiberManualRecordIcon
                            sx={{ color: colors.graphA, marginRight: '.4rem' }}
                          />
                          T1
                        </Box>
                        <Switch checked={state.T1} onChange={handleChange} name="T1" size="small" />
                      </MenuItem>
                      <MenuItem disableRipple className={classes.MenuText}>
                        <Box>
                          <FiberManualRecordIcon
                            sx={{ color: colors.graphB, marginRight: '.4rem' }}
                          />
                          T2
                        </Box>
                        <Switch checked={state.T2} onChange={handleChange} name="T2" size="small" />
                      </MenuItem>
                    </StyledMenu>
                  </div>
                </Grid>
              </Grid>
              <ChartLine
                state={state}
                data={data.data.model_prediction_graph ? data.data.model_prediction_graph : {}}
              />
            </Box>
          </Grid>
          <Grid item xs={4}>
            <Box
              sx={{
                p: 3,
                background: colors.white,
                boxShadow:
                  '0px 0.5px 1.75px rgba(0, 0, 0, 0.039), 0px 1.85px 6.25px rgba(0, 0, 0, 0.19)',
                borderRadius: '4px',
                marginTop: '20px',
                marginBottom: '30px',
                marginLeft: '20px',
                maxHeight: '360px'
              }}
            >
              <Heading heading="LATEST ALERTS" subtitle="Latest alerts" />
              <Scrollbar>
                <TableContainer className={classes.container}>
                  <Table>
                    <TableHead>
                      <TableRow className={classes.tableHead}>
                        {MODEL_DATA.map((column) => (
                          <TableCell
                            key={column.id}
                            align={column.align}
                            colSpan={column.span}
                            className={classes.tableHeadCell}
                          >
                            {column.label}
                          </TableCell>
                        ))}
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {data.data.model_alerts.alerts_list.map((rowData: any) => (
                        <TableRow key={rowData.monitor_name}>
                          <TableCell className={classes.tableCell} align="center">
                            {rowData.monitor_name}
                          </TableCell>
                          <TableCell className={classes.tableCell} align="center">
                            {rowData.monitor_type}
                          </TableCell>
                          <TableCell className={classes.tableCell} align="center">
                            {/* {formatDateTime(rowData.time)} */}
                            {formattedDate(rowData.time)}
                            {/*{rowData.time}*/}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Scrollbar>
            </Box>
          </Grid>
        </Grid>
      </Grid>
    </>
  );
};
export default ModelOverview;
