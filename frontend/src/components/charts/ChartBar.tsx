import React from 'react';
import merge from 'lodash/merge';
import ReactApexChart from 'react-apexcharts';
import round from 'lodash/round';
import BaseOptionChart from './BaseOptionChart';
import { colors } from '../../theme/colors';

interface Props {
  name: string;
  categories: string[];
  data: number[];
  handleBarClick?: (event: any, chartContext: any, config: any) => void;
  options?: {
    height?: number;
    width?: string;
    enableDataLabels?: boolean;
    showGridLines?: boolean;
    showXAxisLabels?: boolean;
    showYAxisLabels?: boolean;
    isHorizontal?: boolean;
    sparkline?: boolean;
    color?: string;
    columnWidth?: string;
    followCursor?: boolean;
    tooltip?: {
      enabled?: boolean;
      followCursor?: boolean;
      style?: {
        fontSize?: string;
        fontFamily?: string;
      };
      onDatasetHover?: {
        highlightDataSeries?: boolean;
      };
      x?: {
        show?: boolean;
      };
      y?: {
        formatter?: any;
        title?: {
          formatter?: any;
        };
      };
      marker?: {
        show?: boolean;
      };
    };
  };
}

const ChartBar: React.FC<Props> = ({ name, categories, data, handleBarClick, options }) => {
  const barSize = 54;
  const isLargerWidth = categories.length * barSize > 1200;
  let chartOptions = merge(BaseOptionChart(), {
    stroke: { show: false },
    plotOptions: {
      bar: {
        borderRadius: 0,
        horizontal: options?.isHorizontal ?? false,
        columnWidth: options?.columnWidth ?? '70%'
      }
    },

    chart: {
      sparkline: {
        enabled: options?.sparkline ?? false
      }
    },
    colors: [options?.color ?? colors.graphLight],
    xaxis: {
      categories,
      labels: {
        show: options?.showXAxisLabels ?? true
      }
    },
    tooltip: options?.tooltip ?? {},

    yaxis: {
      title: {
        text: name,
        style: {
          fontWeight: 400,
          fontSize: '.75rem',
          color: colors.text,
          cssClass: 'apexcharts-yaxis-title'
        }
      },
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
        type="bar"
        series={[{ name, data }]}
        options={chartOptions}
        height={options?.height || 320}
        width={isLargerWidth ? categories.length * barSize : options?.width ?? '100%'}
      />
    </div>
  );
};

export default ChartBar;
