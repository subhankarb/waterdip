import { makeStyles } from '@material-ui/core/styles';
import { Box, Button, Tab, TextField, Tabs, Select, MenuItem } from '@material-ui/core';
import { Icon } from '@iconify/react';
import { useState } from 'react';

import { PATH_PAGE, PATH_DASHBOARD } from '../../../routes/paths';
import { useNavigate, useParams } from 'react-router-dom';

import { colors } from '../../../theme/colors';
import { useSelector } from '../../../redux/store';
import { ModelMonitorState } from '../../../redux/slices/ModelMonitorState';
import { usePaginatedModels } from '../../../api/models/GetModels';
import { ModelListRow } from '../../../@types/model';

const useStyles = makeStyles(() => ({
  dialogBoxMonitorType: { padding: '2.1rem 1.8rem' },
  modelContainer: {
    marginBottom: '1.5rem'
  },
  select: {
    marginTop: '.75rem',
    minWidth: '20rem',
    transform: 'scale(1,.8)',
    '& .MuiInputBase-input': {
      transform: 'scale(1,1.2)'
    },
    [`& fieldset`]: {
      borderRadius: 4,
      borderColor: `${colors.textLight} !important`
    },
    [`&.Mui-focused fieldset`]: {
      borderRadius: 4,
      borderColor: `${colors.text} !important`
    }
  },
  selectDiv: {
    marginTop: '.75rem',
    minWidth: '20rem',
    fontSize: '0.8rem',
    letterSpacing: '0.05rem',
    color: colors.textLight
    // border: `1px solid ${colors.textLight}`
  },
  tabContainer: {
    marginBottom: '1rem'
  },
  conatinerHeading: {
    fontSize: '.9rem',
    color: colors.text,
    fontWeight: 500
  },
  TabItems: {
    marginTop: '1.1rem',
    '& .css-1pvp4f6-MuiButtonBase-root-MuiTab-root:not(:last-child)': {
      marginRight: '0 !important'
    },
    '& .css-1c79mml-MuiTabs-indicator': {
      display: 'none'
    },
    '& .css-1pvp4f6-MuiButtonBase-root-MuiTab-root.Mui-selected': {
      background: '#d1d9f5',
      color: colors.textPrimary,
      fontWeight: 500
    }
  },
  TabItem: {
    borderBottom: `1px solid ${colors.textLight}`,
    borderRadius: '4px 4px 0 0 !important',
    fontWeight: 400,
    fontSize: '0.8rem',
    letterSpacing: '0.05rem',
    color: colors.textLight,
    padding: '0.36rem 1.2rem',
    minHeight: '27px'
  },
  tabItemContent: {
    padding: '0rem 2.4rem 0 1.2rem'
  },
  itemContentChild: {
    borderRadius: '4px',
    cursor: 'pointer',
    padding: '0.5rem 0 1rem 0rem',
    '&:hover .titlehover': {
      color: colors.textPrimary
    },
    '&:hover .hoverdesc': {
      color: colors.textPrimary
    },
    '&:hover::marker': {
      color: colors.textPrimary
    },
    '&::marker': {
      color: colors.textLight,
      fontSize: '0.8rem'
    }
  },
  itemContentChildDisabled: {
    padding: '0.5rem 0 1rem 0rem',
    borderRadius: '4px',
    cursor: 'not-allowed',
    '&::marker': {
      color: colors.textLight,
      fontSize: '0.8rem'
    }
  },
  itemHeading: {
    fontSize: '0.8rem',
    fontWeight: 500,
    color: colors.text,
    marginBottom: '0.25rem'
  },
  itemHeadingDisabled: {
    fontSize: '0.8rem',
    fontWeight: 500,
    color: colors.textLight,
    marginBottom: '0.25rem'
  },
  itemDesc: {
    fontSize: '0.7rem',
    fontWeight: 400,
    color: colors.textLight
  }
}));

type Props = {
  data: any[];
};

type TabItemProps = {
  title: string;
  desc: string;
  disabled: boolean;
};

