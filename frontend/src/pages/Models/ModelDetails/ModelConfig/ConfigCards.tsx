import { useState } from 'react';
import { Heading } from '../../../../components/Heading';
import { makeStyles } from '@material-ui/styles';
import { formatDateTime } from '../../../../utils/date';
import { Box, TextField, MenuItem, Button } from '@material-ui/core';
import { DialogAnimate } from '../../../../components/animate';
import { DialogBoxPart, DeleteDialogBox } from './dialogBox';
import { colors } from '../../../../theme/colors';

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
};

export const ConfigBaseLine = ({ path }: Props) => {
  const now = new Date();
  const [dateRange, setDateRange] = useState([new Date(now.getTime() - 5 * 60 * 60 * 1000), now]);
  const classes = useStyles();
  const [expandForm, setExpandForm] = useState(path);

  const dateTimeString = `${formatDateTime(dateRange[0] ? dateRange[0] : now)} to ${formatDateTime(
    dateRange[1] ? dateRange[1] : now
  )} `;

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
          <DialogBoxPart onSelect={handleSelect} onSave={handleSave} />
        </DialogAnimate>
      </Box>
    </Box>
  );
};

export const ConfigEvaluation = () => {
  const classes = useStyles();
  const [data, setData] = useState<string>('0');

  return (
    <Box className={classes.card}>
      <Heading heading="Evaluation window" />
      <Box className={classes.baseLineContent}>
        <TextField
          select
          fullWidth
          label="Select evaluation window"
          value={data}
          onChange={(e) => setData(e.target.value)}
          sx={{ mt: 2, mb: 2.5 }}
          placeholder="Choose the evaluation"
        >
          <MenuItem value="0">72 Hrs</MenuItem>
          <MenuItem value="1">1 week</MenuItem>
          <MenuItem value="2">1 month</MenuItem>
        </TextField>
        <Box className={classes.btnContainer}>
          <Button variant="contained" className={classes.btn}>
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
