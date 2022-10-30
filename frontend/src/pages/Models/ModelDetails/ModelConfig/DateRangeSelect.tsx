import React, { useState, useEffect } from 'react';
import { Select, MenuItem, TextField, Typography, Box } from '@material-ui/core';
import { DateRange, DateRangePicker, LocalizationProvider } from '@material-ui/lab';
import AdapterDateFns from '@material-ui/lab/AdapterDateFns';
import { formatDateTime, computeDateRange } from '../../../../utils/date';
import calendarFill from '@iconify/icons-eva/calendar-fill';
import { Icon } from '@iconify/react';
import ClickAwayListener from '@material-ui/core/ClickAwayListener';

const timeDuration: Record<string, number> = {
  last5hours: 5 * 60 * 60 * 1000,
  last1day: 24 * 60 * 60 * 1000,
  last10days: 10 * 24 * 60 * 60 * 1000,
  lastmonth: 30 * 24 * 60 * 60 * 1000
};
type Props = {
  onSelect: Function;
};
const DateTimePickerDropdown = ({ onSelect }: Props) => {
  const [selectValue, setSelectValue] = useState<string>('last5hours');
  const [dRValue, setDRValue] = useState<DateRange<Date>>([null, null]);
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [boxShow, setBoxShow] = useState(true);
  const handleClickAway = () => {
    setShowDatePicker(false);
  };

  useEffect(() => {
    if (selectValue === 'showpicker' && dRValue[0] && dRValue[1]) onSelect(dRValue, boxShow);
    else if (selectValue !== 'showpicker') {
      onSelect([new Date(new Date().getTime() - timeDuration[selectValue]), new Date()], boxShow);
    }
  }, [dRValue, boxShow, selectValue]);

  const getDisplayDateTimeRange = (value: string) => {
    let dateTimeString;
    let dateRange;
    const now = new Date();

    if (value !== 'showpicker' && dRValue[0] && dRValue[1]) {
      // when some other option selected from dropdown other showpicker,
      // reset the daterangevalue state
      setDRValue([null, null]);
    }

    if (value === 'last5hours') {
      dateTimeString = `${formatDateTime(
        new Date(now.getTime() - timeDuration.last5hours)
      )} to ${formatDateTime(now)}`;
      dateRange = '5h';
    } else if (value === 'last1day') {
      dateTimeString = `${formatDateTime(
        new Date(now.getTime() - timeDuration.last1day)
      )} to ${formatDateTime(now)}`;
      dateRange = '1D';
    } else if (value === 'last10days') {
      dateTimeString = `${formatDateTime(
        new Date(now.getTime() - timeDuration.last10days)
      )} to ${formatDateTime(now)}`;
      dateRange = '10D';
    } else if (value === 'lastmonth') {
      dateTimeString = `${formatDateTime(
        new Date(now.getTime() - timeDuration.lastmonth)
      )} to ${formatDateTime(now)} `;
      dateRange = '1M';
    } else if (value === 'showpicker') {
      if (dRValue[0] && dRValue[1]) {
        dateTimeString = `${formatDateTime(dRValue[0])} to ${formatDateTime(dRValue[1])} `;
        dateRange = computeDateRange(dRValue[0], dRValue[1]);
      } else dateTimeString = 'Custom Date';
    }
    return (
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          width: '250px',
          height: '32px',
          background: '#F5F6F8',
          borderRadius: '4px'
        }}
      >
        {/*{dateRange && (*/}
        {/*  <>*/}
        {/*    <Chip color="primary" size="small" label={dateRange} /> &nbsp;&nbsp;*/}
        {/*  </>*/}
        {/*)}*/}
        <Icon icon={calendarFill} width={20} height={20} />
        <Typography
          sx={{
            fontFamily: 'Poppins',
            fontStyle: 'normal',
            fontWeight: 500,
            fontSize: '13px',
            letterSpacing: '0.25px',
            marginLeft: '15px'
          }}
        >
          {dateTimeString}
        </Typography>
      </Box>
    );
  };

  return (
    <ClickAwayListener onClickAway={handleClickAway}>
      <Box sx={{ display: 'flex', height: '60px', alignItems: 'center' }}>
        <Select
          id="date-range-select"
          value={selectValue}
          onChange={(e: React.ChangeEvent<{ value: unknown }>) => {
            setSelectValue(e.target.value as string);
            setBoxShow(false);
          }}
          MenuProps={{
            anchorOrigin: {
              vertical: 'bottom',
              horizontal: 'left'
            },
            transformOrigin: {
              vertical: 'top',
              horizontal: 'left'
            }
          }}
          native={false}
          sx={{
            width: '266px',
            height: '32px',
            background: '#F5F6F8',
            borderRadius: '4px',
            border: 'none'
          }}
          renderValue={(value) => getDisplayDateTimeRange(value)}
          onClose={(event: React.SyntheticEvent<Element, Event>) => {
            if (Object.values(event.currentTarget)[1]['data-value'] === 'showpicker')
              setShowDatePicker(true);
          }}
        >
          <MenuItem value="last1day">Last 1 day</MenuItem>
          <MenuItem value="last10days">Last 10 days</MenuItem>
          <MenuItem value="lastmonth">Last month</MenuItem>
          <MenuItem value="showpicker">Custom Date</MenuItem>
        </Select>
        <LocalizationProvider dateAdapter={AdapterDateFns}>
          <DateRangePicker
            open={showDatePicker}
            onOpen={() => setDRValue([null, null])}
            value={dRValue}
            onChange={(newValue) => {
              setDRValue(newValue);
              setBoxShow(false);
            }}
            onAccept={() => setShowDatePicker(false)}
            renderInput={(startProps) => (
              <TextField
                sx={{ display: 'none' }}
                {...{
                  ...startProps,
                  inputProps: { ...startProps.inputProps, placeholder: '' },
                  helperText: '',
                  label: ''
                }}
              >
                Custom Date
              </TextField>
            )}
          />
        </LocalizationProvider>
      </Box>
    </ClickAwayListener>
  );
};

export default DateTimePickerDropdown;
