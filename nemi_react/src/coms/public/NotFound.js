import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'

import Exception from 'ant-design-pro/lib/Exception';
import 'ant-design-pro/dist/ant-design-pro.css';

import { Button } from 'antd';

import { NProgress } from '../../utills/loading'


class NotFound extends Component {

  componentDidMount(){
    NProgress.done();
  }

  GoBack = () =>{
    NProgress.start();
    this.props.history.go(-2)
  }


  GoIndex = () =>{
    NProgress.start();
    this.props.history.push('/')
  }


  render() {
    const actions = (
      <div>
        <Button type="primary" onClick={this.GoBack}>返回上一页</Button>
        <Button onClick={this.GoIndex}>返回首页</Button>
      </div>
    );
    return (
      <Exception type="404" actions={actions} style={{ margin: "5rem 0 0 0" }}/>
    );
  }
}

export default withRouter(NotFound);
