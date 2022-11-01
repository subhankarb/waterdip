import { merge } from 'lodash';
import ReactApexChart from 'react-apexcharts';
import BaseOptionChart from './BaseOptionChart';

interface Props {
  categories: string[];
  data: {
    name: string;
    data: number[];
  }[];
}

const ChartColumnStacked: React.FC<Props> = ({ categories, data }) => {
  const barSize = 60;
  const isLargerWidth = categories.length * barSize > 1200;
  const chartOptions = merge(BaseOptionChart(), {
    chart: {
      stacked: true,
      stackType: '100%',
      zoom: { enabled: true }
    },
    legend: {
      itemMargin: { vertical: 8 },
      position: 'top',
      horizontalAlign: 'left',
      offsetX: 20
    },
    plotOptions: { bar: { borderRadius: 4 } },
    stroke: { show: false },
    xaxis: {
      type: 'string',
      categories
    },
    dataLabels: {
      enabled: true
    }
  });

  return (
    <div style={{ overflowX: isLargerWidth ? 'scroll' : 'hidden', overflowY: 'hidden' }}>
      <ReactApexChart
        type="bar"
        series={data}
        options={chartOptions}
        height={350}
        width={isLargerWidth ? categories.length * barSize : '100%'}
      />
    </div>
  );
};

export default ChartColumnStacked;
