import '../css/uwsolar.css';
import 'react-dates/initialize';

import Button from 'material-ui/Button';
import HomeRoute from './home-route.jsx';
import PrimaryHeader from './primary-header.jsx';
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route } from 'react-router-dom';
import { MuiThemeProvider, createMuiTheme, withStyles } from 'material-ui/styles';

const theme = createMuiTheme({
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
        <BrowserRouter>
          <div>
            <PrimaryHeader title="UW Solar Power Monitor" />
            <div className={classes.content}>
              <Route exact path="/" component={HomeRoute} />
            </div>
          </div>
        </BrowserRouter>
      </MuiThemeProvider>
    );
  }
}

const AppWithStyles = withStyles(styles)(App);
ReactDOM.render(<AppWithStyles />, document.getElementById('app'));
