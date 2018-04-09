import React, { Component } from 'react';
import '../css/App.css';
import Login from './LoginPage'
import Test from './TestPage'
import Home from './HomePage'
import NotFound from './public/NotFound'
// import Cookies from 'js-cookie'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'


class App extends Component {
  state = {
    words: "Affix bottom",
    dataSource: [],
    result: [],
  };

  render() {
    return (
        <Router>
          <div className="App">
            <Switch>
              <Route exact path="/login" component={Login}/>
              <Route exact path="/404" component={NotFound}/>
              <Route exact path="/test" component={Test}/>
              <Route path="/" component={Home}/>
            </Switch>
          </div>
        </Router>
    );
  }
}

export default App;
