import '../css/uwsolar.css';

import HomeRoute from './home-route.jsx';
import React from 'react';
import ReactDOM from 'react-dom';

class App extends React.Component {
  render() {
    return <HomeRoute />;
  }
}

ReactDOM.render(<App />, document.getElementById('app'));
