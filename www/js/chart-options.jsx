import PropTypes from 'prop-types';
import React from 'react';
import Select from 'material-ui/Select';
import TextField from 'material-ui/TextField';
import Typography from 'material-ui/Typography';
import { FormControl } from 'material-ui/Form';
import { InputLabel } from 'material-ui/Input';
import { MenuItem } from 'material-ui/Menu';
import { withStyles } from 'material-ui/styles';

const styles = (theme) => ({
  row: {
    margin: '16px 0'
  },
  select: {
    width: '600px'
  }
});

class ChartOptions extends React.Component {
  render() {
    const { classes } = this.props;

    const topicMenuItems = this.props.topics.map((e) => {
      return <MenuItem key={e.id} value={e.id}>{e.name}</MenuItem>;
    });

    return (
      <div>
        <form>
          <div className={classes.row}>
            <FormControl>
              <InputLabel>Topic</InputLabel>
              <Select
                className={classes.select}
                value={this.props.selectedTopicId}
                onChange={this.handleSelectChange.bind(this)}>
                {topicMenuItems}
              </Select>
            </FormControl>
          </div>
          <div className={classes.row}>
            <InputLabel>Date Range</InputLabel>
          </div>
        </form>
      </div>
    );
  }

  handleSelectChange(event) {
    this.props.onTopicChange(event, event.target.value);
  }
}

ChartOptions.propTypes = {
  topics: PropTypes.array.isRequired,
  selectedTopicId: PropTypes.number.isRequired,
  startDateTime: PropTypes.instanceOf(Date).isRequired,
  endDateTime: PropTypes.instanceOf(Date).isRequired,
  onTopicChange: PropTypes.func.isRequired
};

export default withStyles(styles)(ChartOptions);
