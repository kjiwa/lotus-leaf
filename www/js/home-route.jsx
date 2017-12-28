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
import { withStyles } from 'material-ui/styles';

const SAMPLE_GRANULARITIES = [
  'year',
  'month',
  'date',
  'hour',
  'minute',
  'second',
  'millisecond'
];

const styles = (theme) => ({
  chartOptionsCard: {
    overflow: 'visible'
  },
  chartCard: {
    marginTop: '32px'
  }
});

class HomeRoute extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      startDateTime: new Moment(),
      endDateTime: new Moment(),
      topics: [],
      selectedTopicId: 0,
      data: [],
      selectedSampleGranularity: 'hour'
    };
  }

  componentDidMount() {
    this.fetchTopics();
    this.fetchEarliestTimestamp();
    this.fetchLatestTimestamp();
  }

  render() {
    const { classes } = this.props;

    let chart = null;
    if (this.state.data.length > 0) {
      const selectedTopic = this.state.topics.find((e) => (
        e['topic_id'] == this.state.selectedTopicId
      ));

      chart = (
        <Card className={classes.chartCard}>
          <CardHeader title="Chart" />
          <CardContent>
            <Chart
              data={this.state.data}
              label={selectedTopic['topic_name']} />
          </CardContent>
        </Card>
      );
    }

    return (
      <div>
        <ExpansionPanel defaultExpanded={true}>
          <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
            <Typography type="headline">Chart Options</Typography>
          </ExpansionPanelSummary>
          <ExpansionPanelDetails>
            <ChartOptions
              topics={this.state.topics}
              selectedTopicId={this.state.selectedTopicId}
              startDateTime={this.state.startDateTime}
              endDateTime={this.state.endDateTime}
              sampleGranularities={SAMPLE_GRANULARITIES}
              selectedSampleGranularity={this.state.selectedSampleGranularity}
              onTopicChange={this.handleSelectedTopicChange.bind(this)}
              onDatesChange={this.handleDatesChange.bind(this)}
              onSampleGranularityChange={this.handleSampleGranularityChange.bind(this)}
              onSubmit={this.handleOptionsSubmit.bind(this)} />
          </ExpansionPanelDetails>
        </ExpansionPanel>
        {chart}
      </div>
    );
  }

  fetchTopics() {
    fetch('/_/topics')
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          topics: data,
          selectedTopicId: (data.length > 0 ? data[0]['topic_id'] : 0)
        });
      });
  }

  fetchEarliestTimestamp() {
    fetch('/_/data/timestamp/earliest')
      .then((response) => response.json())
      .then((data) => {
        this.setState({ startDateTime: new Moment(data) });
      });
  }

  fetchLatestTimestamp() {
    fetch('/_/data/timestamp/latest')
      .then((response) => response.json())
      .then((data) => {
        this.setState({ endDateTime: new Moment(data) });
      });
  }

  fetchData() {
    const params = new URLSearchParams();
    params.set('topic_id', this.state.selectedTopicId);
    params.set('start_date_time', this.state.startDateTime.toISOString());
    params.set('end_date_time', this.state.endDateTime.toISOString());

    fetch('/_/data?' + params.toString())
      .then((response) => response.json())
      .then((data) => {
        this.setState({ data: this.getSamples(data, this.state.selectedSampleGranularity) });
      });
  }

  handleSelectedTopicChange(event) {
    this.setState({ selectedTopicId: event.target.value });
  }

  handleDatesChange(event) {
    const dates = {};
    if (event.startDate) {
      dates.startDateTime = event.startDate;
    }

    if (event.endDate) {
      dates.endDateTime = event.endDate;
    }

    this.setState(dates);
  }

  handleSampleGranularityChange(event) {
    this.setState({ selectedSampleGranularity: event.target.value });
  }

  handleOptionsSubmit() {
    this.fetchData();
  }

  getSamples(data, sampleGranularity) {
    if (data.length == 0) {
      return [];
    }

    const samples = [data[0]];
    let ts = samples[0]['ts'];
    for (let i = 1, j = data.length; i < j; ++i) {
      const now = new Moment(data[i]['ts']);
      if (now.isSameOrBefore(ts, sampleGranularity)) {
        continue;
      }

      samples.push(data[i]);
      ts = now;
    }

    return samples;
  }
}

HomeRoute.propTypes = {
};

export default withStyles(styles)(HomeRoute);
