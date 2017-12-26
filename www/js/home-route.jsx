import Card, { CardContent, CardHeader } from 'material-ui/Card';
import ChartOptions from './chart-options.jsx';
import ExpandMoreIcon from 'material-ui-icons/ExpandMore';
import ExpansionPanel, { ExpansionPanelDetails, ExpansionPanelSummary } from 'material-ui/ExpansionPanel';
import IconButton from 'material-ui/IconButton';
import React from 'react';
import { Topic } from './model.js';
import Typography from 'material-ui/Typography';

class HomeRoute extends React.Component {
  constructor(props) {
    super(props);
    this.state = { topics: [] };
  }

  componentDidMount() {
    fetch('/_/topics')
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        const topics = data.map((e) => {
          return new Topic(e[0], e[1]);
        });
        this.setState({ topics: topics });
      });
  }

  render() {
    return (
      <Card>
        <ExpansionPanel defaultExpanded={true}>
          <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
            <Typography type="subheading">Chart Options</Typography>
          </ExpansionPanelSummary>
          <ExpansionPanelDetails>
            <ChartOptions topics={this.state.topics} />
          </ExpansionPanelDetails>
        </ExpansionPanel>
      </Card>
    );
  }
}

export default HomeRoute;
