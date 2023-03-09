import Page from "../../../../components/Page";
import LoadingScreen from "../../../../components/LoadingScreen";
import CollapsibleTable from "../../../../components/Tables/collapsible-table-1";
import { MenuItem, Grid, Box, TextField } from "@material-ui/core";
import { experimentalStyled as styled } from "@material-ui/core/styles";
import { DateRangeFilterState } from "../../../../redux/slices/dateRangeFilter";
import { Heading } from "../../../../components/Heading";
import { makeStyles } from "@material-ui/core/styles";
import { colors } from "../../../../theme/colors";

import ChartBar from "../../../../components/charts/ChartBar";
import { useSelector } from "react-redux";
import { useLocation, useParams } from "react-router-dom";
import { useEffect, useMemo, useState } from "react";
import VersionSelect from "../VersionSelect";
import { useMetricsPsi } from "api/models/GetMetricsPsi";
import Scrollbar from "components/Scrollbar";

function useQuery() {
  const { search } = useLocation();

  return useMemo(() => new URLSearchParams(search), [search]);
}

const daeta = {
  feat_breakdown: [
    {
      driftscore: 0.1725,
      name: "Fico_Score",
    },
    {
      driftscore: 0.1725,
      name: "Fico_Score",
    },
    {
      driftscore: 0.1725,
      name: "Fico_Score",
    },
  ],
  data: [84, 77, 53, 76, 54, 71, 73, 71, 68, 70],
  time_buckets: [
    "2022-05-19T10:41:58.617981",
    "2022-05-18T10:41:58.617988",
    "2022-05-17T10:41:58.617989",
    "2022-05-16T10:41:58.617990",
    "2022-05-15T10:41:58.617991",
    "2022-05-14T10:41:58.617992",
    "2022-05-13T10:41:58.617993",
    "2022-05-12T10:41:58.617994",
    "2022-05-11T10:41:58.617995",
    "2022-05-10T10:41:58.617996",
  ],
};
const RootStyle = styled("div")({
  overflowY: "hidden",
  padding: "1.6rem 2.4rem",
  background: colors.white,
});
const useStyles = makeStyles(() => ({
  graph: {
    maxWidth: "100%",
  },
  table: {
    marginTop: "1.6rem",
    maxWidth: "80%",
  },
}));

const ModelDrift = () => {
  const classes = useStyles();
  let query = useQuery();
  const { modelId } = useParams();
  const versionId = query.get("version_id");
  const [given_versionId, setGivenVersionId] = useState(versionId ?? "");
  const handleVersionChange = (version: string) => {
    setGivenVersionId(version);
  };

  const { fromDate, toDate } = useSelector(
    (state: { dateRangeFilter: DateRangeFilterState }) => state.dateRangeFilter
  );
  
  const { data, isLoading, error } = useMetricsPsi({
    model_id: modelId,
    model_version_id: given_versionId,
    start_time: fromDate,
    end_time: toDate
  })
  

  return (
    <Page title="Model Drift | Waterdip">
      <RootStyle>
        {data && Object.keys(data).length > 0 ?
          <>
            <Box display="grid" maxWidth="80%" gridAutoColumns="auto">
          <Box className={classes.graph} gridColumn="1/3" gridRow="2/4">
            <Heading
              heading="Prediction drift over time"
              subtitle="Prediction drift over time"
            />
            <ChartBar
              data={data.data ? data.data : []}
              categories={data.time_buckets ? data.time_buckets.map(
                (bucket: string) => bucket.split("T")[0]
              ): []}
              name={"PSI"}
              options={{
                width: "100%",
                height: 240,
                columnWidth: "50%",
                enableDataLabels: false,
              }}
            />
          </Box>
          <Box gridColumn="3/4" gridRow="2/4" sx={{ mb: 5 }}>
            <VersionSelect
              on_change={handleVersionChange}
              subtitle="Select a version to view drift"
            />
          </Box>
        </Box>
        <Box className={classes.table}>
          <Heading heading="Feature Breakdown" subtitle="Feature breakdown" />
          <CollapsibleTable
            tablehead_name="Feature Class"
            dataValue={data.feat_breakdown ? data.feat_breakdown : []}
          />
        </Box>
          </>
          : (
            <>
              <Box gridColumn="2/3" gridRow="2/4">
                <Scrollbar>
                  <Box sx={{ py: 3, px: 1 }}>
                    <Box sx={{ height: "calc(100vh - 150px)" }}>
                      <LoadingScreen />
                    </Box>
                  </Box>
                </Scrollbar>
              </Box>
            </>
          )
        }
        
      </RootStyle>
    </Page>
  );
};

export default ModelDrift;
