import React, { useState } from 'react';
import ReactApexChart from 'react-apexcharts';
import { ApexOptions } from 'apexcharts';

const ChartSparkline = ({ data, colors }: any) => {
  const [series, setSeries] = useState([
    {
      data: data
    }
  ]);
  const option: ApexOptions = {
    chart: {
      sparkline: {
        enabled: true
      }
    },
    colors: [colors],

    fill: {
      colors: [colors]
    },
    stroke: {
      curve: 'smooth',
      width: 1
    },
    tooltip: {
      enabled: true,
      followCursor: true,
      style: {
        fontSize: '12px',
        fontFamily: 'Poppins'
      },
      onDatasetHover: {
        highlightDataSeries: false
      },
      x: {
        show: false
      },
      y: {
        formatter: undefined,
        title: {
          formatter: () => ''
        }
      },
      marker: {
        show: false
      }
    }
  };
  return (
    <div>
      <ReactApexChart options={option} type="area" series={series} />
    </div>
  );
};

export default ChartSparkline;
