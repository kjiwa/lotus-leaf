import Card, { CardContent, CardHeader } from 'material-ui/Card';
import ChartOptions from './chart-options.jsx';
import ExpandMoreIcon from 'material-ui-icons/ExpandMore';
import ExpansionPanel, { ExpansionPanelDetails, ExpansionPanelSummary } from 'material-ui/ExpansionPanel';
import IconButton from 'material-ui/IconButton';
import PropTypes from 'prop-types';
import React from 'react';
import Typography from 'material-ui/Typography';
import { Topic } from './model.js';
import { withStyles } from 'material-ui/styles';

const styles = (theme) => ({
  card: {
    overflow: 'visible'
  }
});

class HomeRoute extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      startDateTime: new Date(),
      endDateTime: new Date(),
      topics: [],
      selectedTopicId: 0
    };
  }

  componentDidMount() {
    this.fetchTopics();
    this.fetchEarliestTimestamp();
    this.fetchLatestTimestamp();
  }

  render() {
    const { classes } = this.props;
    return (
      <Card className={classes.card}>
        <ExpansionPanel defaultExpanded={true}>
          <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
            <Typography type="subheading">Chart Options</Typography>
          </ExpansionPanelSummary>
          <ExpansionPanelDetails>
            <ChartOptions
              topics={this.state.topics}
              selectedTopicId={this.state.selectedTopicId}
              startDateTime={this.state.startDateTime}
              endDateTime={this.state.endDateTime}
              onTopicChange={this.handleSelectedTopicChange.bind(this)}
              onDatesChange={this.handleDatesChange.bind(this)}/>
          </ExpansionPanelDetails>
        </ExpansionPanel>
      </Card>
    );
  }

  fetchTopics() {
    fetch('/_/topics')
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        const topics = data.map((e) => {
          return new Topic(e['id'], e['name']);
        });

        let selectedTopicId = 0;
        if (topics.length > 0) {
          selectedTopicId = topics[0].id;
        }

        this.setState({
          topics: topics,
          selectedTopicId: selectedTopicId
        });
      });
  }

  fetchEarliestTimestamp() {
    fetch('/_/data/timestamp/earliest')
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        this.setState({ startDateTime: new Date(Date.parse(data)) });
      });
  }

  fetchLatestTimestamp() {
    fetch('/_/data/timestamp/latest')
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        this.setState({ endDateTime: new Date(Date.parse(data)) });
      });
  }

  handleSelectedTopicChange(event) {
    this.setState({ selectedTopicId: event.target.value });
  }

  handleDatesChange(event) {
    const dates = {};
    if (event.startDate) {
      dates.startDateTime = event.startDate.toDate();
    }

    if (event.endDate) {
      dates.endDateTime = event.endDate.toDate();
    }

    this.setState(dates);
  }
}

HomeRoute.propTypes = {
};

export default withStyles(styles)(HomeRoute);
