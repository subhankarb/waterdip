import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Tabs, Tab } from '@material-ui/core';
import './tab.css';
import { useState, useEffect } from 'react';
import { colors } from '../../../../theme/colors';

const useStyles = makeStyles({
  root: {
    flexGrow: 1,
    width: '150px',
    height: '100%',
    borderRight: `1px solid ${colors.tableHeadBack}`,
    marginTop: '.8rem',
    paddingTop: '.4rem'
  },
  TabItem: {
    marginRight: '0 !important',
    minHeight: '32px',
    borderRadius: 0,
    fontWeight: 400,
    fontSize: '.75rem',
    color: colors.textLight,
    paddingLeft: '1rem'
  }
});
type Props = {
  onChange: Function;
  currentTab: string;
};

export default function TabsPerformance({ onChange, currentTab }: Props) {
  const classes = useStyles();
  const [value, setValue] = React.useState(currentTab);
  console.log(colors.tableHeadBack);

  const handleChange = (event: React.ChangeEvent<{}>, newValue: string) => {
    setValue(newValue);
  };

  useEffect(() => {
    onChange(value);
  }, [value]);

  return (
    <div className={classes.root}>
      <Tabs
        value={value}
        onChange={handleChange}
        indicatorColor="primary"
        textColor="primary"
        orientation="vertical"
        className="tabs-left"
      >
        <Tab className={classes.TabItem} value={'accuracy'} label="Accuracy" />
        <Tab className={classes.TabItem} value={'precision'} label="Precision" />
        <Tab className={classes.TabItem} value={'recall'} label="Recall" />
        <Tab className={classes.TabItem} value={'f1'} label="F1" />
        <Tab className={classes.TabItem} value={'sensitivity'} label="Sensitivity" />
        <Tab className={classes.TabItem} value={'specificity'} label="Specificity" />
        <Tab className={classes.TabItem} value={'fp_rate'} label="FP Rate" />
        <Tab className={classes.TabItem} value={'fn_rate'} label="FN Rate" />
        <Tab className={classes.TabItem} value={'fn_density'} label="FN Density" />
      </Tabs>
    </div>
  );
}
