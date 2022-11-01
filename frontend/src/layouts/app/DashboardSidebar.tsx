import { useEffect } from 'react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import { experimentalStyled as styled } from '@material-ui/core/styles';
import { Box, Drawer, Typography } from '@material-ui/core';
import Logo from '../../components/Logo';
import Scrollbar from '../../components/Scrollbar';
import NavSection from '../../components/NavSection';
import AccountPopover from './AccountPopover';
import { MHidden } from '../../components/@material-extend';
import sidebarConfig from './SidebarConfig';
import NotificationsPopover from './NotificationsPopover';

const DRAWER_WIDTH = 80;

const RootStyle = styled('div')(({ theme }) => ({
  [theme.breakpoints.up('lg')]: {
    flexShrink: 0,
    width: DRAWER_WIDTH
  }
}));

const AccountStyle = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(2, 2.5),
  borderRadius: theme.shape.borderRadiusSm,
  backgroundColor: theme.palette.grey[500_12]
}));

type DashboardSidebarProps = {
  isOpenSidebar: boolean;
  onCloseSidebar: VoidFunction;
};

export default function DashboardSidebar({ isOpenSidebar, onCloseSidebar }: DashboardSidebarProps) {
  const { pathname } = useLocation();

  useEffect(() => {
    if (isOpenSidebar) {
      onCloseSidebar();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathname]);

  const renderContent = (
    <Scrollbar
      sx={{
        height: '100%',
        '& .simplebar-content': { height: '100%', display: 'flex', flexDirection: 'column' }
      }}
    >
      <Box sx={{ px: 2.5, py: 3 }}>
        <Box component={RouterLink} to="/" sx={{ display: 'inline-flex' }}>
          <Logo />
        </Box>
      </Box>
      <NavSection navConfig={sidebarConfig} />
      {/* <Box sx={{ flexGrow: 1 }} /> */}
      {/* <NotificationsPopover /> */}
      {/* <Box sx={{ mb: 2, mx: 2.5 }}>
        <AccountStyle>
          <AccountPopover />
          <Box sx={{ ml: 2 }}>
            <Typography variant="subtitle1" sx={{ color: 'text.primary' }}>
              Carlota Montario
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.primary' }}>
              Admin
            </Typography>
          </Box>
        </AccountStyle>
      </Box> */}
    </Scrollbar>
  );

  return (
    <RootStyle>
      <MHidden width="lgUp">
        <Drawer
          open={isOpenSidebar}
          onClose={onCloseSidebar}
          PaperProps={{
            sx: { width: DRAWER_WIDTH }
          }}
        >
          {renderContent}
        </Drawer>
      </MHidden>

      <MHidden width="lgDown">
        <Drawer
          open
          variant="persistent"
          PaperProps={{
            sx: { width: DRAWER_WIDTH, bgcolor: '#111D4A' }
          }}
        >
          {renderContent}
        </Drawer>
      </MHidden>
    </RootStyle>
  );
}