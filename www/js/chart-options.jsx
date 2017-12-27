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
  sampleGranularitySelect: {
    width: '200px'
  },
  topicSelect: {
    width: '600px'
  }
});

class ChartOptions extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      focusedInput: null,
      sampleGranularityFieldError: false
    };
  }

  render() {
    const { classes } = this.props;
    const topicMenuItems = this.props.topics.map((e) => (
      <MenuItem key={e['topic_id']} value={e['topic_id']}>{e['topic_name']}</MenuItem>
    ));

    const sampleGranularityMenuItems = this.props.sampleGranularities.map((e) => (
      <MenuItem key={e} value={e}>{e}</MenuItem>
    ));

    return (
      <div>
        <form>
          <div className={classes.row}>
            <FormControl>
              <InputLabel>Topic</InputLabel>
              <Select
                className={classes.topicSelect}
                value={this.props.selectedTopicId}
                onChange={this.props.onTopicChange}>
                {topicMenuItems}
              </Select>
            </FormControl>
          </div>
          <div className={classes.row}>
            <InputLabel className={classes.dateRangeInputLabel}>Date Range</InputLabel>
            <DateRangePicker
              initialVisibleMonth={() => this.props.startDateTime}
              startDate={this.props.startDateTime}
              endDate={this.props.endDateTime}
              focusedInput={this.state.focusedInput}
              onDatesChange={this.props.onDatesChange}
              onFocusChange={this.handleFocusChange.bind(this)}
              startDateId="start_date"
              endDateId="end_date"
              isOutsideRange={(moment) => false} />
          </div>
          <div className={classes.row}>
            <FormControl>
              <InputLabel>Sample Granularity</InputLabel>
              <Select
                className={classes.sampleGranularitySelect}
                value={this.props.selectedSampleGranularity}
                onChange={this.props.onSampleGranularityChange}>
                {sampleGranularityMenuItems}
              </Select>
            </FormControl>
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
  startDateTime: PropTypes.instanceOf(Moment).isRequired,
  endDateTime: PropTypes.instanceOf(Moment).isRequired,
  sampleGranularities: PropTypes.array.isRequired,
  selectedSampleGranularity: PropTypes.string.isRequired,
  onTopicChange: PropTypes.func.isRequired,
  onDatesChange: PropTypes.func.isRequired,
  onSampleGranularityChange: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired
};

export default withStyles(styles)(ChartOptions);
