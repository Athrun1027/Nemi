import React, { Component } from 'react';
import { withRouter, Switch, Route } from 'react-router-dom'

import ShareFrom from './sharefrom'
import ShareTo from './shareto'

import '../../css/space.css';


class Share extends Component {
  state = {
    loading: false,
  };

  render() {
    return (
      <Switch>
        <Route exact path="/share/from" component={ShareFrom}/>
        <Route exact path="/share/to" component={ShareTo}/>
      </Switch>
    );
  }
}

export default withRouter(Share);
