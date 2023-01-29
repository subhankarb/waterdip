import React, { useState, useEffect } from 'react';
import { Stepper, Step, StepLabel, Button, Typography, CircularProgress } from '@material-ui/core';
import { Formik, Form } from 'formik';
import { useQueryClient } from 'react-query';
import { useNavigate } from 'react-router-dom';
import { useSnackbar } from 'notistack';
import { makeStyles } from '@material-ui/core/styles';
import { colors } from '../../../../theme/colors';
import { Grid } from '@material-ui/core';
import MonitorCondition from './ComponentsStep/MonitorCondition';
import MonitorAction from './ComponentsStep/MonitorAction';
import formInitialValues from './FormInitialValues';
import FormMonitor from './FormMonitor';
import { PATH_DASHBOARD } from '../../../../routes/paths';
import { useMonitorCreate } from '../../../../api/monitors/createMonitor';
import MonitorReview from './ComponentsStep/MonitorReview';

const useStyles = makeStyles(() => ({
  container: {
    background: colors.white,
    padding: '1.8rem 2.4rem 3.2rem 2.4rem',
    borderRadius: '4px',
    marginTop: '1rem',
    marginBottom: '1.6rem',
    minHeight: '80vh'
  },
  stepperContainer: {
    margin: '1rem 0 0 0',
    height: '75%',
    '& .css-ua46y1-MuiStepConnector-line': {
      height: '100% !important',
      minHeight: 'none !important'
    }
  },
  stepGrid: {
    borderRight: `1px solid ${colors.textLight}`
  },
  contentGrid: {
    paddingLeft: '2rem'
  },
  stepLabel: {
    fontSize: '.8rem',
    fontWeight: 600,
    color: colors.text,
    letterSpacing: '0.1rem'
  }
}));

const steps = ['Monitor Condition', 'Action', 'Review'];
const { formId, formField } = FormMonitor;

function _renderStepContent(step: number, monitorType: any, model_id: any, model_version_id: any) {
  switch (step) {
    case 0:
      return (
        <>
          <MonitorCondition monitorType={monitorType} model_id={model_id} model_version_id={model_version_id}/>
          {/* <MonitorMethod monitorType={monitorType} /> */}
        </>
      );
    case 1:
      return (
        <>
          <MonitorAction />
        </>
      );
    case 2:
      return (
        <>
          <MonitorReview monitorType={monitorType}/>
        </>
      );
    default:
      return <div>Not Found</div>;
  }
}
type Props = {
  monitorType: any;
  model_id: any,
  model_version_id: any
};
export default function VerticalLinearStepper({ monitorType, model_id, model_version_id }: Props) {
  const classes = useStyles();
  const [activeStep, setActiveStep] = useState(0);
  const isLastStep = activeStep === steps.length - 1;
  // const currentValidationSchema = validationSchema[activeStep];

  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  const mutation = useMonitorCreate();

  async function _submitForm(values: any, actions: any) {
    try {
      const value = {
        "monitor_name": values.actions.monitor_name,
        "monitor_type": values.monitor_type === 'Data Quality' ? 'DATA_QUALITY' : values.monitor_type === 'Drift'? 'DRIFT' : 'PERFORMANCE',
        "monitor_identification": {
          "model_id": values.monitor_identification.model_id,
          "model_version_id": values.monitor_identification.model_version_id,
        },
        "monitor_condition": {
          "evaluation_metric": values.monitor_condition.evaluation_metric,
          ...(values.monitor_type!== "Model Performance") && {"dimensions": values.monitor_condition.dimensions},
          "threshold": {
            "threshold" : values.monitor_condition.threshold.threshold == "Lesser" ? "lt" : "gt",
            "value" : values.monitor_condition.threshold.value
          },
          "evaluation_window": values.monitor_condition.evaluation_window,
        },
        "severity": values.actions.severity
      }
      mutation.mutate(value, {
        onSuccess: () => {
          enqueueSnackbar('Monitor created successfully!', { variant: 'success' });
          navigate(PATH_DASHBOARD.general.monitors);
        }
      });
    } catch (error) {
      enqueueSnackbar('Error', { variant: 'error' });
      actions.isSubmitting(false);
      actions.setErrors(error);
    }
  }

  function _handleSubmit(values: any, actions: any) {
    if (isLastStep) {
      // window.alert(JSON.stringify(values));
      _submitForm(values, actions);
    } else {
      setActiveStep(activeStep + 1);
      actions.setTouched({});
      actions.setSubmitting(false);
    }
  }

  function _handleBack() {
    setActiveStep(activeStep - 1);
  }

  return (
    <>
      <Grid item container xs={12} className={classes.container}>
        <Grid className={classes.stepGrid} item xs={2}>
          <Stepper
            activeStep={activeStep}
            className={classes.stepperContainer}
            orientation="vertical"
          >
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel className={classes.stepLabel}>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>
        </Grid>

        <Grid className={classes.contentGrid} item xs={10}>
          <>
            {activeStep === steps.length ? (
              'Done'
            ) : (
              <Formik
                initialValues={formInitialValues}
                // validationSchema={currentValidationSchema}
                onSubmit={_handleSubmit}
              >
                {({ isSubmitting }) => (
                  <Form
                    id={formId}
                    style={{
                      margin: '15px 15px 15px 15px',
                      display: 'flex',
                      flexDirection: 'column',
                      height: '100%'
                    }}
                  >
                    {_renderStepContent(activeStep, monitorType, model_id, model_version_id)}
                    <div style={{ marginTop: 'auto' }}>
                      <div
                        style={{
                          display: 'inline-block',
                          float: 'right',
                          margin: '10px 10px 10px 10px'
                        }}
                      >
                        <Button
                          disabled={isSubmitting}
                          type="submit"
                          variant="contained"
                          sx={{
                            width: '130px',
                            height: '40px',
                            background: '#6780DC',
                            boxShadow: '0px 4px 10px rgba(103, 128, 220, 0.24)',
                            borderRadius: '4px'
                          }}
                        >
                          {isLastStep ? 'Add Monitor' : 'Next'}
                        </Button>
                        {isSubmitting && <CircularProgress size={24} />}
                      </div>
                      <div
                        style={{
                          display: 'inline-block',
                          float: 'right',
                          margin: '10px 10px 10px 10px'
                        }}
                      >
                        {activeStep !== 0 && (
                          <Button
                            sx={{
                              width: '100px',
                              height: '40px',

                              borderColor: '#6780DC',
                              borderRadius: '4px'
                            }}
                            variant="outlined"
                            onClick={_handleBack}
                          >
                            Back
                          </Button>
                        )}
                      </div>
                    </div>
                  </Form>
                )}
              </Formik>
            )}
          </>
        </Grid>
      </Grid>
    </>
  );
}
