import Button from 'material-ui/Button';
import Moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';
import Select from 'material-ui/Select';
import TextField from 'material-ui/TextField';
import Typography from 'material-ui/Typography';
import { DateRangePicker } from 'react-dates';
import { FormControl } from 'material-ui/Form';
import { InputLabel } from 'material-ui/Input';
import { MenuItem } from 'material-ui/Menu';
import { withStyles } from 'material-ui/styles';

const styles = (theme) => ({
  dateRangeInputLabel: {
    display: 'block',
    marginBottom: '8px'
  },
  row: {
    margin: '16px 0'
  },
  select: {
    width: '600px'
  }
});

class ChartOptions extends React.Component {
  constructor(props) {
    super(props);
    this.state = { focusedInput: null };
  }

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
                onChange={this.props.onTopicChange}>
                {topicMenuItems}
              </Select>
            </FormControl>
          </div>
          <div className={classes.row}>
            <InputLabel className={classes.dateRangeInputLabel}>Date Range</InputLabel>
            <DateRangePicker
              initialVisibleMonth={() => new Moment(this.props.startDateTime)}
              startDate={new Moment(this.props.startDateTime)}
              endDate={new Moment(this.props.endDateTime)}
              focusedInput={this.state.focusedInput}
              onDatesChange={this.props.onDatesChange}
              onFocusChange={this.handleFocusChange.bind(this)}
              startDateId="start_date"
              endDateId="end_date"
              isOutsideRange={(date) => date.isBefore(this.props.startDateTime)} />
          </div>
          <div className={classes.row}>
            <Button
              raised
              color="primary"
              onClick={this.props.onSubmit.bind(this)}>
              Submit
            </Button>
          </div>
        </form>
      </div>
    );
  }

  handleFocusChange(focusedInput) {
    this.setState({ focusedInput: focusedInput });
  }
}

ChartOptions.propTypes = {
  topics: PropTypes.array.isRequired,
  selectedTopicId: PropTypes.number.isRequired,
  startDateTime: PropTypes.instanceOf(Date).isRequired,
  endDateTime: PropTypes.instanceOf(Date).isRequired,
  onDatesChange: PropTypes.func.isRequired,
  onTopicChange: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired
};

export default withStyles(styles)(ChartOptions);
