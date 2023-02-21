import { useEffect, useState } from 'react';
import { Heading } from '../../../../components/Heading';
import { makeStyles } from '@material-ui/styles';
import { formatDateTime } from '../../../../utils/date';
import { Box, TextField, MenuItem, Button } from '@material-ui/core';
import { DialogAnimate } from '../../../../components/animate';
import { DialogBoxPart, DeleteDialogBox } from './dialogBox';
import { colors } from '../../../../theme/colors';
import { useModelUpdate } from 'api/models/UpdateModel';
import { useSnackbar } from 'notistack';
import { useParams } from 'react-router-dom';

const useStyles = makeStyles({
  card: {
    maxWidth: '360px',
    marginBottom: '3rem'
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
  },
  delete: {
    borderRadius: '4px',
    marginTop: '1rem',
    paddingLeft: '1.5rem',
    paddingRight: '1.5rem',
    borderColor: colors.error,
    color: colors.error,
    letterSpacing: '.1rem'
  }
});

type Props = {
  path: boolean;
  data: any;
};

const stringToMilliseconds = (str: string) => {
  const [value, unit] = str.split('d');
  const millisecondsInADay = 24 * 60 * 60 * 1000;
  return parseInt(value) * millisecondsInADay;
};

export const ConfigBaseLine = ({ path, data }: Props) => {
  const now = new Date();
  const [dateRange, setDateRange] = useState([new Date(now.getTime() - 5 * 60 * 60 * 1000), now]);
  const [dateTimeString, setDateTimeString] = useState(`${formatDateTime(dateRange[0] ? dateRange[0] : now)} to ${formatDateTime(
    dateRange[1] ? dateRange[1] : now
  )} `)
  const classes = useStyles();
  const [expandForm, setExpandForm] = useState(path);
  
  useEffect(() => {
    if (data && data.data && data.data.data && data.data.data.model_baseline?.time_window?.time_window_type) {
      const timer = data.data.data && data.data.data.model_baseline?.time_window;
      const window_type = data.data.data.model_baseline?.time_window?.time_window_type
      if (window_type === "MOVING_TIME_WINDOW") {
        const milliseconds = stringToMilliseconds(timer.moving_time_window.time_period)
        setDateRange([new Date(now.getTime() - milliseconds), now]);
      }
      else if (window_type === "FIXED_TIME_WINDOW") {
        setDateRange([new Date(timer.fixed_time_window.start_time), new Date(timer.fixed_time_window.end_time)]);
      }
      
    }
  }, [data]);

  useEffect(() => {
    setDateTimeString(`${formatDateTime(dateRange[0] ? dateRange[0] : now)} to ${formatDateTime(
      dateRange[1] ? dateRange[1] : now
    )}`)
  },[dateRange])


  const handleSave = (data: any) => {
    setExpandForm(data);
  };
  const handleSelect = (data: any) => {
    setDateRange(data);
  };

  return (
    <Box className={classes.card}>
      <Heading heading="BaseLine" subtitle="baseline" />
      <Box className={classes.baseLineContent}>
        <Box className={classes.contentHeading}>Production</Box>
        <hr />
        <Box className={classes.contentText}>Date from {dateTimeString}</Box>
        <Button className={classes.contentButton} onClick={() => setExpandForm((state) => !state)}>
          Configure baseline {'>'}
        </Button>
        <DialogAnimate open={expandForm} onClose={() => setExpandForm(false)}>
          <DialogBoxPart onSelect={handleSelect} onSave={handleSave} stringToMilliseconds={stringToMilliseconds}/>
        </DialogAnimate>
      </Box>
    </Box>
  );
};


export const ConfigEvaluation = ({data}: any) => {
  const res = data?.data?.data;
  const classes = useStyles();
  const [posClass, setPosClass] = useState<string>('');
  const { isUpdating, error, ModelUpdate } = useModelUpdate();
  const { modelId } = useParams();
  const { enqueueSnackbar } = useSnackbar();
  interface classList{
    classN : string;
  }
  
  return (
    <Box className={classes.card}>
      <Heading heading="Setup Positive Class" />
      <Box className={classes.baseLineContent}>
        <TextField
          select
          fullWidth
          label="Select positive class"
          value={posClass}
          onChange={(e) => setPosClass(e.target.value)}
          sx={{ mt: 2, mb: 2.5 }}
          placeholder="Choose the evaluation"
        >
          {res.model_prediction_classes && res.model_prediction_classes.map((row_class: any)=> (
                <MenuItem value={row_class}>{row_class}</MenuItem>
          ))}
        </TextField>
        <Box className={classes.btnContainer}>
          <Button variant="contained" className={classes.btn}
            onClick={async () => {
              if (posClass !== "") {
                await ModelUpdate({
                  model_id: modelId,
                  property_name: "positive_class",
                  positive_class: {
                    name: posClass
                  }
                })
                if (error) {
                  enqueueSnackbar(`Something went wrong!`, { variant: 'error' });
                }
                else if (!isUpdating) {
                  enqueueSnackbar(`Updated Successfully`, { variant: 'success' });
                }
              } else {
                enqueueSnackbar(`No Class Selected`, { variant: 'info' })
              }
            }}
          >
            Save
          </Button>
        </Box>
      </Box>
    </Box>
  );
};

export const ConfigAdvanced = () => {
  const classes = useStyles();
  const [expandForm, setExpandForm] = useState(false);
  const handleDelete = (data: any) => {
    setExpandForm(data);
  };
  return (
    <Box className={classes.card}>
      <Heading heading="Advanced Configuration" />
      <Button
        className={classes.delete}
        variant="outlined"
        onClick={() => setExpandForm((state) => !state)}
      >
        Delete Model
      </Button>
      <DialogAnimate open={expandForm} onClose={() => setExpandForm(false)}>
        <DeleteDialogBox onDelete={handleDelete} />
      </DialogAnimate>
    </Box>
  );
};
