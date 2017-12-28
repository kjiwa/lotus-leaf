import AppBar from 'material-ui/AppBar';
import PropTypes from 'prop-types';
import React from 'react';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import uwBlockWLogo from '../img/uw-block-w-logo.png';
import { withStyles } from 'material-ui/styles';

const styles = (theme) => ({
  uwBlockWLogo: {
    height: '100px',
    width: '150px'
  }
});

class PrimaryHeader extends React.Component {
  render() {
    const { classes } = this.props;
    return (
      <AppBar position="static">
        <Toolbar>
          <img src={uwBlockWLogo} className={classes.uwBlockWLogo} />
          <Typography type="title" color="inherit">{this.props.title}</Typography>
          {this.props.children}
        </Toolbar>
      </AppBar>
    );
  }
}

PrimaryHeader.propTypes = {
  title: PropTypes.string.isRequired
};

export default withStyles(styles)(PrimaryHeader);
