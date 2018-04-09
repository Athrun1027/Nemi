import React, { Component } from 'react';
import { withRouter, Switch, Route } from 'react-router-dom'

import Users from './users'
import Groups from './groups'


class Admin extends Component {

  render() {
    return (
      <Switch>
        <Route exact path="/admin/user-admin" component={Users}/>
        <Route exact path="/admin/group-admin" component={Groups}/>
      </Switch>
    );
  }
}

export default withRouter(Admin);
