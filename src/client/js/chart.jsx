/**
 * A chart component that renders timeseries data.
 */

import ChartJs from 'chart.js';
import Moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';
import uuid4 from 'uuid/v4';
import { withStyles } from 'material-ui/styles';

const styles = (theme) => ({ canvas: {} });

/**
 * A chart component for rendering timeseries data.
 */
class Chart extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      // The chart.js object.
      chart: null
    };
  }

  /**
   * Handles post-render page processing after the initial render.
   * @returns {undefined}
   */
  componentDidMount() {
    this.refreshChart();
  }

  /**
   * Checks whether the component requires a refresh.
   * @param {Object} nextProps The next properties values to be set.
   * @param {Object} nextState The next state values to be set.
   * @returns {boolean} Whether the component should process updates.
   */
  shouldComponentUpdate(nextProps, nextState) {
    if (this.props.data.length != nextProps.data.length) {
      return true;
    }

    const sortedData = this.props.data.slice(0);
    sortedData.sort((a, b) => (a.ts.milliseconds() - b.ts.milliseconds()));

    const sortedNextData = nextProps.data.slice(0);
    sortedNextData.sort((a, b) => (a.ts.milliseconds() - b.ts.milliseconds()));

    for (let i = 0, j = sortedData.length; i < j; ++i) {
      const a = sortedData[i];
      const b = sortedNextData[i];
      if (!a.ts.isSame(b.ts) || a.topicId != b.topicId || a.valueString != b.valueString) {
        return true;
      }
    }

    return false;
  }

  /**
   * Handles post-render page processing after property updates.
   * @returns {undefined}
   */
  componentDidUpdate() {
    this.refreshChart();
  }

  /**
   * Renders chart DOM elements.
   * @returns {undefined}
   */
  render() {
    const { classes } = this.props;
    return <canvas className={classes.canvas} />;
  }

  /**
   * Refreshes the chart.
   * @returns {undefined}
   */
  refreshChart() {
    // TODO(kjiwa): Put this into a worker thread.
    const data = this.props.data.map((e) => ({
      x: new Moment(e.ts),
      y: parseFloat(e.valueString)
    }));

    const args = {
      type: 'scatter',
      data: {
        datasets: [
          {
            label: this.props.label,
            data: data,
            backgroundColor: '#4b2e83',
            borderColor: '#4b2e83',
            borderWidth: 1
          }
        ]
      },
      options: {
        scales: {
          xAxes: [{ type: 'time' }]
        }
      }
    };

    if (this.state.chart) {
      this.state.chart.destroy();
    }

    const { classes } = this.props;
    const canvas = document.getElementsByClassName(classes.canvas)[0];
    this.state.chart = new ChartJs(canvas.getContext('2d'), args);
  }
}

Chart.propTypes = {
  data: PropTypes.array.isRequired,
  label: PropTypes.string.isRequired
};

export default withStyles(styles)(Chart);
