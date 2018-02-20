import '../css/uwsolar.css';

import AboutRoute from './about-route.jsx';
import Button from 'material-ui/Button';
import HomeRoute from './home-route.jsx';
import PrimaryHeader from './primary-header.jsx';
import React from 'react';
import ReactDOM from 'react-dom';
import { HashRouter, Link, Route } from 'react-router-dom';
import { MuiThemeProvider, createMuiTheme, withStyles } from 'material-ui/styles';
import { UW_PRIMARY_PURPLE, UW_SECONDARY_LIGHT_GRAY } from './palette.js';

const theme = createMuiTheme({
  palette: {
    primary: UW_PRIMARY_PURPLE,
    secondary: UW_SECONDARY_LIGHT_GRAY
  },
  typography: { fontFamily: 'Open Sans' },
  overrides: {
    // Allow overflow content to be displayed when it is expanded.
    // See https://github.com/mui-org/material-ui/issues/9483 for further
    // details.
    MuiCollapse: {
      entered: {
        height: 'auto',
        overflow: 'visible'
      }
    }
  }
});

const styles = (theme) => ({
  content: {
    margin: '16px auto',
    width: '90%'
  }
});

class App extends React.Component {
  render() {
    const { classes } = this.props;
    return (
      <MuiThemeProvider theme={theme}>
        <HashRouter>
          <div>
            <PrimaryHeader title="Solar Power Monitor">
              <Button color="inherit"><Link to="/">Home</Link></Button>
              <Button color="inherit" className="{classes.button}"><Link to="/about">About</Link></Button>
            </PrimaryHeader>
            <div className={classes.content}>
              <Route exact path="/" component={HomeRoute} />
              <Route exact path="/about" component={AboutRoute} />
            </div>
          </div>
        </HashRouter>
      </MuiThemeProvider>
    );
  }
}

const AppWithStyles = withStyles(styles)(App);
ReactDOM.render(<AppWithStyles />, document.getElementById('app'));
