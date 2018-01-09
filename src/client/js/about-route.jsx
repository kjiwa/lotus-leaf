/**
 * A route that displays information about the UW Solar Power Monitor.
 */

import AccountCircleIcon from 'material-ui-icons/AccountCircle';
import Avatar from 'material-ui/Avatar';
import Card, { CardContent, CardHeader } from 'material-ui/Card';
import List, { ListItem, ListItemText } from 'material-ui/List';
import PropTypes from 'prop-types';
import React from 'react';
import Typography from 'material-ui/Typography';

class AboutRoute extends React.Component {
  /**
   * Renders the about route.
   * @returns {undefined}
   */
  render() {
    return (
      <Card>
        <CardHeader title="About the UW Solar Power Monitor" />
        <CardContent>
          <Typography>This project was created under the supervision of Professor Daniel Kirschen.</Typography>
        </CardContent>
        <CardContent>
          <Typography type="subheading">Authors</Typography>
          <List>
            <ListItem>
              <Avatar><AccountCircleIcon/></Avatar>
              <ListItemText
                primary="Yuxuan Chen"
                secondary="yuxuan7@uw.edu" />
            </ListItem>
            <ListItem>
              <Avatar><AccountCircleIcon/></Avatar>
              <ListItemText
                primary="Nathan Hills"
                secondary="hillsn@uw.edu" />
            </ListItem>
            <ListItem>
              <Avatar><AccountCircleIcon/></Avatar>
              <ListItemText
                primary="Kamil Jiwa"
                secondary="kjiwa@uw.edu" />
            </ListItem>
            <ListItem>
              <Avatar><AccountCircleIcon/></Avatar>
              <ListItemText
                primary="Jordan Wollenman"
                secondary="wollej@uw.edu" />
            </ListItem>
          </List>
        </CardContent>
      </Card>
    );
  }
}

AboutRoute.propTypes = {
};

export default AboutRoute;
