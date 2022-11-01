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
