import '../css/uwsolar.css';

import HomeRoute from './home-route.jsx';
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route } from 'react-router-dom';

class App extends React.Component {
  render() {
    return (
      <BrowserRouter>
        <Route exact path="/" component={HomeRoute} />
      </BrowserRouter>
    );
  }
}

ReactDOM.render(<App />, document.getElementById('app'));
