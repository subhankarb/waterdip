import React, { useState, useEffect } from 'react';
import { MenuItem, Grid, Box, TextField } from '@material-ui/core';
import { experimentalStyled as styled } from '@material-ui/core/styles';
import Page from '../../../../components/Page';
import LoadingScreen from '../../../../components/LoadingScreen';
import Scrollbar from '../../../../components/Scrollbar';
import CollapsibleTable from '../../../../components/Tables/collapsible-table-1';
import TabsPerformance from './PerformanceTabs';
import { Heading } from '../../../../components/Heading';
import BaseLine from './BaseLine';
import { useParams , useLocation  } from 'react-router-dom';
import { useSelector } from '../../../../redux/store';
import { DateRangeFilterState } from '../../../../redux/slices/dateRangeFilter';
import { useModelPerformance } from '../../../../api/models/GetModelPerformance';
import PerformanceChart from './PerformanceChart';

const RootStyle = styled('div')({
  overflowY: 'hidden',
  padding: '1.6rem 2.4rem',
  background: '#fff'
});

function useQuery() {
  const { search } = useLocation();

  return React.useMemo(() => new URLSearchParams(search), [search]);
}

const ModelPerformance = () => {
  let query = useQuery();
  const versionId = query.get('version_id')
  const { fromDate, toDate } = useSelector(
    (state: { dateRangeFilter: DateRangeFilterState }) => state.dateRangeFilter
  );
  const { data, isLoading } = useModelPerformance({
    id: versionId != null ? versionId : '',
    start_date: fromDate,
    end_date: toDate
  });

  const [currentTab, setCurrentTab] = useState<string>('accuracy');
  const handleCurrentTab = (data: string) => {
    setCurrentTab(data);
  };
  return (
    <Page title="Model Performance | Waterdip">
      <RootStyle>
        <Box
          display="grid"
          gridTemplateRows="auto auto auto auto auto"
          gridTemplateColumns="150px auto 270px"
        >
          <Box gridColumn="1/-1" gridRow="1/2">
            <Heading heading="Performance over Time" subtitle="Performance" />
          </Box>
          <Box gridColumn="1/2" gridRow="2/-1">
            <TabsPerformance currentTab={currentTab} onChange={handleCurrentTab} />
          </Box>
          {data ? (
            <>
              <Box gridColumn="2/3" gridRow="2/4">
                <Scrollbar>
                  <Box sx={{ px: 3, py: 2 }}>
                    <PerformanceChart dataValue={data.data[currentTab]} tabValue={currentTab} />
                  </Box>
                </Scrollbar>
              </Box>
              <Box gridColumn="3/4" gridRow="2/3" sx={{ ml: 2 }}>
                <BaseLine />
              </Box>
            </>
          ) : (
            <>
              <Box gridColumn="2/3" gridRow="2/4">
                <Scrollbar>
                  <Box sx={{ py: 3, px: 1 }}>
                    <Box sx={{ height: 'calc(100vh - 150px)' }}>
                      <LoadingScreen />
                    </Box>
                  </Box>
                </Scrollbar>
              </Box>
            </>
          )}
        </Box>
      </RootStyle>
    </Page>
  );
};

export default ModelPerformance;
