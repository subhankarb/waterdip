/*
 *  Copyright 2022-present, the Waterdip Labs Pvt. Ltd.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 */

import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { experimentalStyled as styled } from '@material-ui/core/styles';
import DashboardNavbar from './DashboardNavbar';
import DashboardSidebar from './DashboardSidebar';
import { MHidden } from '../../components/@material-extend';

const APP_BAR_MOBILE = 64;
const APP_BAR_DESKTOP = 0;

const RootStyle = styled('div')({
  display: 'flex',
  minHeight: '100%',
  overflow: 'hidden'
});

const MainStyle = styled('div')(({ theme }) => ({
  flexGrow: 1,
  overflow: 'auto',
  minHeight: '100%',
  paddingTop: APP_BAR_MOBILE + 5,
  [theme.breakpoints.up('lg')]: {
    paddingTop: 0,
    paddingLeft: 0,
    paddingRight: 0
  }
}));

export default function DashboardLayout() {
  const [open, setOpen] = useState(false);

  return (
    <RootStyle>
      <MHidden width="lgUp">
        <DashboardNavbar onOpenSidebar={() => setOpen(true)} />
      </MHidden>
      <DashboardSidebar isOpenSidebar={open} onCloseSidebar={() => setOpen(false)} />
      <MainStyle>
        <Outlet />
      </MainStyle>
    </RootStyle>
  );
}
