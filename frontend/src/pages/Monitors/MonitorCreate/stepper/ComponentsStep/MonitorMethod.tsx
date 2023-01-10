import { useEffect, useState } from 'react';
import { Box, Select, MenuItem, TextField, Input, TextareaAutosize } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { colors } from '../../../../../theme/colors';
import { useFormikContext } from 'formik';
import { useGetDatasets } from '../../../../../api/datasets/GetDatasets';

const useStyles = makeStyles(() => ({
  form: { display: 'flex' },
  label: {
    [`& > input + div`]: {
      background: colors.boxBackground,
      border: `0px solid ${colors.textPrimary}`,
      transition: 'all 0.15s ease-in-out'
    },
    [`& > input:checked + div`]: {
      border: `2px solid ${colors.textPrimary}`,
      background: colors.primaryLight
    }
  },
  inputRadio: {
    display: 'none'
  },
  radioBox: {
    borderRadius: '7px',
    width: '270px',
    padding: '18px 20px',
    margin: '0 30px 0 0',
    cursor: 'pointer',
    transition: 'all 0.25s ease-in-out',
    [`&:hover`]: {
      transform: 'scale(1.025)'
    }
  },
  radioBoxTitle: {
    fontSize: '.8rem',
    color: colors.text,
    fontWeight: 600,
    marginBottom: '.4rem'
  },
  radioBoxDescription: {
    fontSize: '.65rem',
    fontWeight: 400,
    color: colors.text,
    lineHeight: '1.2rem',
    letterSpacing: '0.05rem',
    textAlign: 'justify'
  },
  baseLineContent: {
    marginTop: '3rem',
    width: '50%',
    color: colors.text,
    background: colors.boxBackground,
    borderRadius: '4px',
    padding: '1rem'
  },
  contentHeading: {
    fontSize: '.85rem',
    fontWeight: 600,
    letterSpacing: '.25px',
    marginBottom: '.5rem'
  },
  contentText: {
    fontSize: '.7rem',
    color: colors.textLight,
    fontWeight: 400,
    marginBottom: '.65rem'
  },
  select: {
    transform: 'scale(1,.75)',
    backgroundColor: `${colors.tableHeadBack} !important`,
    // maxWidth: '20rem',
    width: '10rem',
    height: '2.3rem',
    fontSize: '.85rem',
    '& .MuiInputBase-input': {
      transform: 'scale(1,1.25)'
    },
    [`& fieldset`]: {
      borderRadius: 4,
      borderColor: `${colors.textLight} !important`
    },
    [`&.Mui-focused fieldset`]: {
      borderRadius: 4,
      borderColor: `${colors.text} !important`
    },
    option: {
      transform: 'scale(1,.75)'
    }
  }
}));
type Props = {
  monitorType: any;
};
const MonitorMethod = ({ monitorType }: Props) => {
  const formikProps = useFormikContext();
  const { values }: any = formikProps;
  const [state, setState] = useState('');
  const [dataset, setDataset] = useState('');
  const [timePeriod, setTimePeriod] = useState('');

  // const { data, isLoading } = useGetDatasets({
  //   query: '',
  //   page: 1,
  //   limit: 10,
  //   sort: 'name_asc',
  //   model_id: ''
  // });
  // const datasetList = data?.dataset_list || [];

  useEffect(() => {
    formikProps.setFieldValue('monitor_type', monitorType);
  }, [monitorType]);

  useEffect(() => {
    formikProps.setFieldValue('monitor_method.method', state);
    formikProps.setFieldValue('monitor_method.dataset_id', dataset);
    formikProps.setFieldValue('monitor_method.baseline.time_period', timePeriod);
  }, [state, dataset, timePeriod]);

  const classes = useStyles();

  const handleRadioChange = (event: any) => {
    setState(event.currentTarget.value);
  };

  return (
    <>
      <Box className={classes.form}>
        <label className={classes.label}>
          <input
            className={classes.inputRadio}
            type="radio"
            name="monitor_method"
            value="anomaly_detection"
            id=""
            // defaultChecked
            onChange={handleRadioChange}
          />
          <Box className={classes.radioBox}>
            <Box className={classes.radioBoxTitle}>Anomaly Detection</Box>
            <Box className={classes.radioBoxDescription}>
              Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quidem aliquam et similique
              praesentium. Quis, mollitia eos aperiam deleniti architecto maiores.
            </Box>
          </Box>
        </label>
        <label className={classes.label}>
          <input
            className={classes.inputRadio}
            type="radio"
            name="monitor_method"
            value="compared_to_dataset"
            id=""
            onChange={handleRadioChange}
          />
          <Box className={classes.radioBox}>
            <Box className={classes.radioBoxTitle}>Compared to dataset</Box>
            <Box className={classes.radioBoxDescription}>
              Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quidem aliquam et similique
              praesentium. Quis, mollitia eos aperiam deleniti architecto maiores.
            </Box>
          </Box>
        </label>
      </Box>
      {state === 'anomaly_detection' ? (
        <div className={classes.baseLineContent}>
          <div className={classes.contentHeading}>Baseline</div>
          <hr />
          <div className={classes.contentText}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </div>
          <Select
            defaultValue={'15 days'}
            className={classes.select}
            onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
              setTimePeriod(e.target.value as string);
            }}
          >
            <MenuItem value="5 days">5 days</MenuItem>
            <MenuItem value="10 days">10 days</MenuItem>
            <MenuItem value="15 days">15 days</MenuItem>
          </Select>
        </div>
      ) : null}
      {state === 'compared_to_dataset' ? (
        <div className={classes.baseLineContent}>
          <div className={classes.contentHeading}>Baseline</div>
          <hr />
          <div className={classes.contentText}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </div>
          {
            <Select
              defaultValue=""
              className={classes.select}
              onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
                setDataset(e.target.value as string);
              }}
            >
              {/* {datasetList.map((item: any) => (
                <MenuItem value={item.dataset_id} key={item.dataset_id}>
                  {item.dataset_name}
                </MenuItem>
              ))} */}
            </Select>
          }
        </div>
      ) : null}
    </>
  );
};

export default MonitorMethod;
