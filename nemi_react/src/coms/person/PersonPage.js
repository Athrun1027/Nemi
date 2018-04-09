import React, { Component } from 'react';
import { withRouter, Switch, Route } from 'react-router-dom'

import Info from './info'
import Help from './help'
import Logging from './logging'


class Person extends Component {

  render() {
    return (
      <Switch>
        <Route exact path="/person/info" component={Info}/>
        <Route exact path="/person/help" component={Help}/>
        <Route exact path="/person/logging" component={Logging}/>
      </Switch>
    );
  }
}

export default withRouter(Person);
