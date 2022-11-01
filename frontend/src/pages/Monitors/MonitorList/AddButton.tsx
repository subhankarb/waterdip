import { useState } from 'react';
import { DialogAnimate } from '../../../components/animate';
import { Box, Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { Grid } from '@material-ui/core';
import { colors } from '../../../theme/colors';
import MonitorAddDialog from './MonitorAddDialog';

const useStyles = makeStyles(() => ({
  button_add: {
    fontSize: '0.75rem',
    fontWeight: 600,
    letterSpacing: '0.01em',
    color: colors.white,
    background: colors.textPrimary,
    boxShadow: '0px 4px 10px rgba(103, 128, 220, 0.24)',
    borderRadius: '4px',
    height: '40px',
    padding: '0rem 2.4rem'
  }
}));

const DialogBox = () => {
  const classes = useStyles();
  const [boxDisplay, setBoxDisplay] = useState(true);

  return (
    <>
      {boxDisplay === true ? (
        <>
          <MonitorAddDialog />
        </>
      ) : null}
    </>
  );
};

const AddButton = () => {
  const classes = useStyles();
  const [expandForm, setExpandForm] = useState(false);
  return (
    <Box>
      <Button
        className={classes.button_add}
        variant="contained"
        onClick={() => setExpandForm((state) => !state)}
      >
        Create Monitor
      </Button>
      <DialogAnimate maxWidth="sm" open={expandForm} onClose={() => setExpandForm(false)}>
        <DialogBox />
      </DialogAnimate>
    </Box>
  );
};

export default AddButton;
