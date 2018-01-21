/**
 * A component containing chart options.
 *
 * The component displays the following options:
 *   - topic
 *   - start date and time
 *   - end date and time
 *   - sample rate
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
import { withStyles } from 'material-ui/styles';

const styles = (theme) => ({
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
      // Whether there is an error in the start time text field.
      startDateTimeFieldError: false,

      // Whether there is an error in the end time text field.
      endDateTimeFieldError: false,

      // Whether there is an error in the sample rate text field.
      sampleRateFieldError: false
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
      <MenuItem key={e.topicId} value={e.topicId}>{e.topicName}</MenuItem>
    ));

    return (
      <div>
        <form>
          <Grid container alignItems="flex-start">
            <Grid xs={12} item>
              <FormControl>
                <InputLabel>Topic</InputLabel>
                <Select
                  multiple
                  className={classes.topicSelect}
                  value={this.props.selectedTopicIds}
                  onChange={this.props.onTopicChange}>
                  {topicMenuItems}
                </Select>
              </FormControl>
            </Grid>
            <Grid xs={12} item key={'start-date-time=' + this.props.startDateTime.milliseconds()}>
              <FormControl>
                <TextField
                  label="Start Date and Time"
                  type="datetime-local"
                  defaultValue={this.props.startDateTime.format('YYYY-MM-DD[T]HH:mm:ss.SSS')}
                  onChange={this.handleStartDateTimeChange.bind(this)}
                  InputLabelProps={{ shrink: true }} />
              </FormControl>
            </Grid>
            <Grid xs={12} item key={'end-date-time=' + this.props.endDateTime.milliseconds()}>
              <FormControl>
                <TextField
                  label="End Date and Time"
                  type="datetime-local"
                  defaultValue={this.props.endDateTime.format('YYYY-MM-DD[T]HH:mm:ss.SSS')}
                  onChange={this.handleEndDateTimeChange.bind(this)}
                  InputLabelProps={{ shrink: true }} />
              </FormControl>
            </Grid>
            <Grid xs={12} item>
              <FormControl>
                <TextField
                  label="Sample Rate"
                  defaultValue={this.props.selectedSampleRate.toString()}
                  onChange={this.handleSampleRateChange.bind(this)}
                  error={this.state.sampleRateFieldError} />
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
   * Handles changes to the start date component.
   * @param {Object} event The change event.
   * @returns {undefined}
   */
  handleStartDateTimeChange(event) {
    const value = new Moment(event.target.value);
    if (!value.isValid()) {
      this.setState({ startDateTimeFieldError: true });
      return;
    }

    this.setState({ startDateTimeFieldError: false });
    this.props.onStartDateTimeChange(value);
  }

  /**
   * Handles changes to the end date component.
   * @param {Object} event The change event.
   * @returns {undefined}
   */
  handleEndDateTimeChange(event) {
    const value = new Moment(event.target.value);
    if (!value.isValid()) {
      this.setState({ endDateTimeFieldError: true });
      return;
    }

    this.setState({ endDateTimeFieldError: false });
    this.props.onEndDateTimeChange(value);
  }

  /**
   * Handles changes to the sample rate.
   * @param {Object} event The change event.
   * @returns {undefined}
   */
  handleSampleRateChange(event) {
    // Check that the sample rate value is a number.
    let value = event.target.value;
    if (!/^(\-|\+)?([0-9]+(\.[0-9]+)?|Infinity)$/.test(value)) {
      this.setState({ sampleRateFieldError: true });
      return;
    }

    // Check that the sample rate is in the range [0, 1].
    value = parseFloat(value);
    if (value < 0 || value > 1) {
      this.setState({ sampleRateFieldError: true });
      return;
    }

    this.setState({ sampleRateFieldError: false });
    this.props.onSampleRateChange(value);
  }
}

ChartOptions.propTypes = {
  topics: PropTypes.array.isRequired,
  selectedTopicIds: PropTypes.array.isRequired,
  startDateTime: PropTypes.instanceOf(Moment).isRequired,
  endDateTime: PropTypes.instanceOf(Moment).isRequired,
  selectedSampleRate: PropTypes.number.isRequired,
  onTopicChange: PropTypes.func.isRequired,
  onStartDateTimeChange: PropTypes.func.isRequired,
  onEndDateTimeChange: PropTypes.func.isRequired,
  onSampleRateChange: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired
};

export default withStyles(styles)(ChartOptions);
