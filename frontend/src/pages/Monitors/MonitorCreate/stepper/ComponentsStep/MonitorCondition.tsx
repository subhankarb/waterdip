import { useEffect, useState } from 'react';
import { Box, Select, MenuItem, TextField, Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { colors } from '../../../../../theme/colors';
import { DialogAnimate } from '../../../../../components/animate';
import { useFormikContext } from 'formik';
import { fontSize } from '@material-ui/system';

const useStyles = makeStyles(() => ({
  form: {
    // display: 'flex'
  },
  contentInput: {
    display: 'flex',
    flexDirection: 'column',
    margin: '0 0 1rem 0'
  },
  performData: {
    marginTop: '.3rem',
    display: 'flex',
    alignItems: 'center'
  },
  contentInputLabel: {
    fontSize: '.9rem',
    color: colors.text,
    fontWeight: 600,
    marginBottom: '.4rem'
  },
  contentInputDesc: {
    fontSize: '.7rem',
    color: colors.textLight,
    fontWeight: 400,
    marginBottom: '.65rem'
  },
  contentInputSubDesc: {
    fontSize: '.75rem',
    color: colors.text,
    fontWeight: 600
  },
  select: {
    transform: 'scale(1,.6)',
    maxWidth: '20rem',
    '& .MuiInputBase-input': {
      transform: 'scale(1,1.4)',
      fontSize: '.8rem'
    },
    [`& fieldset`]: {
      borderRadius: 4,
      borderColor: `${colors.textLight} !important`
    },
    [`&.Mui-focused fieldset`]: {
      borderRadius: 4,
      borderColor: `${colors.text} !important`
    },
    option: {
      transform: 'scale(1,.75)',
      fontSize: '.8rem'
    }
  },
  numberInput: {
    transform: 'scale(1,.6)',
    width: '5rem',
    '& .MuiInputBase-input': {
      transform: 'scale(1,1.4)',
      fontSize: '.8rem'
    },
    '& .MuiOutlinedInput-root': {
      '& fieldset': {
        borderRadius: '4px',
        borderColor: colors.textLight
      },
      '&.Mui-focused fieldset': {
        borderColor: colors.text
      }
    }
  }
}));

const MonitorCondition = () => {
  const classes = useStyles();
  const [expandForm, setExpandForm] = useState(false);
  const formikProps = useFormikContext();
  const { values }: any = formikProps;
  const [dimension, setDimension] = useState<string[]>([]);
  const [evaluationWindow, setevaluationWindow] = useState('');
  const [greater, setGreater] = useState<number>();
  const [less, setLess] = useState<number>();

  useEffect(() => {
    formikProps.setFieldValue('monitor_condition.dimensions.features', dimension);
    formikProps.setFieldValue('monitor_condition.evaluation_window', evaluationWindow);
    formikProps.setFieldValue('monitor_condition.threshold.gt', greater);
    formikProps.setFieldValue('monitor_condition.threshold.lt', less);
  }, [dimension, evaluationWindow, greater, less]);
  return (
    <Box className={classes.form}>
      <Box className={classes.contentInput}>
        <label className={classes.contentInputLabel}>Dimension</label>
        <label className={classes.contentInputDesc}>
          Dimension is a column of a dataset which can represent feature or prediction value
        </label>
        <label className={classes.contentInputSubDesc}>Select one or multiple feature</label>
        <Select
          defaultValue={'dimension_1'}
          className={classes.select}
          onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
            setDimension((dimension) => [...dimension, e.target.value as string]);
          }}
        >
          <MenuItem value="dimension_1">Dimension 1</MenuItem>
          <MenuItem value="dimension_2">Dimension 2</MenuItem>
          <MenuItem value="dimension_3">Dimension 3</MenuItem>
        </Select>
      </Box>
      {values.monitor_type !== 'Missing Value' && (
        <Box className={classes.contentInput}>
          <label className={classes.contentInputLabel}>Evaluation Metric</label>
          <label className={classes.contentInputDesc}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </label>
          <label className={classes.contentInputSubDesc}>
            Select evaluation metric from the list
          </label>
          <Select defaultValue={'psi'} className={classes.select}>
            <MenuItem value="psi">PSI</MenuItem>
          </Select>
        </Box>
      )}
      <Box className={classes.contentInput}>
        <label className={classes.contentInputLabel}>Evaluation Window</label>
        <label className={classes.contentInputDesc}>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        </label>
        <label className={classes.contentInputSubDesc}>Select evaluation window</label>
        <Select
          defaultValue={'1 day'}
          className={classes.select}
          onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
            setevaluationWindow(e.target.value as string);
          }}
        >
          <MenuItem value="1 day">24 Hrs</MenuItem>
          <MenuItem value="1 week">1 Week</MenuItem>
          <MenuItem value="1 month">1 Month</MenuItem>
        </Select>
      </Box>
      <Box className={classes.contentInput}>
        <label className={classes.contentInputLabel}>Performance Threshold</label>
        <label className={classes.contentInputDesc}>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        </label>
        <label className={classes.contentInputSubDesc}>
          Incident will triggered when threshold is
        </label>
        <div className={classes.performData}>
          <label className={classes.contentInputSubDesc}>Greater than &nbsp;&nbsp;&nbsp;</label>
          <TextField
            placeholder="Eg: 0.2"
            className={classes.numberInput}
            type="number"
            onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
              setGreater(e.target.value as number);
            }}
          ></TextField>
          &nbsp;&nbsp;&nbsp;
          <label className={classes.contentInputSubDesc}>or Less than&nbsp;&nbsp;&nbsp;</label>
          <TextField
            placeholder="Eg: 0.8"
            className={classes.numberInput}
            type="number"
            onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
              setLess(e.target.value as number);
            }}
          ></TextField>
        </div>
      </Box>
    </Box>
  );
};

export default MonitorCondition;

// <Box className={classes.contentInput}>
//   <label className={classes.contentInputLabel}>BaseLine</label>
//   <Button className={classes.contentButton} onClick={() => setExpandForm((state) => !state)}>
//     Configure baseline {'>'}
//   </Button>
//   <DialogAnimate open={expandForm} onClose={() => setExpandForm(false)}></DialogAnimate>
// </Box>;
