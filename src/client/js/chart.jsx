/**
 * A chart component that renders timeseries data.
 */

import Moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';
import { VictoryAxis, VictoryChart, VictoryScatter, VictoryTheme, VictoryVoronoiContainer } from 'victory';

/**
 * A chart component for rendering timeseries data.
 */
class Chart extends React.Component {
  /**
   * Renders chart DOM elements.
   * @returns {undefined}
   */
  render() {
    const container = (<VictoryVoronoiContainer labels={(d) => `${d.x.format('YYYY-MM-DD[T]HH:mm:ss.SSS')}, ${d.y}`} />);
    const data = this.props.data.map((e) => ({x: e.ts, y: parseFloat(e.valueString)}));
    return (
      <VictoryChart
        containerComponent={container}
        theme={VictoryTheme.material}
        scale={{ x: 'time' }}
        width={1280}
        height={720}>
        <VictoryScatter data={data} />
      </VictoryChart>
    );
  }
}

Chart.propTypes = {
  data: PropTypes.array.isRequired,
  label: PropTypes.string.isRequired
};

export default Chart;
