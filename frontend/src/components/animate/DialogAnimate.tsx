import { motion, AnimatePresence } from 'framer-motion';
// material
import { Dialog, Box, Paper, DialogProps } from '@material-ui/core';
//
import { varFadeInUp } from './variants';

// ----------------------------------------------------------------------

interface DialogAnimateProps extends DialogProps {
  animate?: object;
  onClose?: VoidFunction;
  maxWidth?: any;
}

export default function DialogAnimate({
  open = false,
  animate,
  onClose,
  maxWidth,
  children,
  ...other
}: DialogAnimateProps) {
  return (
    <AnimatePresence>
      {open && (
        <Dialog
          fullWidth
          maxWidth={maxWidth ? maxWidth : 'xs'}
          open={open}
          onClose={onClose}
          PaperComponent={(props) => (
            <Box
              component={motion.div}
              {...(animate || varFadeInUp)}
              sx={{
                width: '100%',
                height: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <Box onClick={onClose} sx={{ width: '100%', height: '100%', position: 'fixed' }} />
              <Paper {...props} sx={{ borderRadius: '0px !important' }}>
                {props.children}
              </Paper>
            </Box>
          )}
          {...other}
        >
          {children}
        </Dialog>
      )}
    </AnimatePresence>
  );
}
