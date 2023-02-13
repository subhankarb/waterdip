import { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import DateRangeSelect from './DateRangeSelect';
import { formatDateTime } from '../../../../utils/date';
import trashOutline from '@iconify/icons-eva/trash-outline';
import { Icon } from '@iconify/react';
import { Box, TextField, MenuItem, Button } from '@material-ui/core';
import { Grid } from '@material-ui/core';
import { colors } from '../../../../theme/colors';
import { useModelDelete } from 'api/models/DeleteModel';
import { useNavigate, useParams } from 'react-router';
import { PATH_DASHBOARD } from 'routes/paths';
import { useModelUpdate } from 'api/models/UpdateModel';
import { useSnackbar } from 'notistack';

const useStyles = makeStyles(() => ({
  outerBox: {
    background: '#FFFFFF',
    boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.08)',
    borderRadius: '0px',
    width: '100%',
    paddingTop: '20px',
    paddingBottom: '20px'
  },
  boxButton: {
    width: '100%',
    height: '40px',
    background: '#ffffff',
    '&:hover': {
      background: 'rgba(103, 128, 220, 0.2)'
    },
    borderWidth: '0px',
    borderRadius: '0px',
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 500,
    fontSize: '14px',
    color: '#212B36',
    textAlign: 'left',
    paddingLeft: '30px'
  },
  boxHeading: {
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 500,
    fontSize: '13px',
    color: '#000000',
    paddingLeft: '30px',
    paddingRight: '30px'
  },
  dateBoxButton: {
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 500,
    fontSize: '14px',
    color: '#B00020',
    borderWidth: '0px',
    background: '#ffffff',
    float: 'right'
  },
  boxDiv: {
    paddingLeft: '30px',
    paddingRight: '30px'
  },
  confiText: {
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 500,
    fontSize: '12px',
    color: '#212B36',
    paddingLeft: '30px',
    paddingRight: '30px',
    marginTop: '18px',
    marginBottom: '30px'
  },
  confiBackButton: {
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 500,
    fontSize: '15px',
    color: '#6780DC',
    borderColor: '#6780DC',
    borderRadius: '4px',
    float: 'right',
    width: '64px',
    height: '30px',
    marginLeft: '12px',
    background: '#ffffff',
    borderWidth: '1px'
  },
  confiSaveButton: {
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 500,
    fontSize: '13px',
    color: '#ffffff',
    background: '#6780DC',
    // boxShadow: '0px 4px 10px rgba(103, 128, 220, 0.24)',
    borderRadius: '4px',
    borderColor: '#6780DC',
    float: 'right',
    marginLeft: '30px',
    width: '64px',
    height: '30px',
    borderWidth: '1px'
  },
  confiDeleteButton: {
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 500,
    fontSize: '13px',
    color: '#ffffff',
    background: '#B00020',
    // boxShadow: '0px 4px 10px rgba(103, 128, 220, 0.24)',
    borderRadius: '4px',
    borderColor: '#B00020',
    float: 'right',
    marginLeft: '12px',
    width: '64px',
    height: '20px',
    borderWidth: '1px',
    marginTop: '10px'
  },
  confiNoButton: {
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 500,
    fontSize: '13px',
    color: '#6780DC',
    borderColor: '#6780DC',
    borderRadius: '4px',
    float: 'right',
    width: '64px',
    height: '20px',
    marginLeft: '12px',
    background: '#ffffff',
    borderWidth: '1px',
    marginTop: '10px'
  },
  confiYesButton: {
    fontFamily: 'Poppins',
    fontStyle: 'normal',
    fontWeight: 500,
    fontSize: '13px',
    color: '#B00020',
    borderColor: '#B00020',
    borderRadius: '4px',
    float: 'right',
    width: '64px',
    height: '20px',
    marginLeft: '12px',
    background: '#ffffff',
    borderWidth: '1px',
    marginTop: '10px'
  },
  baseLineContent: {
    width: '100%',
    borderRadius: '4px',
    paddingTop: '1rem',
    paddingLeft: '1.1rem',
    paddingRight: '1.1rem'
  },
  btnContainer: {
    display: 'flex',
    justifyContent: 'flex-end'
  },
  btn: {
    paddingLeft: '1.5rem',
    paddingRight: '1.5rem',
    background: colors.textPrimary,
    letterSpacing: '.1rem'
  }
}));

type Props = {
  onSave: Function;
  onSelect: Function;
  stringToMilliseconds: Function;
};

