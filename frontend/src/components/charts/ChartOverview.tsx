import React, { useState, useEffect } from 'react';
import ReactApexChart from 'react-apexcharts';
import ApexCharts from 'apexcharts';
import { ApexOptions } from 'apexcharts';
import { colors } from '../../theme/colors';

type Props = {
  state: any;
  data: any;
};
const ChartLine = ({ state, data }: Props) => {
  const [series, setSeries] = useState([
    {
      name: 'hist',
      type: 'column',
      data: data.predictions.val ? data.predictions.val : [],
    },
    ...data.predictions_versions.map((item: any) => {
      const id = Object.keys(item)[0];
      return { name: id, type: 'line', show: false, data: item[id].val };
    })
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
      opacity: [1, 1, 1],
      gradient: {
        inverseColors: false,
        shade: 'light',
        type: 'vertical',
        opacityFrom: 0.85,
        opacityTo: 0.55,
        stops: [0, 100, 100, 100]
      }
    },
    labels: data.predictions.date_bins ? data.predictions.date_bins : [],
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
    state.forEach((seriesState: any, index: any) => {
        Object.keys(seriesState).forEach(id => {
            if (seriesState[id] === false) {
                ApexCharts.exec('overview', 'hideSeries', `${id}`);
            } else {
                ApexCharts.exec('overview', 'showSeries', `${id}`);
            }
        });
    });
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
