import React, { Component } from 'react';
import { withRouter, Switch, Route } from 'react-router-dom'

import SpaceMine from './mine'
import SpaceGroup from './group'
import SpaceSearch from './search'

import '../../css/space.css';


class Space extends Component {
  state = {
    loading: false,
  };

  render() {
    return (
      <Switch>
        <Route exact path="/space/mine" component={SpaceMine}/>
        <Route exact path="/space/group" component={SpaceGroup}/>
        <Route exact path="/space/search" component={SpaceSearch}/>
      </Switch>
    );
  }
}

export default withRouter(Space);
