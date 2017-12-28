/**
 * A component containing chart options.
 *
 * The component displays the following options:
 *   - topic
 *   - start date and time
 *   - end date and time
 *   - sample granularity
 */

import Button from 'material-ui/Button';
import Grid from 'material-ui/Grid';
import Moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';
import Select from 'material-ui/Select';
import TextField from 'material-ui/TextField';
import Typography from 'material-ui/Typography';
import { FormControl } from 'material-ui/Form';
import { InputLabel } from 'material-ui/Input';
import { MenuItem } from 'material-ui/Menu';
import { SingleDatePicker } from 'react-dates';
import { withStyles } from 'material-ui/styles';

const styles = (theme) => ({
  dateInputLabel: {
    display: 'block',
    marginBottom: '8px'
  },
  sampleGranularitySelect: {
    width: '200px'
  },
  topicSelect: {
    width: '600px'
  }
});

class ChartOptions extends React.Component {
  /**
   * Creates a new ChartOptions component.
   * @param {Object} props The component's properties.
   */
  constructor(props) {
    super(props);
    this.state = {
      // Whether the start date SingleDatePicker is focused.
      startDatePickerFocused: false,

      // Whether the end date SingleDatePicker is focused.
      endDatePickerFocused: false,

      // Whether there is an error in the start time text field.
      startTimeFieldError: false,

      // Whether there is an error in the end time text field.
      endTimeFieldError: false
    };
  }

  /**
   * Renders the component.
   * @returns {Object} A rendered JSX element.
   */
  render() {
    const { classes } = this.props;

    // Create topic menu items.
    const topicMenuItems = this.props.topics.map((e) => (
      <MenuItem key={e['topic_id']} value={e['topic_id']}>{e['topic_name']}</MenuItem>
    ));

    // Create sample granularity menu items.
    const sampleGranularityMenuItems = this.props.sampleGranularities.map((e) => (
      <MenuItem key={e} value={e}>{e}</MenuItem>
    ));

    return (
      <div>
        <form>
          <Grid container alignItems="flex-start">
            <Grid xs={12} item>
              <FormControl>
                <InputLabel>Topic</InputLabel>
                <Select
                  className={classes.topicSelect}
                  value={this.props.selectedTopicId}
                  onChange={this.props.onTopicChange}>
                  {topicMenuItems}
                </Select>
              </FormControl>
            </Grid>
            <Grid xs={1} item>
              <InputLabel className={classes.dateInputLabel}>
                <Typography type="caption">Start Date</Typography>
              </InputLabel>
              <SingleDatePicker
                date={this.props.startDateTime}
                focused={this.state.startDatePickerFocused}
                onDateChange={this.handleStartDateChange.bind(this)}
                onFocusChange={this.handleStartDateFocusChange.bind(this)}
                initialVisibleMonth={() => this.props.startDateTime}
                isOutsideRange={(moment) => false}
                small={true} />
            </Grid>
            <Grid xs={11} item key={'start-time-' + this.props.startDateTime}>
              <InputLabel className={classes.dateInputLabel}>
                <Typography type="caption">Start Time</Typography>
              </InputLabel>
              <TextField
                className={classes.startTimeTextField}
                defaultValue={this.props.startDateTime.format('HH:mm:ss.SSS')}
                onChange={this.handleStartTimeChange.bind(this)}
                error={this.state.startTimeFieldError} />
            </Grid>
            <Grid xs={1} item>
              <InputLabel className={classes.dateInputLabel}>
                <Typography type="caption">End Date</Typography>
              </InputLabel>
              <SingleDatePicker
                date={this.props.endDateTime}
                focused={this.state.endDatePickerFocused}
                onDateChange={this.handleEndDateChange.bind(this)}
                onFocusChange={this.handleEndDateFocusChange.bind(this)}
                initialVisibleMonth={() => this.props.endDateTime}
                isOutsideRange={(moment) => false}
                small={true} />
            </Grid>
            <Grid xs={11} item key={'end-time-' + this.props.endDateTime}>
              <InputLabel className={classes.dateInputLabel}>
                <Typography type="caption">End Time</Typography>
              </InputLabel>
              <TextField
                className={classes.endTimeTextField}
                defaultValue={this.props.endDateTime.format('HH:mm:ss.SSS')}
                onChange={this.handleEndTimeChange.bind(this)}
                error={this.state.endTimeFieldError} />
            </Grid>
            <Grid xs={12} item>
              <FormControl>
                <InputLabel>Sample Granularity</InputLabel>
                <Select
                  className={classes.sampleGranularitySelect}
                  value={this.props.selectedSampleGranularity}
                  onChange={this.props.onSampleGranularityChange}>
                  {sampleGranularityMenuItems}
                </Select>
              </FormControl>
            </Grid>
            <Grid xs={12} item>
              <Button
                raised
                color="primary"
                onClick={this.props.onSubmit.bind(this)}>
                Submit
              </Button>
            </Grid>
          </Grid>
        </form>
      </div>
    );
  }