const TabContent = ({ data }: Props) => {
  const classes = useStyles();
  const navigate = useNavigate();
  return (
    <Box className={classes.tabItemContent}>
      <ul>
        {data.map((item: any) => {
          const disabled = item.disabled;
          return (
            <>
              <li
                className={`${
                  disabled === false
                    ? `${classes.itemContentChild}`
                    : `${classes.itemContentChildDisabled}`
                }`}
                onClick={() => {
                  if (disabled === false)
                    navigate(`${PATH_DASHBOARD.general.monitorCreate}`, {
                      state: { value: item.title }
                    });
                }}
              >
                <Box
                  className={`${
                    disabled === false ? `${classes.itemHeading}` : `${classes.itemHeadingDisabled}`
                  } titlehover`}
                >
                  {item.title}
                </Box>
                <Box className={`hoverdesc ${classes.itemDesc}`}>{item.desc}</Box>
              </li>
            </>
          );
        })}
      </ul>
    </Box>
  );
};

const MonitorAddDialog = () => {
  const classes = useStyles();
  const [value, setValue] = useState('drift');
  const { data } = usePaginatedModels({
    query: '',
    page: 1,
    limit: 10,
    sort: 'name_asc'
  });
  const modelList = data?.modelList || [];
  console.log(modelList[0]?.name);
  const handleChange = (event: React.ChangeEvent<{}>, newValue: string) => {
    setValue(newValue);
  };
  const { modelID, pathLocation } = useSelector(
    (state: { modelMonitorState: ModelMonitorState }) => state.modelMonitorState
  );
  const modelNameData = ['model 1', 'model 2', 'model 3'];
  return (
    <Box className={classes.dialogBoxMonitorType}>
      <Box className={classes.modelContainer}>
        <Box className={classes.conatinerHeading}>Select Model</Box>
        {pathLocation === 'model' ? (
          <Select defaultValue={`${modelID}`} className={classes.select} disabled>
            <MenuItem value={`${modelID}`}>{modelID}</MenuItem>
          </Select>
        ) : (
          <Select defaultValue="select" className={classes.select}>
            <MenuItem value="select" disabled className="selectDisable">
              Select Model Name
            </MenuItem>
            {modelList.map((row: ModelListRow) => (
              <MenuItem value={row.name} key={row.id}>
                {row.name}
              </MenuItem>
            ))}
          </Select>
        )}
      </Box>
      <Box className={classes.tabContainer}>
        <Box className={classes.conatinerHeading}>Monitor Type</Box>
        <Tabs value={value} onChange={handleChange} className={classes.TabItems}>
          <Tab className={classes.TabItem} value={'drift'} label="Drift" />
          <Tab className={classes.TabItem} value={'model_performance'} label="Model Performance" />
          <Tab className={classes.TabItem} value={'data_quality'} label="Data Quality" />
        </Tabs>
        {value === 'drift' && (
          <>
            <TabContent
              data={[
                {
                  title: 'Data Drift',
                  desc:
                    'Lorem ipsum dolor sit amet consectetur, adipisicing elit. Fuga architecto voluptate repellat impedit minus rem optio neque ab aspernatur quaerat!',
                  disabled: false
                },
                {
                  title: 'Prediction Dift',
                  desc:
                    'Lorem ipsum dolor sit amet consectetur, adipisicing elit. Fuga architecto voluptate repellat impedit minus rem optio neque ab aspernatur quaerat!',
                  disabled: false
                }
              ]}
            />
          </>
        )}
        {value === 'model_performance' && (
          <>
            <TabContent
              data={[
                {
                  title: 'Performance Degradation',
                  desc:
                    'Lorem ipsum dolor sit amet consectetur, adipisicing elit. Fuga architecto voluptate repellat impedit minus rem optio neque ab aspernatur quaerat!',
                  disabled: false
                },
                {
                  title: 'Metric Change',
                  desc: 'Coming Soon ...',
                  disabled: true
                },
                {
                  title: 'Model Activity',
                  desc: 'Coming Soon ...',
                  disabled: true
                },
                {
                  title: 'Model Stellness',
                  desc: 'Coming Soon ...',
                  disabled: true
                }
              ]}
            />
          </>
        )}
        {value === 'data_quality' && (
          <>
            <TabContent
              data={[
                {
                  title: 'Missing Value',
                  desc:
                    'Lorem ipsum dolor sit amet consectetur, adipisicing elit. Fuga architecto voluptate repellat impedit minus rem optio neque ab aspernatur quaerat!',
                  disabled: false
                },
                {
                  title: 'New Values',
                  desc: 'Coming Soon ...',
                  disabled: true
                },
                {
                  title: 'Out Of Range',
                  desc: 'Coming Soon ...',
                  disabled: true
                }
              ]}
            />
          </>
        )}
      </Box>
    </Box>
  );
};

export default MonitorAddDialog;
