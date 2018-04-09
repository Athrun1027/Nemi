import React, { Component } from 'react';
import Cookies from 'js-cookie'
import { Route, Switch, withRouter } from 'react-router-dom'

import { Layout } from 'antd';

import { GetLoginUser } from '../apis/user'
import { NProgress } from '../utills/loading'
import '../css/home.css';

import SiderBar from './public/SiderbarPage'
import HeaderBar from './public/HeaderPage'
import FooterBar from './public/FooterPage'

import DashBoard from './dashboard/DashBoard'
import Space from './space/SpacePage'
import Share from './share/SharePage'
import Person from './person/PersonPage'
import Admin from './admin/AdminPage'
import Advanced from './advanced/AdvancedPage'


class Home extends Component {
  state = {
    collapsed: false,
    load: false
  };

  toggle = () => {
    this.setState({
      collapsed: !this.state.collapsed,
    });
  }

  componentWillMount(){
    const { history } = this.props;
    if (!Cookies.get("token")){
      NProgress.start();
      history.push("/login")
    }
  }

  componentDidMount(){
    GetLoginUser(this);
    NProgress.done();
  }

  componentWillUpdate(nextProps, nextState) {
    const { history } = this.props;
    if (!Cookies.get("token")){
      NProgress.start();
      history.push("/login")
    }
  }

  render() {
    if (!this.state.load) {
      return <div></div>
    };

    return (
      <Layout>
        <SiderBar collapsed={this.state.collapsed}/>
        <Layout>
          <HeaderBar
          collapsed={this.state.collapsed}
          toggle={this.toggle.bind(this)}/>
          <Layout.Content style={{ minHeight: 280 }}>
            <Switch>
              <Route exact path="/" component={DashBoard}/>
              <Route path="/space" component={Space}/>
              <Route path="/share" component={Share}/>
              <Route path="/person" component={Person}/>
              <Route path="/admin" component={Admin}/>
              <Route path="/advanced" component={Advanced}/>
            </Switch>
          </Layout.Content>
          <FooterBar />
        </Layout>
      </Layout>
    );
  }
}

export default withRouter(Home);
