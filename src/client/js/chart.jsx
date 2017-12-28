import ChartJs from 'chart.js';
import Moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';
import uuid4 from 'uuid/v4';
import { withStyles } from 'material-ui/styles';

const styles = (theme) => ({ canvas: {} });

class Chart extends React.Component {
  componentDidMount() {
    this.refreshChart();
  }

  componentDidUpdate() {
    this.refreshChart();
  }

  render() {
    const { classes } = this.props;
    return <canvas className={classes.canvas} />;
  }

  refreshChart() {
    const { classes } = this.props;
    const canvas = document.getElementsByClassName(classes.canvas)[0];

    // TODO(kjiwa): Put this into a worker thread.
    const data = this.props.data.map((e) => ({
      x: new Moment(e['ts']),
      y: parseFloat(e['value_string'])
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

    new ChartJs(canvas.getContext('2d'), args);
  }
}

Chart.propTypes = {
  data: PropTypes.array.isRequired,
  label: PropTypes.string.isRequired
};

export default withStyles(styles)(Chart);
