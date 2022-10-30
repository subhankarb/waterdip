import React from 'react';
import merge from 'lodash/merge';
import ReactApexChart from 'react-apexcharts';
import BaseOptionChart from './BaseOptionChart';
import { ChartSeries, ChartCategories } from '../../@types/charts';

interface Props {
  categories: ChartCategories;
  series: ChartSeries[];
  height?: number;
}

const ChartBar: React.FC<Props> = ({ categories, series, height }) => {
  const chartOptions = merge(BaseOptionChart(), {
    legend: { position: 'top', horizontalAlign: 'right' },
    xaxis: {
      categories
    }
  });

  return (
    <ReactApexChart type="area" series={series} options={chartOptions} height={height || 364} />
  );
};

export default ChartBar;
