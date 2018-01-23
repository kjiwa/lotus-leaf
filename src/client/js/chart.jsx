/**
 * A chart component that renders timeseries data.
 */

import Moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';
import { VictoryChart, VictoryLegend, VictoryScatter, VictoryTheme, VictoryVoronoiContainer } from 'victory';

const CHART_COLORS = [
  '#e94858', '#f3a32a', '#82BF6E', '#3CB4CB',
  '#16434B', '#d9f35a', '#13aacb', '#5b6368',
  '#ac62b2', '#5f62a0', '#17b2b4', '#80217a'
];

/**
 * A chart component for rendering timeseries data.
 */
class Chart extends React.Component {
  /**
   * Renders chart DOM elements.
   * @returns {undefined}
   */
  render() {
    // Use a Voronoi container so that labels appear over data points.
    const container = (
      <VictoryVoronoiContainer
        labels={(d) => `${d.x.format('YYYY-MM-DD[T]HH:mm:ss.SSS')}, ${d.y}`} />
    );

    // Group data by topic ID.
    const data = {};
    this.props.data.forEach(function(datum) {
      if (!(datum.topicId in data)) {
        data[datum.topicId] = [];
      }

      data[datum.topicId].push({
        x: datum.ts,
        y: parseFloat(datum.valueString)
      });
    });

    // Create a scatter chart for each topic ID.
    const charts = [];
    const legendData = [];
    const topics = this.props.topics;
    Object.keys(data).forEach(function(topicId, index) {
      const color = CHART_COLORS[index % CHART_COLORS.length];
      const topic = topics.find((e) => (e.topicId == topicId));

      charts.push(
        <VictoryScatter
          key={topicId}
          data={data[topicId]}
          style={{ data: { fill: color } }} />
      );

      legendData.push({
        name: topic.topicName,
        symbol: { fill: color }
      });
    });

    // Create legend entries.
    Object.keys(data).forEach(function(topicId, index) {
    });

    return (
      <VictoryChart
        containerComponent={container}
        theme={VictoryTheme.material}
        scale={{ x: 'time' }}
        width={1280}
        height={720}>

        {charts}
        <VictoryLegend
          gutter={16}
          x={960} y={64}
          data={legendData} />
      </VictoryChart>
    );
  }
}

Chart.propTypes = {
  data: PropTypes.array.isRequired,
  topics: PropTypes.array.isRequired
};

export default Chart;
