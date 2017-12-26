import Card, { CardContent, CardHeader } from 'material-ui/Card';
import ExpandMoreIcon from 'material-ui-icons/ExpandMore';
import ExpansionPanel, { ExpansionPanelDetails, ExpansionPanelSummary } from 'material-ui/ExpansionPanel';
import IconButton from 'material-ui/IconButton';
import React from 'react';
import Typography from 'material-ui/Typography';
import { withStyles} from 'material-ui/styles';

const styles = (theme) => ({});

class HomeRoute extends React.Component {
  render() {
    const { classes } = this.props;
    return (
      <Card>
        <ExpansionPanel defaultExpanded={true}>
          <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
            <Typography type="subheading">Chart Options</Typography>
          </ExpansionPanelSummary>
          <ExpansionPanelDetails>
            <Typography>Lorem ipsum dolor sit amet.</Typography>
          </ExpansionPanelDetails>
        </ExpansionPanel>
      </Card>
    );
  }
}

export default withStyles(styles)(HomeRoute);
