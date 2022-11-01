import { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import DateRangeSelect from './DateRangeSelect';
import { formatDateTime } from '../../../../utils/date';
import trashOutline from '@iconify/icons-eva/trash-outline';
import { Icon } from '@iconify/react';
import TextField from '@material-ui/core/TextField';
import { Grid } from '@material-ui/core';

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
  }
}));

type Props = {
  onSave: Function;
  onSelect: Function;
};

export const DialogBoxPart = ({ onSave, onSelect }: Props) => {
  const now = new Date();
  const classes = useStyles();
  const [boxDisplay, setBoxDisplay] = useState(true);
  const [selectDate, setSelectDate] = useState(false);
  const [confiDisplay, setconfiDisplay] = useState(false);
  const [dataDisplay, setDataDisplay] = useState(false);
  const [dateRange, setDateRange] = useState([new Date(now.getTime() - 5 * 60 * 60 * 1000), now]);
  const [expandForm, setExpandForm] = useState(true);

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
              setSelectDate(true);
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
            Datasets
          </button>
        </div>
      ) : null}
      {selectDate === true ? (
        <div className={classes.outerBox}>
          <div className={classes.boxHeading}>
            select date range{' '}
            <button
              type="button"
              onClick={() => {
                setSelectDate(false);
                setBoxDisplay(true);
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
              onClick={() => {
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
            Select Dataset from below list{' '}
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
  const [expandForm, setExpandForm] = useState(true);

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
                  />
                </div>
              </Grid>
            </Grid>
          </div>
          <div className={classes.boxDiv}>
            <button
              type="button"
              className={classes.confiDeleteButton}
              onClick={() => {
                setExpandForm(false);
              }}
            >
              DELETE
            </button>
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