export const DialogBoxPart = ({ onSave, onSelect, stringToMilliseconds }: Props) => {
  const now = new Date();
  const classes = useStyles();
  const [boxDisplay, setBoxDisplay] = useState(true);
  const [timeDisplay, setTimeDisplay] = useState(false);
  const [selectDate, setSelectDate] = useState(false);
  const [selectNumDays, setSelectNumDays] = useState(false);
  const [confiDisplay, setconfiDisplay] = useState(false);
  const [dataDisplay, setDataDisplay] = useState(false);
  const [dateRange, setDateRange] = useState([new Date(now.getTime() - 5 * 60 * 60 * 1000), now]);
  const [days, setDays] = useState<string>('');
  const [data, setData] = useState<string>('');
  const [expandForm, setExpandForm] = useState(true);
  const { isUpdating, error, ModelUpdate } = useModelUpdate();
  const { modelId } = useParams();
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    onSave(expandForm);
    if (expandForm === false) {
      onSelect(dateRange);
    }
  }, [expandForm]);
  
  const handleSelect = (data: any, boxShow: any) => {
    setDateRange(data);
    setSelectDate(boxShow);
    setconfiDisplay(!boxShow);
  };

  return (
    <>
      {boxDisplay === true ? (
        <div className={classes.outerBox}>
          <button
            type="button"
            className={classes.boxButton}
            onClick={() => {
              setBoxDisplay(false);
              setTimeDisplay(true);
            }}
          >
            Production Data
          </button>
          <button
            type="button"
            className={classes.boxButton}
            onClick={() => {
              setBoxDisplay(false);
              setDataDisplay(true);
            }}
          >
            {' '}
            Dataset Environment
          </button>
        </div>
      ) : null}
      {timeDisplay === true ? (
        <div className={classes.outerBox}>
          <button
            type="button"
            className={classes.boxButton}
            onClick={() => {
              setTimeDisplay(false);
              setSelectDate(true);
            }}
          >
            Fixed Time Window
          </button>
          <button
            type="button"
            className={classes.boxButton}
            onClick={() => {
              setTimeDisplay(false);
              setSelectNumDays(true);
            }}
          >
            {' '}
            Moving Time Window
          </button>
        </div>
      ) : null}
      {selectNumDays == true? (
        <div className={classes.outerBox}>
          <div className={classes.boxHeading}>
            Select Moving Time Period
          </div>
          <Box className={classes.baseLineContent}>
            <TextField
              fullWidth
              type="number" 
              label="Number of Days"
              value={days}
              InputProps={{
                inputProps: { min: 0 }
              }}
              onKeyPress={(event) => {
                if (event?.key === '-' || event?.key === '+') {
                  event.preventDefault();
                }
              }}
              onChange={(e) => setDays(e.target.value)}
              sx={{ mt: 2, mb: 2.5 }}
              placeholder="7"
            >
            </TextField>
          </Box>
          <div className={classes.boxDiv}>
            <button
              type="button"
              className={classes.confiSaveButton}
              onClick={async () => {
                if (days === "") {
                  enqueueSnackbar(`Enter a valid number!`, { variant: 'error' });
                  return;
                };
                await ModelUpdate({
                  model_id: modelId,
                  property_name: "baseline",
                  baseline: {
                    time_window : {
                      time_window_type: "MOVING_TIME_WINDOW",
                      moving_time_window: {
                        time_period: days+"d"
                      }
                    }
                  }
                })
                if (error) {
                  enqueueSnackbar(`Something went wrong!`, { variant: 'error' });
                }
                else if (!isUpdating) {
                  enqueueSnackbar(`Updated Successfully`, { variant: 'success' });
                  setDateRange([new Date(now.getTime() - stringToMilliseconds(days)), new Date(now.getTime())])
                }
                setExpandForm(false);
              }}
            >
              save
            </button>
            <button
              type="button"
              className={classes.confiBackButton}
              onClick={() => {
                setSelectNumDays(false);
                setTimeDisplay(true);
              }}
            >
              back
            </button>
          </div>
        </div>
      ) : null }
      {selectDate === true ? (
        <div className={classes.outerBox}>
          <div className={classes.boxHeading}>
            Select Date Range{' '}
            <button
              type="button"
              onClick={() => {
                setSelectDate(false);
                setTimeDisplay(true);
              }}
              className={classes.dateBoxButton}
            >
              cancel
            </button>
          </div>
          <div className={classes.boxDiv}>
            <DateRangeSelect onSelect={handleSelect} />
          </div>
        </div>
      ) : null}
      {confiDisplay === true ? (
        <div className={classes.outerBox}>
          <div className={classes.boxHeading}>Confirm your baseline</div>
          <div className={classes.confiText}>
            Production between {formatDateTime(dateRange[0] ? dateRange[0] : now)} and{' '}
            {formatDateTime(dateRange[1] ? dateRange[1] : now)}
          </div>
          <div className={classes.boxDiv}>
            <button
              type="button"
              className={classes.confiSaveButton}
              onClick={async () => {
                await ModelUpdate({
                  model_id: modelId,
                  property_name: "baseline",
                  baseline: {
                    time_window : {
                      time_window_type: "FIXED_TIME_WINDOW",
                      fixed_time_window:  {
                        start_time: dateRange[0].toISOString(),
                        end_time: dateRange[1].toISOString()
                      }
                    }
                  }
                })
                if (error) {
                  enqueueSnackbar(`Something went wrong!`, { variant: 'error' });
                }
                else if (!isUpdating) {
                  enqueueSnackbar(`Updated Successfully`, { variant: 'success' });
                }
                setExpandForm(false);
              }}
            >
              save
            </button>
            <button
              type="button"
              className={classes.confiBackButton}
              onClick={() => {
                setconfiDisplay(false);
                setSelectDate(true);
              }}
            >
              back
            </button>
          </div>
        </div>
      ) : null}
      {dataDisplay === true ? (
        <div className={classes.outerBox}>
          <div className={classes.boxHeading}>
            Select Dataset Environment from below list{' '}
            <button
              type="button"
              className={classes.dateBoxButton}
              onClick={() => {
                setBoxDisplay(true);
                setDataDisplay(false);
              }}
            >
              cancel
            </button>
          </div>
          <Box className={classes.baseLineContent}>
          <TextField
            select
            fullWidth
            label="Select positive class"
            value={data}
            onChange={(e) => setData(e.target.value)}
            sx={{ mt: 2, mb: 2.5 }}
            placeholder="Select Environment"
          >
          <MenuItem value="TRAINING">Training</MenuItem>
          <MenuItem value="TESTING">Testing</MenuItem>
          <MenuItem value="VALIDATION">Validation</MenuItem>

        </TextField>
        <Box className={classes.btnContainer}>
          {
            data &&
            <Button variant="contained" className={classes.btn}
              onClick={async () => {
                await ModelUpdate({
                  model_id: modelId,
                  property_name: "baseline",
                  baseline: {
                    dataset_env: data
                  }
                })
                if (error) {
                  enqueueSnackbar(`Something went wrong!`, { variant: 'error' });
                }
                else if (!isUpdating) {
                  enqueueSnackbar(`Updated Successfully`, { variant: 'success' });
                }
                setExpandForm(false);
              }}
            >
              Save
            </Button>
          } 
        </Box>
        </Box>
        </div>
      ) : null}
    </>
  );
};

