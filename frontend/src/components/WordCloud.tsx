import React from 'react';
import ReactWordcloud, { OptionsProp } from 'react-wordcloud';
import 'tippy.js/dist/tippy.css';
import 'tippy.js/animations/scale.css';

interface Props {
  data: {
    text: string;
    value: number;
  }[];
}

const options: OptionsProp = {
  colors: ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
  enableTooltip: true,
  deterministic: false,
  fontFamily: 'Public Sans',
  fontSizes: [5, 60],
  fontStyle: 'normal',
  fontWeight: 'normal',
  padding: 1,
  rotations: 3,
  rotationAngles: [0, 90],
  scale: 'sqrt',
  spiral: 'archimedean',
  transitionDuration: 1000
};

const WordCloud: React.FC<Props> = ({ data }) => <ReactWordcloud words={data} options={options} />;

export default WordCloud;
