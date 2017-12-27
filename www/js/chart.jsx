import ChartJs from 'chart.js';
import PropTypes from 'prop-types';
import React from 'react';
import uuid4 from 'uuid/v4';
import { withStyles } from 'material-ui/styles';

const styles = (theme) => {
  canvas: {
  }
};

class Chart extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      canvasId: 'uwsolar-chart-' + uuid4()
    };
  }

  componentDidUpdate() {
    const { classes } = this.props;
    const canvas = document.getElementsByClassName(classes.canvas)[0];

    const args = {
      type: 'scatter',
      data: { datasets: [{ data: this.props.data }] },
      options: { scales: { xAxes: [{ type: 'linear', position: 'bottom' }] } }
    };

    new ChartJs(canvas.getContext('2d'), args);
  }

  render() {
    const { classes } = this.props;
    return <canvas className={classes.canvas} />;
  }
}

Chart.propTypes = {
  data: PropTypes.array.isRequired
};

export default withStyles(styles)(Chart);
