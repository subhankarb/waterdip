import { useEffect, useState } from 'react';
import { Box, Select, MenuItem, TextField, Button } from '@material-ui/core';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { makeStyles } from '@material-ui/core/styles';
import { colors } from '../../../../../theme/colors';
import { DialogAnimate } from '../../../../../components/animate';
import { useFormikContext } from 'formik';
import { fontSize } from '@material-ui/system';
import { useModelVersionInfo } from 'api/models/GetModelVersionInfo';

const useStyles = makeStyles(() => ({
  form: {
    // display: 'flex'
  },
  contentInput: {
    display: 'flex',
    flexDirection: 'column',
    margin: '0 0 1rem 0'
  },
  performData: {
    marginTop: '.3rem',
    display: 'flex',
    alignItems: 'center'
  },
  contentInputLabel: {
    fontSize: '.9rem',
    color: colors.text,
    fontWeight: 600,
    marginBottom: '.4rem'
  },
  contentInputDesc: {
    fontSize: '.7rem',
    color: colors.textLight,
    fontWeight: 400,
    marginBottom: '.65rem'
  },
  contentInputSubDesc: {
    fontSize: '.75rem',
    color: colors.text,
    fontWeight: 600
  },
  select: {
    transform: 'scale(1,.6)',
    maxWidth: '20rem',
    minWidth: '10rem',
    '& .MuiInputBase-input': {
      transform: 'scale(1,1.4)',
      fontSize: '.8rem'
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
      transform: 'scale(1,.75)',
      fontSize: '.8rem'
    }
  },
  numberInput: {
    transform: 'scale(1,.6)',
    width: '5rem',
    '& .MuiInputBase-input': {
      transform: 'scale(1,1.4)',
      fontSize: '.8rem'
    },
    '& .MuiOutlinedInput-root': {
      '& fieldset': {
        borderRadius: '4px',
        borderColor: colors.textLight
      },
      '&.Mui-focused fieldset': {
        borderColor: colors.text
      }
    }
  }
}));

