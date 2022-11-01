import { useState } from 'react';
import { Icon } from '@iconify/react';
import { NavLink as RouterLink, matchPath, useLocation } from 'react-router-dom';
import arrowIosForwardFill from '@iconify/icons-eva/arrow-ios-forward-fill';
import arrowIosDownwardFill from '@iconify/icons-eva/arrow-ios-downward-fill';
import { alpha, useTheme, experimentalStyled as styled } from '@material-ui/core/styles';
import { Box, List, ListItem, Collapse, ListItemText, ListItemIcon } from '@material-ui/core';
import typography from '../theme/typography';

export type NavItemProps = {
  title: string;
  path: string;
  icon?: JSX.Element;
  info?: JSX.Element;
  children?: {
    title: string;
    path: string;
  }[];
};

const ListItemStyle = styled(ListItem)(({ theme }) => ({
  ...typography.body2,
  height: 48,
  position: 'relative',
  textTransform: 'capitalize',
  paddingLeft: theme.spacing(4),
  paddingRight: theme.spacing(2.5),
  color: theme.palette.text.secondary,
  '&:before': {
    top: 0,
    right: 0,
    width: 5,
    bottom: 0,
    content: "''",
    display: 'none',
    position: 'absolute',
    // borderTopLeftRadius: 4,
    // borderBottomLeftRadius: 4,
    backgroundColor: '#ffffff',
    marginRight: 4
  }
}));

const ListItemIconStyle = styled(ListItemIcon)({
  width: 22,
  height: 22,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center'
});

function NavItem({ item }: { item: NavItemProps }) {
  const theme = useTheme();
  const { pathname } = useLocation();
  const { title, path, icon, info, children } = item;
  const isActiveRoot = path ? !!matchPath({ path, end: false }, pathname) : false;
  const [open, setOpen] = useState(isActiveRoot);

  const handleOpen = () => {
    setOpen(!open);
  };

  const activeRootStyle = {
    color: '#ffffff',
    fontWeight: 'fontWeightMedium',
    bgcolor: '#111D4A',
    '&:before': { display: 'block' }
  };

  const activeSubStyle = {
    color: '#ffffff',
    fontWeight: 'fontWeightMedium'
  };

  if (children) {
    return (
      <>
        <ListItemStyle
          button
          disableGutters
          onClick={handleOpen}
          sx={{
            ...(isActiveRoot && activeRootStyle)
          }}
        >
          {icon && <ListItemIconStyle>{icon}</ListItemIconStyle>}
          <ListItemText disableTypography primary={title} />
          {info && info}
          <Box
            component={Icon}
            icon={open ? arrowIosDownwardFill : arrowIosForwardFill}
            sx={{ width: 16, height: 16, ml: 1 }}
          />
        </ListItemStyle>

        <Collapse in={open} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            {children.map((item) => {
              const { title, path } = item;
              const isActiveSub = path ? !!matchPath({ path, end: false }, pathname) : false;

              return (
                <ListItemStyle
                  button
                  disableGutters
                  key={title}
                  // @ts-ignore
                  component={RouterLink}
                  to={path}
                  sx={{
                    ...(isActiveSub && activeSubStyle)
                  }}
                >
                  <ListItemIconStyle>
                    <Box
                      component="span"
                      sx={{
                        width: 4,
                        height: 4,
                        display: 'flex',
                        borderRadius: '50%',
                        alignItems: 'center',
                        justifyContent: 'center',
                        bgcolor: 'text.disabled',
                        transition: (theme) => theme.transitions.create('transform'),
                        ...(isActiveSub && {
                          transform: 'scale(2)',
                          bgcolor: '#ffffff'
                        })
                      }}
                    />
                  </ListItemIconStyle>
                  <ListItemText disableTypography primary={title} />
                </ListItemStyle>
              );
            })}
          </List>
        </Collapse>
      </>
    );
  }

  return (
    <ListItemStyle
      button
      disableGutters
      // @ts-ignore
      component={RouterLink}
      to={path}
      sx={{
        ...(isActiveRoot && activeRootStyle)
      }}
    >
      {icon && <ListItemIconStyle>{icon}</ListItemIconStyle>}
      {/* <ListItemText disableTypography primary={item.title} /> */}
      {info && info}
    </ListItemStyle>
  );
}

export default NavItem;