  /**
   * Handles changes to the start date component's focused input.
   * @param {boolean} focused the currently focused input.
   * @returns {undefined}
   */
  handleStartDateFocusChange({ focused }) {
    this.setState({ startDatePickerFocused: focused });
  }

  /**
   * Handles changes to the end date component's focused input.
   * @param {boolean} focused the currently focused input.
   * @returns {undefined}
   */
  handleEndDateFocusChange({ focused }) {
    this.setState({ endDatePickerFocused: focused });
  }

  /**
   * Handles changes to the start date component.
   * @param {Moment} date The new start date.
   * @returns {undefined}
   */
  handleStartDateChange(date) {
    // Merge time into the date.
    date.hours(this.props.startDateTime.hours());
    date.minutes(this.props.startDateTime.minutes());
    date.seconds(this.props.startDateTime.seconds());
    date.milliseconds(this.props.startDateTime.milliseconds());
    this.props.onStartDateTimeChange(date);
  }

  /**
   * Handles changes to the end date component.
   * @param {Moment} date The new end date.
   * @returns {undefined}
   */
  handleEndDateChange(date) {
    // Merge time into the date.
    date.hours(this.props.endDateTime.hours());
    date.minutes(this.props.endDateTime.minutes());
    date.seconds(this.props.endDateTime.seconds());
    date.milliseconds(this.props.endDateTime.milliseconds());
    this.props.onEndDateTimeChange(date);
  }

  /**
   * Handles changes to the start time component.
   * @param {Object} event The event object
   * @returns {undefined}
   */
  handleStartTimeChange(event) {
    const moment = new Moment('1970-01-01T' + event.target.value);
    if (!moment.isValid()) {
      this.setState({ startTimeFieldError: true  });
      return;
    }

    this.setState({ startTimeFieldError: false });

    const dt = this.props.startDateTime;
    dt.hours(moment.hours());
    dt.minutes(moment.minutes());
    dt.seconds(moment.seconds());
    dt.milliseconds(moment.milliseconds());
    this.props.onStartDateTimeChange(dt);
  }

  /**
   * Handles changes to the end time component.
   * @param {Object} event The event object
   * @returns {undefined}
   */
  handleEndTimeChange(event) {
    const moment = new Moment('1970-01-01T' + event.target.value);
    if (!moment.isValid()) {
      this.setState({ endTimeFieldError: true  });
      return;
    }

    this.setState({ endTimeFieldError: false });

    const dt = this.props.endDateTime;
    dt.hours(moment.hours());
    dt.minutes(moment.minutes());
    dt.seconds(moment.seconds());
    dt.milliseconds(moment.milliseconds());
    this.props.onEndDateTimeChange(dt);
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
  onStartDateTimeChange: PropTypes.func.isRequired,
  onEndDateTimeChange: PropTypes.func.isRequired,
  onSampleGranularityChange: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired
};

export default withStyles(styles)(ChartOptions);
