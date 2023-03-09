import { Heading } from "../../../components/Heading";
import { makeStyles } from "@material-ui/styles";
import { MenuItem } from "@material-ui/core";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { colors } from "../../../theme/colors";
import { useEffect, useMemo, useState } from "react";
import { Select } from "@material-ui/core";
import { useModelInfo } from "api/models/GetModelInfo";

const useStyles = makeStyles({
  select: {
    marginTop: ".75rem",
    marginBottom: ".75rem",
    backgroundColor: `${colors.white} !important`,
    fontFamily: "Poppins",
    maxWidth: "80%",
    minWidth: "80%",
    transform: "scale(1,.8)",
    "& .MuiInputBase-input": {
      transform: "scale(1,1.2)",
    },
    [`& fieldset`]: {
      borderRadius: 2,
      borderColor: `${colors.textLight} !important`,
    },
    [`&.Mui-focused fieldset`]: {
      borderRadius: 4,
      borderColor: `${colors.text} !important`,
    },
  },
  baseLine: {
    paddingLeft: ".8rem",
  },
  baseLineContent: {
    marginTop: ".6rem",
    width: "100%",
    maxWidth: "250px",
    color: colors.text,
    background: colors.boxBackground,
    borderRadius: "4px",
    padding: "1rem",
  },
  contentHeading: {
    fontSize: ".85rem",
    fontWeight: 600,
    letterSpacing: ".25px",
    marginBottom: ".5rem",
  },
  contentText: {
    fontSize: ".8rem",
    fontWeight: 500,
    letterSpacing: ".25px",
    padding: ".7rem 0 .5rem",
  },
});

function useQuery() {
  const { search } = useLocation();

  return useMemo(() => new URLSearchParams(search), [search]);
}

export default function VersionSelect({ on_change, subtitle }: any) {
  const navigate = useNavigate();
  const { modelId, tabName } = useParams();
  const classes = useStyles();
  const query = useQuery();

  const [selected, setSelected] = useState(query.get("version_id"));
  useEffect(() => {
    on_change(selected);
  }, [selected]);
  const modelOverview = useModelInfo({
    id: modelId,
  });
  const handleChange = (event: any) => {
    setSelected(event.target.value);
  };
  return (
    <div className={classes.baseLine}>
      <Heading
        heading="Model Version"
        subtitle={subtitle}
      />
      <div className={classes.baseLineContent}>
        <div className={classes.contentHeading}>Select Version</div>
        <hr />
        <Select
          defaultValue="select"
          className={classes.select}
          onChange={handleChange}
          value={selected}
        >
          <MenuItem value="select" disabled className="selectDisable">
            Version
          </MenuItem>
          {modelOverview &&
            modelOverview?.data?.data?.model_versions?.map((row: any) => (
              <MenuItem value={row.model_version_id} key={row}>
                {row.model_version}
              </MenuItem>
            ))}
        </Select>
      </div>
    </div>
  );
}