type DeleteProps = {
  onDelete: Function;
};

export const DeleteDialogBox = ({ onDelete }: DeleteProps) => {
  const classes = useStyles();
  const [boxDisplay, setBoxDisplay] = useState(true);
  const [confiDisplay, setconfiDisplay] = useState(false);
  const [confirm, setConfirm] = useState('');
  const [expandForm, setExpandForm] = useState(true);
  const { isDeleting, error, ModelDelete } = useModelDelete();
  const { modelId } = useParams();
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  useEffect(() => {
    onDelete(expandForm);
  }, [expandForm]);

  return (
    <>
      {boxDisplay === true ? (
        <div className={classes.outerBox}>
          <div className={classes.boxHeading}>
            <Grid item container xs={12}>
              <Grid item xs={2}>
                <div>
                  <Icon icon={trashOutline} width={30} height={30} color={'#B00020'} />
                </div>
              </Grid>
              <Grid item xs={10}>
                Are you sure you want to delete this model ?
              </Grid>
            </Grid>
          </div>
          <div className={classes.boxDiv}>
            <button
              type="button"
              className={classes.confiYesButton}
              onClick={() => {
                setBoxDisplay(false);
                setconfiDisplay(true);
              }}
            >
              YES
            </button>
            <button
              type="button"
              className={classes.confiNoButton}
              onClick={() => {
                setExpandForm(false);
              }}
            >
              NO
            </button>
          </div>
        </div>
      ) : null}
      {confiDisplay === true ? (
        <div className={classes.outerBox}>
          <div className={classes.boxHeading}>
            <Grid item container xs={12}>
              <Grid item xs={2}>
                <div>
                  <Icon icon={trashOutline} width={30} height={30} color={'#B00020'} />
                </div>
              </Grid>
              <Grid item xs={10}>
                <div>Are you sure you want to delete this model ?</div>
                <div>Type “MODEL” here</div>
                <div>
                  <TextField
                    id="outlined-basic"
                    label="Type"
                    variant="outlined"
                    sx={{ height: '60px !important', width: '300px' }}
                    onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
                      setConfirm(e.target.value as string);
                    }}
                  />
                </div>
              </Grid>
            </Grid>
          </div>
          <div className={classes.boxDiv}>
            { confirm.toUpperCase() === "MODEL" && 
              <button
                type="button"
                className={classes.confiDeleteButton}
                onClick={async () => {
                  setExpandForm(false);
                  await ModelDelete(modelId);   
                  if (!isDeleting) {
                    enqueueSnackbar(`Model Deleted`, { variant: 'info' })
                    navigate(PATH_DASHBOARD.general.models);
                  }
                }}
              >
                DELETE
              </button>
            }             
            <button
              type="button"
              className={classes.confiNoButton}
              onClick={() => {
                setconfiDisplay(false);
                setBoxDisplay(true);
              }}
            >
              CANCEL
            </button>
          </div>
        </div>
      ) : null}
    </>
  );
};
