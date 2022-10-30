import React from 'react';
import merge from 'lodash/merge';
import ReactApexChart from 'react-apexcharts';
import round from 'lodash/round';
import BaseOptionChart from './BaseOptionChart';

interface Props {
  name: string;
  categories: string[];
  data: number[];
  barSize?: number;
  handleBarClick?: (event: any, chartContext: any, config: any) => void;
  options?: {
    height?: number;
    width?: string;
    enableDataLabels?: boolean;
    showGridLines?: boolean;
    showXAxisLabels?: boolean;
    showYAxisLabels?: boolean;
    isHorizontal?: boolean;
    showLegend?: boolean;
  };
}

const ChartHistogram: React.FC<Props> = ({
  name,
  categories,
  data,
  handleBarClick,
  options,
  barSize
}) => {
  const barSize_ = barSize || 54;
  const isLargerWidth = categories.length * barSize_ > 1200;
  let chartOptions = merge(BaseOptionChart(), {
    stroke: { show: false },
    plotOptions: {
      bar: { borderRadius: 4, horizontal: options?.isHorizontal ?? false }
    },
    legend: {
      show: options?.showLegend ?? true
    },
    xaxis: {
      categories,
      labels: {
        show: options?.showXAxisLabels ?? true
      }
    },
    yaxis: {
      labels: {
        show: options?.showYAxisLabels ?? true
      }
    },
    dataLabels: {
      enabled: options?.enableDataLabels ?? true,
      formatter: (value: number) => round(value, 2)
    },
    grid: {
      show: options?.showGridLines ?? true
    }
  });
  if (handleBarClick) {
    chartOptions = merge(chartOptions, {
      chart: {
        events: {
          dataPointSelection: handleBarClick
        }
      }
    });
  }

  return (
    <div style={{ overflowX: isLargerWidth ? 'scroll' : 'hidden', overflowY: 'hidden' }}>
      <ReactApexChart
        type="histogram"
        series={[{ name, data }]}
        options={chartOptions}
        height={options?.height || 320}
        width={isLargerWidth ? categories.length * barSize_ : options?.width ?? '100%'}
      />
    </div>
  );
};

export default ChartHistogram;
