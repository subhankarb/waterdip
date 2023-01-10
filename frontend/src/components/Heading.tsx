import { makeStyles } from '@material-ui/core/styles';
import { Button, Tooltip } from '@material-ui/core';
import { Icon } from '@iconify/react';
import infoOutline from '@iconify/icons-eva/info-outline';
import { MIconButton } from './@material-extend';

const useStyles = makeStyles({
  heading: {
    fontSize: '.9rem',
    fontWeight: 600,
    display: 'flex',
    alignItems: 'center',
    letterSpacing: '.25px',
    paddingBottom: '.6rem'
  },
  cardheading: {
    fontSize: '.9rem',
    fontWeight: 500,
    display: 'flex',
    alignItems: 'center',
    letterSpacing: '.25px',
    paddingBottom: '.25rem',
    textTransform: 'uppercase'
  },
  info: {}
});

type headingProps = {
  heading: string;
  subtitle?: string;
};

export function Heading({ heading, subtitle }: headingProps) {
  const classes = useStyles();
  return (
    <div className={classes.heading}>
      {heading}
      {subtitle && (
        <Tooltip title={subtitle} placement="right">
          <MIconButton
            color="inherit"
            sx={{
              p: 0,
              width: 21,
              height: 21,
              marginLeft: '.5rem'
            }}
          >
            <Icon icon={infoOutline} width={20} height={20} />
          </MIconButton>
        </Tooltip>
      )}
    </div>
  );
}
export function CardHeading({ heading, subtitle }: headingProps) {
  const classes = useStyles();

  return (
    <div className={classes.cardheading}>
      {heading}
      {subtitle && (
        <Tooltip title={subtitle} placement="right">
          <MIconButton
            color="inherit"
            sx={{
              p: 0,
              width: 18,
              height: 18,
              marginLeft: '.5rem'
            }}
          >
            <Icon icon={infoOutline} width={18} height={18} />
          </MIconButton>
        </Tooltip>
      )}
    </div>
  );
}
