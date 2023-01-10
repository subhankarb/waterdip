import ReactApexChart from 'react-apexcharts';
import { ApexOptions } from 'apexcharts';
import React, { useState, useEffect } from 'react';
import { formattedDate, formatDateTime } from '../../../../utils/date';
import { colors } from '../../../../theme/colors';

type Props = {
  dataValue: any;
  tabValue: string;
};

const PerformanceChart = ({ dataValue, tabValue }: Props) => {
  const series = [
    {
      name: tabValue,
      data: dataValue?.data.map((i: number) => Math.round(i * 1000) / 1000)
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
      categories: dataValue.time_buckets
        ? dataValue.time_buckets.map((item: any) => item.split('T')[0])
        : []
    },
    yaxis: {
      decimalsInFloat: tabValue === 'accuracy' ? 0 : 3,

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
