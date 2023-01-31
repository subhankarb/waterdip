import { capitalCase } from 'change-case';
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { Box, Container, Tab, Tabs, Grid } from '@material-ui/core';
import Page from '../../../components/Page';
import { MHidden } from '../../../components/@material-extend';
import ModelOverview from './ModelOverview/ModelOverview';
// import HeaderBreadcrumbs from '../../../components/HeaderBreadcrumbs';
import DateRangeSelect from '../../../components/DateRangeSelect';
import { PATH_PAGE, PATH_DASHBOARD } from '../../../routes/paths';
import ModelPerformance from './ModelPerformance/ModelPerformance';
import ModelDrift from './ModelDrift/ModelDrift';
import ModelDataProfile from './ModelDataProfile/ModelDataProfile';
import { useModelInfo } from '../../../api/models/GetModelInfo';
import HeaderBreadcrumbs from '../../../components/HeaderBreadcrumbs';
import ModelConfiguration from './ModelConfig/ModelConfig';
import ModelMonitors from './ModelMonitors/ModelMonitors';
import ModelAlerts from './ModelAlerts/ModelAlerts';
import { capitalize } from 'lodash';

const MODEL_TABS = [
  {
    value: 'overview',
    // icon: <Icon icon={barChartOutline} width={20} height={20} />,
    component: <ModelOverview />,
    isDisabled: false
  },
  {
    value: 'performance',
    // icon: <Icon icon={baselineDeveloperBoard} width={20} height={20} />,
    component: <ModelPerformance />,
    isDisabled: false
  },
  {
    value: 'drift',
    // icon: <Icon icon={activityOutline} width={20} height={20} />,
    component: <ModelDrift />,
    isDisabled: false
  },
  {
    value: 'dataset',
    // icon: <Icon icon={fileTextOutline} width={20} height={20} />,
    component: <ModelDataProfile />,
    isDisabled: false
  },
  {
    value: 'alerts',
    // icon: <Icon icon={fileTextOutline} width={20} height={20} />,
    component: <ModelAlerts />,
    isDisabled: false
  },
  {
    value: 'monitors',
    // icon: <Icon icon={fileTextOutline} width={20} height={20} />,
    component: <ModelMonitors />,
    isDisabled: false
  },
  {
    value: 'configuration',
    // icon: <Icon icon={fileTextOutline} width={20} height={20} />,
    component: <ModelConfiguration />,
    isDisabled: false
  }
];

interface TabPanelProps {
  children?: React.ReactNode;
  index: any;
  value: any;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box>{children}</Box>}
    </div>
  );
}
function useQuery() {
  const { search } = useLocation();

  return React.useMemo(() => new URLSearchParams(search), [search]);
}
export default function ModelDetails() {
  let query = useQuery();

  const navigate = useNavigate();
  const [currentTab, setCurrentTab] = useState('overview');
  const { modelId, tabName } = useParams();

  const { data } = useModelInfo({ id: modelId });
  const model_name = (data && Object.keys(data).length > 0) ? data.data.model_name : "Model";

  const handleOnChange = (value: string) => {
    setCurrentTab(value);
    navigate(
      `${PATH_DASHBOARD.general.models}/${modelId}/${value}?version_id=${query.get('version_id')}`
    );
  };

  useEffect(() => {
    const isNotFound = MODEL_TABS.filter((tab) => tab.value === tabName).length === 0;
    if (isNotFound || (data && Object.keys(data).length === 0)) navigate(PATH_PAGE.page404);
    setCurrentTab(tabName);
  }, [tabName, navigate, modelId, data]);

  const headerBody = (isDesktop: boolean) => (
    <>
      <Box sx={{ width: '100%', height: '54px', borderBottom: '0.5px solid #90A0B7' }}>
        <Tabs
          value={currentTab}
          scrollButtons="auto"
          variant="scrollable"
          allowScrollButtonsMobile
          onChange={(e, value) => handleOnChange(value)}
          sx={{ height: '54px', width: '100%' }}
          textColor="primary"
          indicatorColor="primary"
        >
          {MODEL_TABS.map((tab) => (
            <Tab
              disableRipple
              key={tab.value}
              label={capitalCase(tab.value)}
              value={tab.value}
              disabled={tab.isDisabled}
              sx={{
                height: '54px',
                fontFamily: 'Poppins',
                fontStyle: 'normal',
                fontWeight: 400,
                fontSize: '14px',
                textAlign: 'center',
                letterSpacing: '0.01em',
                color: '#90A0B7',
                paddingTop: '15px'
              }}
            />
          ))}
        </Tabs>
      </Box>
    </>
  );

  return (
    <Page title="Model Details | Waterdip" style={{ background: '#F5F6F8' }}>
      <Box
        sx={{
          background: '#FFFFFF',
          boxShadow: '0px 4px 5px rgba(0, 0, 0, 0.02)'
        }}
      >
        <HeaderBreadcrumbs
          heading={
            model_name !== undefined ? `${capitalize(model_name)} / ${capitalize(currentTab)}` : ''
          }
          links={[{ name: 'Models', href: `${PATH_DASHBOARD.general.models}` }]}
          action={currentTab !== 'configuration' ? <DateRangeSelect /> : null}
          sx={{ height: '75px' }}
        />
      </Box>
      <Container maxWidth={false} style={{ height: '54px' }}>
        {headerBody(true)}
      </Container>

      <Container maxWidth={false} style={{ marginTop: '30px' }}>
        <Box sx={{ mb: 1 }} />
        {(data && Object.keys(data).length > 0) && 
          MODEL_TABS.map((tab) => (
            <TabPanel value={currentTab} index={tab.value} key={tab.value}>
              {tab.component}
            </TabPanel>
          ))
        }
      </Container>
    </Page>
  );
}
