import React, { Component } from 'react';
import { withRouter, Switch, Route } from 'react-router-dom'

import UserDisable from './users'
import GroupDisabled from './groups'
import FileDisable from './files'


class Advanced extends Component {

  render() {
    return (
      <Switch>
        <Route exact path="/advanced/user-disabled" component={UserDisable}/>
        <Route exact path="/advanced/group-disabled" component={GroupDisabled}/>
        <Route exact path="/advanced/file-disabled" component={FileDisable}/>
      </Switch>
    );
  }
}

export default withRouter(Advanced);
