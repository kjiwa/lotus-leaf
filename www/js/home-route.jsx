import Card, { CardContent, CardHeader } from 'material-ui/Card';
import ChartOptions from './chart-options.jsx';
import ExpandMoreIcon from 'material-ui-icons/ExpandMore';
import ExpansionPanel, { ExpansionPanelDetails, ExpansionPanelSummary } from 'material-ui/ExpansionPanel';
import IconButton from 'material-ui/IconButton';
import PropTypes from 'prop-types';
import React from 'react';
import { Topic } from './model.js';
import Typography from 'material-ui/Typography';

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
    return (
      <Card>
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
              onTopicChange={this.handleSelectedTopicChange.bind(this)} />
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
          return new Topic(e[0], e[1]);
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

  handleSelectedTopicChange(event, topicId) {
    this.setState({ selectedTopicId: topicId });
  }
}

HomeRoute.propTypes = {
};

export default HomeRoute;
