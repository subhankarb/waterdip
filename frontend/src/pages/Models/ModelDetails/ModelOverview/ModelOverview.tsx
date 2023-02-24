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
import { useModelOverview } from '../../../../api/models/GetModelOverview';
import LoadingScreen from '../../../../components/LoadingScreen';
import ChartLine from '../../../../components/charts/ChartOverview';
import { formatDateTime } from '../../../../utils/date';
import ChartSparkline from '../../../../components/charts/ChartSparkline';
import React, { useState, useEffect } from 'react';
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
    width: 'auto',
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
    height: 'auto',
    minHeight: '200px',
    background: colors.white,
    boxShadow: '0px 0.5px 1.75px rgba(0, 0, 0, 0.039), 0px 1.85px 6.25px rgba(0, 0, 0, 0.19)',
    borderRadius: '4px',
    marginRight: '20px',
  },

  BoxSubHeading: {
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 400,
    fontSize: '.8rem',
    lineHeight: '15px',
    color: colors.text,
    marginTop: '6px'
  },
  modelDetailDiv: {
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 300,
    fontSize: '.8rem',
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

  const { data, isLoading } = useModelOverview({ id: modelId });
  console.log('DATA: ',data);
  const modelInfo = {
    numberOfVersions: data ? data.data.number_of_model_versions : 0,
    latestVersion: data ? data.data.latest_version.model_version.toUpperCase() : "V1",
    createTime: data ? formattedDate(data.data.latest_version_created_at) : '22 Dec 2022',
  }
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const [state, setState] = useState([]);
  useEffect(() => {
    if (data) {
      setState(
        data.data.model_prediction_hist.predictions_versions.map((item: any) => {
          const id = Object.keys(item)[0];
          return { [id]: false };
        })
      );
    }
  }, [data]);


  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  if (isLoading && data?.data)
    return (
      <Box sx={{ height: 'calc(100vh - 150px)' }}>
        <LoadingScreen />
      </Box>
    );
  const PERCENT1 = data?.data?.model_prediction_overview.pred_percentage_change;
  const PERCENT2 = data?.data?.model_alert_overview.alert_percentage_change;
  return (
    <>
      <Grid container sx={{ flexGrow: 1 }}>
        <Grid item container spacing={3} xs={12} sx={{ maxWidth: '90%', alignItems: 'stretch' }}>
          <Grid item xs={12} sm={6} md={6} lg={3}>
            <Box sx={{ p: 3 }} className={classes.smallBox}>
              <CardHeading heading="Model details" />
              <Grid item container xs={12}>
                <Grid item xs={6}>
                  <div className={classes.BoxSubHeading}>Number of versions</div>
                </Grid>
                <Grid item xs={6}>
                  <div className={classes.modelDetailDiv}>{modelInfo?.numberOfVersions}</div>
                </Grid>
                <Grid item xs={6}>
                  <div className={classes.BoxSubHeading}>Latest Version</div>
                </Grid>
                <Grid item xs={6}>
                  <div className={classes.modelDetailDiv}>{modelInfo?.latestVersion}</div>
                </Grid>
                <Grid item xs={6}>
                  <div className={classes.BoxSubHeading}>Created Time</div>
                </Grid>
                <Grid item xs={6}>
                  <div className={classes.modelDetailDiv}>{modelInfo?.createTime}</div>
                </Grid>
              </Grid>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={6} lg={3}>
            <Box sx={{ p: 3 }} className={classes.smallBox}>
              <CardHeading heading="Today's Prediction" subtitle={`Prediction volume changed ${PERCENT1}% compare to last 7 days average`}/>
              <Grid item container xs={12}>
                <Grid item xs={6}>
                  <div className={classes.divNumber}>
                    {data?.data.model_prediction_overview.pred_yesterday}
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
                        color: `${PERCENT2 && PERCENT2 > 0 ? colors.success : colors.error}`
                      }}
                    >
                      <IconWrapperStyle
                        sx={{
                          ...(PERCENT1 && PERCENT1 < 0
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
                          icon={PERCENT1 && PERCENT1 >= 0 ? trendingUpFill : trendingDownFill}
                        />
                      </IconWrapperStyle>
                      {data?.data.model_prediction_overview.pred_percentage_change}%
                    </Stack>
                  </div>
                </Grid>
                <Grid item xs={6}>
                  {data &&
                    <ChartSparkline
                      colors={`${PERCENT1 && PERCENT1 >= 0 ? colors.success : colors.error}`}
                      data={data?.data.model_prediction_overview.pred_trend_data}
                    />
                  }

                </Grid>
              </Grid>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={6} lg={3}>
            <Box sx={{ p: 3 }} className={classes.smallBox}>
              <CardHeading heading="Average Prediction" subtitle="Average prediction volume in last 7 days" />

              <div className={classes.divNumber}>{data?.data.model_prediction_overview.pred_average}</div>
              <Box sx={{ color: colors.textLight, fontSize: '.7rem', mt: 1, fontWeight: 500 }}>
                Last {data?.data.model_prediction_overview.pred_average_window_days} days
              </Box>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={6} lg={3}>
            <Box sx={{ p: 3 }} className={classes.smallBox}>
              <CardHeading heading="No. of alerts trends" subtitle="No. of alerts trends" />
              <Grid item container xs={12}>
                <Grid item xs={6}>
                  <div className={classes.divNumber}>{data?.data.model_alert_overview.alerts_count}</div>
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
                        color: `${PERCENT2 && PERCENT2 < 0 ? colors.success : colors.error}`
                      }}
                    >
                      <IconWrapperStyle
                        sx={{
                          ...(PERCENT2 && PERCENT2 >= 0
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
                          icon={PERCENT2 && PERCENT2 >= 0 ? trendingUpFill : trendingDownFill}
                        />
                      </IconWrapperStyle>
                      {data?.data.model_alert_overview.alert_percentage_change}%
                    </Stack>
                  </div>
                </Grid>
                <Grid item xs={6}>
                  {data &&
                    <ChartSparkline
                      colors={`${PERCENT2 && PERCENT2 < 0 ? colors.success : colors.error}`}
                      data={data?.data.model_alert_overview.alert_trend_data}
                    />
                  }

                </Grid>
              </Grid>
            </Box>
          </Grid>
        </Grid>
        <Grid item container spacing={3} xs={12} sx={{ maxWidth: '90%' }}>
          <Grid item xs={12} sm={12} md={12} lg={8} >
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
              <Grid item container justifyContent="space-between" xs={12}>
                <Grid item>
                  <Heading heading="PREDICTION VOLUME" subtitle="Model prediction volume per day" />
                </Grid>
                <Grid item>
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
                        width: '160px',
                        height: '30px',
                        boxShadow: 'none'
                      }}
                    >
                      Model Version&nbsp;&nbsp;
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
                      {state.map((item, index) => (
                        <MenuItem disableRipple className={classes.MenuText}>
                          <Box>
                            <FiberManualRecordIcon
                              sx={{ color: colors.graphB, marginRight: '.4rem' }}
                            />
                            {Object.keys(item)[0]}
                          </Box>
                          <Switch value={item[Object.keys(item)[0]]} checked={item[Object.keys(item)[0]]} 
                          onChange={() => setState((prevItems: any) =>
                              prevItems.map((prevItem: any) => {
                                if (prevItem === item) {
                                  return { [Object.keys(prevItem)[0]]: !prevItem[Object.keys(prevItem)[0]] };
                                }
        
                                return prevItem;
                              })
                            )} 
                          name={Object.keys(item)[0]} size="small" />
                        </MenuItem>
                      ))}

                      
                    </StyledMenu>
                  </div>
                </Grid>
              </Grid>
              { data && state.length > 0 ? (
                <ChartLine
                  state={state}
                  data={data.data.model_prediction_hist}
                />
                ) : null}

            </Box>
          </Grid>
          <Grid item xs={12} sm={12} md={12} lg={4} >
            <Box
              sx={{
                p: 3,
                height: '360px',
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
              <Heading heading="LATEST ALERTS" subtitle="Last five alerts" />
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
                      {data && data.data.model_alert_list.map((rowData: any) => (
                        <TableRow key={rowData.monitor_name}>
                          <TableCell className={classes.tableCell} align="center">
                            {rowData.monitor_name}
                          </TableCell>
                          <TableCell className={classes.tableCell} align="center">
                            {rowData.monitor_type}
                          </TableCell>
                          <TableCell className={classes.tableCell} align="center">
                            {formatDateTime(rowData.time)}
                            {formattedDate(rowData.time)}
                            {rowData.time}
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
