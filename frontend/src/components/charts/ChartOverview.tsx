import React, { useState, useEffect } from 'react';
import ReactApexChart from 'react-apexcharts';
import { ApexOptions } from 'apexcharts';
import { colors } from '../../theme/colors';

type Props = {
  state: { T1: boolean; T2: boolean };
  data: any;
};
const ChartLine = ({ state, data }: Props) => {
  const [series, setSeries] = useState([
    {
      name: 'hist',
      type: 'column',
      data: data.predictions ? data.predictions : []
    },
    {
      name: 'T1',
      type: 'line',
      data: data.predictions_target_class.pred_1 ? data.predictions_target_class.pred_1 : []
    },
    {
      name: 'T2',
      type: 'line',
      data: data.predictions_target_class.pred_2 ? data.predictions_target_class.pred_2 : []
    }
  ]);
  const option: ApexOptions = {
    chart: {
      id: 'overview',
      height: 270,
      type: 'line',
      stacked: false,
      toolbar: {
        show: false
      }
    },
    stroke: {
      curve: 'straight',
      width: [0, 2, 2]
    },
    legend: {
      show: false
    },
    plotOptions: {
      bar: {
        columnWidth: '50%'
      }
    },
    colors: [colors.graphLight, colors.graphA, colors.graphB],

    fill: {
      // opacity: [0.5, 1, 1]
      // gradient: {
      //   inverseColors: false,
      //   shade: 'light',
      //   type: 'vertical',
      //   opacityFrom: 0.85,
      //   opacityTo: 0.55,
      //   stops: [0, 100, 100, 100]
      // }
    },
    labels: data.time_buckets ? data.time_buckets : [],
    xaxis: {
      type: 'datetime'
    },
    yaxis: {
      title: {
        text: 'Prediction Volume',
        style: {
          fontWeight: 400,
          fontSize: '.75rem',
          color: colors.text,
          cssClass: 'apexcharts-yaxis-title'
        }
      },
      min: 0
    }
  };
  useEffect(() => {
    for (const [key, value] of Object.entries(state)) {
      if (value == false) {
        ApexCharts.exec('overview', 'hideSeries', `${key}`);
      } else {
        ApexCharts.exec('overview', 'showSeries', `${key}`);
      }
    }
  }, [state]);
  return (
    <>
      <div>
        <ReactApexChart options={option} series={series} height={270} />
      </div>
    </>
  );
};

export default ChartLine;
