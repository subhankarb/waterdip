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

// routes
import { PATH_DASHBOARD } from '../../routes/paths';
// components
import SvgIconStyle from '../../components/SvgIconStyle';

// ----------------------------------------------------------------------

const getIcon = (name: string) => (
  <SvgIconStyle src={`/static/icons/navbar/${name}.svg`} sx={{ width: '100%', height: '100%' }} />
);

const ICONS = {
  grid: getIcon('grid'),
  layers: getIcon('layers'),
  alert_octagon: getIcon('alert-octagon')
};

const sidebarConfig = [
  // GENERAL
  // ----------------------------------------------------------------------
  {
    subheader: '',
    items: [
      { title: 'Grid', path: PATH_DASHBOARD.general.models, icon: ICONS.grid },
      { title: 'Layers', path: PATH_DASHBOARD.general.monitors, icon: ICONS.layers },
      { title: 'Alert Octagon', path: PATH_DASHBOARD.general.alerts, icon: ICONS.alert_octagon }
    ]
  }

  // MANAGEMENT
  // ----------------------------------------------------------------------
];

export default sidebarConfig;
