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
      endDatePickerFocused: false
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
            <InputLabel className={classes.dateInputLabel}>
              <Typography type="caption">Start Date</Typography>
            </InputLabel>
            <SingleDatePicker
              date={this.props.startDateTime}
              focused={this.state.startDatePickerFocused}
              onDateChange={this.props.onStartDateChange}
              onFocusChange={this.handleStartDateFocusChange.bind(this)}
              initialVisibleMonth={() => this.props.startDateTime}
              isOutsideRange={(moment) => false} />
          </div>
          <div className={classes.row}>
            <InputLabel className={classes.dateInputLabel}>
              <Typography type="caption">End Date</Typography>
            </InputLabel>
            <SingleDatePicker
              date={this.props.endDateTime}
              focused={this.state.endDatePickerFocused}
              onDateChange={this.props.onEndDateChange}
              onFocusChange={this.handleEndDateFocusChange.bind(this)}
              initialVisibleMonth={() => this.props.endDateTime}
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
}

ChartOptions.propTypes = {
  topics: PropTypes.array.isRequired,
  selectedTopicId: PropTypes.number.isRequired,
  startDateTime: PropTypes.instanceOf(Moment).isRequired,
  endDateTime: PropTypes.instanceOf(Moment).isRequired,
  sampleGranularities: PropTypes.array.isRequired,
  selectedSampleGranularity: PropTypes.string.isRequired,
  onTopicChange: PropTypes.func.isRequired,
  onStartDateChange: PropTypes.func.isRequired,
  onEndDateChange: PropTypes.func.isRequired,
  onSampleGranularityChange: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired
};

export default withStyles(styles)(ChartOptions);
