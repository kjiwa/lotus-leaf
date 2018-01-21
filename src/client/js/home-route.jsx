/**
 * A route component that queries and displays time-series data.
 */

import Card, { CardContent, CardHeader } from 'material-ui/Card';
import Chart from './chart.jsx';
import ChartOptions from './chart-options.jsx';
import ExpandMoreIcon from 'material-ui-icons/ExpandMore';
import ExpansionPanel, { ExpansionPanelDetails, ExpansionPanelSummary } from 'material-ui/ExpansionPanel';
import IconButton from 'material-ui/IconButton';
import Moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';
import Typography from 'material-ui/Typography';
import { Datum, Topic } from './model.js';
import { LinearProgress } from 'material-ui/Progress';
import { withStyles } from 'material-ui/styles';

const styles = (theme) => ({
  chartCard: {
    marginTop: '32px'
  },
  linearProgress: {
    left: '0',
    position: 'absolute',
    top: '100px',
    width: '100%'
  }
});

class HomeRoute extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      // The start date and time of the query.
      startDateTime: new Moment(),

      // The end date and time of the query.
      endDateTime: new Moment(),

      // A list of known topics.
      topics: [],

      // The currently selected topics.
      selectedTopicIds: [],

      // The currently displayed data, grouped by topic.
      data: {},

      // The currently selected sample rate.
      selectedSampleRate: 0.05,

      // Whether the progress indicator should be shown.
      showProgressIndicator: false
    };
  }

  /**
   * Performs post-render tasks after properties updates.
   * @returns {undefined}
   */
  componentDidMount() {
    this.fetchTopics();
    this.fetchEarliestTimestamp();
    this.fetchLatestTimestamp();
  }

  /**
   * Renders the home route view.
   * @returns {Object} A rendered JSX element.
   */
  render() {
    const { classes } = this.props;

    let chart = null;
    if (this.state.data.length > 0) {
      chart = (
        <Card className={classes.chartCard}>
          <CardHeader title="Chart" />
          <CardContent>
            <Chart data={this.state.data} topics={this.state.topics} />
          </CardContent>
        </Card>
      );
    }

    return (
      <div>
        {this.state.showProgressIndicator && <LinearProgress mode="query" className={classes.linearProgress} />}
        <ExpansionPanel defaultExpanded={true}>
          <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
            <Typography type="headline">Chart Options</Typography>
          </ExpansionPanelSummary>
          <ExpansionPanelDetails>
            <ChartOptions
              topics={this.state.topics}
              selectedTopicIds={this.state.selectedTopicIds}
              startDateTime={this.state.startDateTime}
              endDateTime={this.state.endDateTime}
              selectedSampleRate={this.state.selectedSampleRate}
              onTopicChange={this.handleSelectedTopicChange.bind(this)}
              onStartDateTimeChange={this.handleStartDateTimeChange.bind(this)}
              onEndDateTimeChange={this.handleEndDateTimeChange.bind(this)}
              onSampleRateChange={this.handleSampleRateChange.bind(this)}
              onSubmit={this.handleOptionsSubmit.bind(this)} />
          </ExpansionPanelDetails>
        </ExpansionPanel>
        {chart}
      </div>
    );
  }

  /**
   * Fetches topics from the backend.
   * @returns {undefined}
   */
  fetchTopics() {
    fetch('/_/topics')
      .then((response) => response.json())
      .then((data) => {
        const topics = data.map((e) => (new Topic(e[0], e[1])));
        this.setState({
          topics: topics,
          selectedTopicId: (topics.length > 0 ? topics[0].topicId : 0)
        });
      });
  }

  /**
   * Fetches the earliest data timestamp from the backend.
   * @returns {undefined}
   */
  fetchEarliestTimestamp() {
    fetch('/_/data/timestamp/earliest')
      .then((response) => response.json())
      .then((data) => {
        this.setState({ startDateTime: new Moment(data) });
      });
  }

  /**
   * Fetches the latest data timestamp from the backend.
   * @returns {undefined}
   */
  fetchLatestTimestamp() {
    fetch('/_/data/timestamp/latest')
      .then((response) => response.json())
      .then((data) => {
        this.setState({ endDateTime: new Moment(data) });
      });
  }

  /**
   * Fetches data to be displayed in the chart.
   * @returns {undefined}
   */
  fetchData() {
    this.setState({ showProgressIndicator: true });

    const params = new URLSearchParams();
    params.set('start_date_time', this.state.startDateTime.toISOString());
    params.set('end_date_time', this.state.endDateTime.toISOString());
    params.set('sample_rate', this.state.selectedSampleRate);
    params.set('topic_ids', this.state.selectedTopicIds);

    fetch('/_/data?' + params.toString())
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          data: data.map((e) => (new Datum(new Moment(e[0]), parseInt(e[1], 10), e[2]))),
          showProgressIndicator: false
        });
      });
  }

  /**
   * Handles changes to the topic selection field.
   * @param {Object} event The change event.
   * @returns {undefined}
   */
  handleSelectedTopicChange(event) {
    this.setState({ selectedTopicIds: event.target.value });
  }

  /**
   * Handles changes to the start date and time field.
   * @param {Moment} date The new start date and time.
   * @returns {undefined}
   */
  handleStartDateTimeChange(date) {
    this.setState({ startDateTime: date });
  }

  /**
   * Handles changes to the end date and time field.
   * @param {Moment} date The new end date and time.
   * @returns {undefined}
   */
  handleEndDateTimeChange(date) {
    this.setState({ endDateTime: date });
  }

  /**
   * Handles changes to the sample rate field.
   * @param {number} value The new sample rate.
   * @returns {undefined}
   */
  handleSampleRateChange(value) {
    this.setState({ selectedSampleRate: value });
  }

  /**
   * Handles submissions of the chart options component.
   * @returns {undefined}
   */
  handleOptionsSubmit() {
    this.fetchData();
  }
}

HomeRoute.propTypes = {
};

export default withStyles(styles)(HomeRoute);
