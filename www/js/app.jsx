import '../css/uwsolar.css';

import Button from 'material-ui/Button';
import HomeRoute from './home-route.jsx';
import PrimaryHeader from './primary-header.jsx';
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route } from 'react-router-dom';

const styles = (theme) => ({
  content: {
    margin: '16px auto',
    width: '90%'
  }
});

class App extends React.Component {
  render() {
    return (
      <BrowserRouter>
        <div>
          <PrimaryHeader title="UW Solar Power Monitor" />
          <div className={classes.content}>
            <Route exact path="/" component={HomeRoute} />
          </div>
        </div>
      </BrowserRouter>
    );
  }
}

ReactDOM.render(<App />, document.getElementById('app'));