const MonitorCondition = (props: any) => {
  const classes = useStyles();
  const [expandForm, setExpandForm] = useState(false);
  const formikProps = useFormikContext();
  const { values }: any = formikProps;
  const [dimension, setDimension] = useState<string[]>([]);
  const [prediction, setPrediction] = useState<string[]>([]);
  const [featureOrPrediction, setFeatureOrPrediction] = useState('');
  const [evaluationMetric, setevaluationMetric] = useState('');
  const [evaluationWindow, setevaluationWindow] = useState('');
  const [gtlt, setGTLT] = useState('');
  const [value, setValue] = useState<number>();

  const onDimensionChange = (e: React.ChangeEvent<{ value: unknown }>) => {
    
  }
  const { data, isLoading } = useModelVersionInfo({
    model_version_id: props.model_version_id
  });

  useEffect(() => {
    formikProps.setFieldValue('monitor_type', props.monitorType);
    formikProps.setFieldValue('monitor_identification.model_id', props.model_id);
    formikProps.setFieldValue('monitor_identification.model_version_id', props.model_version_id);
    formikProps.setFieldValue('monitor_condition.dimensions.features', dimension);
    formikProps.setFieldValue('monitor_condition.dimensions.predictions', prediction);
    formikProps.setFieldValue('monitor_condition.evaluation_window', evaluationWindow);
    formikProps.setFieldValue('monitor_condition.evaluation_metric', evaluationMetric);
    formikProps.setFieldValue('monitor_condition.threshold.threshold', gtlt);
    formikProps.setFieldValue('monitor_condition.threshold.value', value);
  }, [props.monitorType, dimension, evaluationWindow, gtlt, value]);
  return (
    <Box className={classes.form}>
      {props.monitorType === 'Model Performance' && (
        <Box className={classes.contentInput}>
          <label className={classes.contentInputLabel}>Evaluation Metric</label>
          <label className={classes.contentInputDesc}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </label>
          <label className={classes.contentInputSubDesc}>
            Select evaluation metric from the list
          </label>
          <Select
            required
            className={classes.select}
            onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
              setevaluationMetric(e.target.value as string);
            }}>
            <MenuItem value="PRECISION">Precision</MenuItem>
            <MenuItem value="RECALL">Recall</MenuItem>
            <MenuItem value="F1">F1</MenuItem>
          </Select>
        </Box>
      )}
      {props.monitorType === 'Data Quality' && (
        <Box className={classes.contentInput}>
          <label className={classes.contentInputLabel}>Evaluation Metric</label>
          <label className={classes.contentInputDesc}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </label>
          <label className={classes.contentInputSubDesc}>
            Select evaluation metric from the list
          </label>
          <Select
            required
            className={classes.select}
            onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
              setevaluationMetric(e.target.value as string);
            }}>
            <MenuItem value="MISSING_VALUE">Missing Value</MenuItem>
            <MenuItem value="EMPTY_VALUE">Empty Value</MenuItem>
            <MenuItem value="NEW_VALUE">New Value</MenuItem>
          </Select>
        </Box>
      )}
      {props.monitorType === 'Drift' && (
        <Box className={classes.contentInput}>
          <label className={classes.contentInputLabel}>Evaluation Metric</label>
          <label className={classes.contentInputDesc}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </label>
          <label className={classes.contentInputSubDesc}>
            Select evaluation metric from the list
          </label>
          <Select
            required
            className={classes.select}
            onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
              setevaluationMetric(e.target.value as string);
            }}>
            <MenuItem value="PSI">PSI</MenuItem>
          </Select>
        </Box>
      )}
      {props.monitorType !== 'Model Performance' && (
        <Box className={classes.contentInput}>
          <label className={classes.contentInputLabel}>Dimension</label>
          <label className={classes.contentInputDesc}>
            Dimension is a column of a dataset which can represent feature or prediction value
          </label>
          <label className={classes.contentInputSubDesc}>Select either Features or Predictions</label>
          <Select
            required
            className={classes.select}
            onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
              setFeatureOrPrediction(e.target.value as string);
              if(e.target.value==='feature') { setPrediction([])} else { setDimension([]) }
            }}>
            <MenuItem value="feature">Feature</MenuItem>
            <MenuItem value="prediction">Prediction</MenuItem>
          </Select>
          {featureOrPrediction === "feature" &&
            <>
            <label className={classes.contentInputSubDesc}>Select one or multiple features</label>
            <Autocomplete
            limitTags={1}
            multiple
            id="tags-outlined"
            options={!isLoading && data ? Object.keys(data.data.model_version.version_schema.features) : []}
            style={{ 
              width: 400, padding:"10px 0px 0px 0px"
            }}
            onChange={ (e,v) => setDimension(v)}
            filterSelectedOptions
            renderInput={(params) => (
              <TextField
                {...params}
                placeholder="Features"
                variant="outlined"
                InputLabelProps={ { required: true }}
              />
            )}
          />
          </>
          }
          {featureOrPrediction === "prediction" &&
            <>
            <label className={classes.contentInputSubDesc}>Select one or multiple predictions</label>
            <Autocomplete
            limitTags={1}
            multiple
            id="tags-outlined"
            options={!isLoading && data ? Object.keys(data.data.model_version.version_schema.predictions) : []}
            style={{ 
              width: 400, padding:"10px 0px 0px 0px"
            }}
            onChange={ (e,v) => setPrediction(v) }
            filterSelectedOptions
            renderInput={(params) => (
              <TextField
                {...params}
                variant="outlined"
                placeholder="Predictions"
                InputLabelProps={ { required: true }}
              />
            )}
          />
          </>
          }
        </Box>
      )}
      {props.monitorType === 'Model Performance' && (
        <Box className={classes.contentInput}>
          <label className={classes.contentInputLabel}>Performance Threshold</label>
          <label className={classes.contentInputDesc}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </label>
          <label className={classes.contentInputSubDesc}>
            Incident will triggered when threshold is
          </label>
          <div className={classes.performData}>
            <label className={classes.contentInputSubDesc}>Greater than &nbsp;&nbsp;&nbsp;</label>
            <Select
              required
              className={classes.select}
              onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
                setGTLT(e.target.value as string);
              }}
            >
              <MenuItem value="Greater">Greater Than</MenuItem>
              <MenuItem value="Lesser">Lesser Than</MenuItem>
            </Select>
            &nbsp;&nbsp;&nbsp;
            <label className={classes.contentInputSubDesc}>Value&nbsp;&nbsp;&nbsp;</label>
            <TextField
              required
              placeholder="Eg: 0.2"
              className={classes.numberInput}
              inputProps={{ min: 0, step: 0.01 }}
              type="number"
              onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
                setValue(e.target.value as number);
              }}
            ></TextField>
          </div>
        </Box>
      )}
      {props.monitorType === 'Data Quality' && (
        <Box className={classes.contentInput}>
          <label className={classes.contentInputLabel}>Metric Threshold</label>
          <label className={classes.contentInputDesc}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </label>
          <label className={classes.contentInputSubDesc}>
            Incident will triggered when threshold is
          </label>
          <div className={classes.performData}>
            <Select
              required
              className={classes.select}
              onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
                setGTLT(e.target.value as string);
              }}
            >
              <MenuItem value="Greater">Greater Than</MenuItem>
              <MenuItem value="Lesser">Lesser Than</MenuItem>
            </Select>
            &nbsp;&nbsp;&nbsp;
            <label className={classes.contentInputSubDesc}>Value&nbsp;&nbsp;&nbsp;</label>
            <TextField
              required
              placeholder="Eg: 0.2"
              className={classes.numberInput}
              type="number"

              onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
                setValue(e.target.value as number);
              }}
            ></TextField>
          </div>
        </Box>
      )}
      {props.monitorType === 'Drift' && (
        <Box className={classes.contentInput}>
          <label className={classes.contentInputLabel}>Drift Threshold</label>
          <label className={classes.contentInputDesc}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </label>
          <label className={classes.contentInputSubDesc}>
            Incident will triggered when threshold is
          </label>
          <div className={classes.performData}>
            <label className={classes.contentInputSubDesc}>Greater than &nbsp;&nbsp;&nbsp;</label>
            <Select
              required
              className={classes.select}
              onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
                setGTLT(e.target.value as string);
              }}
            >
              <MenuItem value="Greater">Greater Than</MenuItem>
              <MenuItem value="Lesser">Lesser Than</MenuItem>
            </Select>
            &nbsp;&nbsp;&nbsp;
            <label className={classes.contentInputSubDesc}>Value&nbsp;&nbsp;&nbsp;</label>
            <TextField
              required
              placeholder="Eg: 0.2"
              className={classes.numberInput}
              type="number"
              onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
                setValue(e.target.value as number);
              }}
            ></TextField>
          </div>
        </Box>
      )}
      <Box className={classes.contentInput}>
        <label className={classes.contentInputLabel}>Evaluation Window</label>
        <label className={classes.contentInputDesc}>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        </label>
        <label className={classes.contentInputSubDesc}>Select evaluation window</label>
        <Select
          required
          className={classes.select}
          onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
            setevaluationWindow(e.target.value as string);
          }}
        >
          <MenuItem value="1d">24 Hrs</MenuItem>
          <MenuItem value="7d">1 Week</MenuItem>
          <MenuItem value="31d">1 Month</MenuItem>
        </Select>
      </Box>
    </Box>
  );
};

export default MonitorCondition;

// <Box className={classes.contentInput}>
//   <label className={classes.contentInputLabel}>BaseLine</label>
//   <Button className={classes.contentButton} onClick={() => setExpandForm((state) => !state)}>
//     Configure baseline {'>'}
//   </Button>
//   <DialogAnimate open={expandForm} onClose={() => setExpandForm(false)}></DialogAnimate>
// </Box>;
