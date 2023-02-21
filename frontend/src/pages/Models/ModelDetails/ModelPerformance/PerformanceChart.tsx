import ReactApexChart from 'react-apexcharts';
import { ApexOptions } from 'apexcharts';
import React, { useState, useEffect } from 'react';
import { formattedDate, formatDateTime } from '../../../../utils/date';
import { colors } from '../../../../theme/colors';

type Props = {
  dateValue: any;
  tabValue: string;
};

const PerformanceChart = ({ dateValue, tabValue }: Props) => {
  
  const series = [
    {
      name: tabValue,
      data: dateValue && dateValue.value ? dateValue.value : []
    }
  ];

  const option: ApexOptions = {
    chart: {
      height: 270,
      type: 'bar',
      toolbar: {
        show: false
      }
    },
    plotOptions: {
      bar: {
        columnWidth: '50%'
      }
    },
    dataLabels: {
      enabled: false
    },
    colors: [`${colors.graphLight}`],

    xaxis: {
      labels: {
        rotate: -45,
        style: {}
      },
      categories: dateValue && dateValue.date ? dateValue.date : []
    },
    yaxis: {
      decimalsInFloat: 3,

      title: {
        text: tabValue,
        style: {
          fontWeight: 400,
          fontSize: '.75rem',
          color: '#212B36',
          cssClass: 'apexcharts-yaxis-title'
        }
      }
    }
  };
  return (
    <div>
      <ReactApexChart options={option} series={series} type="bar" height={270} />
    </div>
  );
};

export default PerformanceChart;
