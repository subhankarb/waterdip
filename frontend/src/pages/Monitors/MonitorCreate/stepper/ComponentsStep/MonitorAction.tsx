import { useEffect, useState } from 'react';
import { Box, TextareaAutosize, TextField } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { colors } from '../../../../../theme/colors';
import { useFormikContext } from 'formik';

const useStyles = makeStyles(() => ({
  actionInput: {
    margin: '0 0 1.8rem 0'
  },
  actionInputTitle: {
    fontSize: '.9rem',
    color: colors.text,
    fontWeight: 600,
    marginBottom: '.4rem'
  },
  actionInputContent: {
    display: 'flex',
    flexDirection: 'column'
  },
  label: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '1rem',
    [`& > input`]: {
      marginRight: '1rem'
    },
    [`& > input + div`]: {
      borderRadius: '4px',
      padding: '0.3rem 0.5rem',
      margin: '0 1rem 0 0',
      color: colors.textLight,
      fontSize: '.75rem',
      fontWeight: 400,
      letterSpacing: '0.05rem',
      cursor: 'pointer',
      transition: 'all 0.15s ease-in-out',
      [`&:hover`]: {
        transform: 'scale(1.05)'
      }
    },
    [`& > input:checked + div`]: {
      fontWeight: 500,
      color: colors.black
    },
    [`& input:checked + .low`]: {
      background: colors.low
    },
    [`& input:checked + .medium`]: {
      background: colors.medium
    },
    [`& input:checked + .high`]: {
      background: colors.high
    }
  },
  desc: {
    minWidth: 350,
    maxWidth: 350,
    minHeight: 100,
    fontSize: '.85rem',
    padding: '0.75rem 1.2rem',
    letterSpacing: '0.025rem',
    borderRadius: '4px',
    borderColor: colors.textLight
  },
  txtInp: {
    width: '350px',
    transform: 'scale(1,.8)',
    '& .MuiInputBase-input': {
      transform: 'scale(1,1.2)'
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

const MonitorAction = () => {
  const formikProps = useFormikContext();
  const classes = useStyles();
  const [monitorName, setmonitorName] = useState<string>();

  useEffect(() => {
    formikProps.setFieldValue('monitor_name', monitorName);
  }, [monitorName]);
  return (
    <>
      <Box className={classes.actionInput}>
        <Box className={classes.actionInputTitle}>Severity</Box>
        <Box className={classes.actionInputContent}>
          <label className={classes.label}>
            <input type="radio" name="severity" value="low" id="" />
            <Box className="low">Low</Box>
          </label>
          <label className={classes.label}>
            <input defaultChecked type="radio" name="severity" value="medium" id="" />
            <Box className="medium">Medium</Box>
          </label>
          <label className={classes.label}>
            <input type="radio" name="severity" value="high" id="" />
            <Box className="high">High</Box>
          </label>
        </Box>
      </Box>
      <Box className={classes.actionInput}>
        <Box className={classes.actionInputTitle}>Monitor Name</Box>
        <TextField
          placeholder="Eg: Monitor 1"
          className={classes.txtInp}
          onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
            setmonitorName(e.target.value as string);
          }}
        />
      </Box>
      <Box className={classes.actionInput}>
        <Box className={classes.actionInputTitle}>Description</Box>
        <TextareaAutosize
          aria-label="empty textarea"
          placeholder="Type Here..."
          className={classes.desc}
        />
      </Box>
    </>
  );
};

export default MonitorAction;
